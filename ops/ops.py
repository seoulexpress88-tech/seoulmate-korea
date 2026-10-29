"""Seoulmate team operations: task board, approval queue, work reports and the monitoring dashboard.

Agents record their work here; only the owner decides approvals.

  py ops/ops.py task add --agent dev --title "..." [--detail "..."]
  py ops/ops.py task update T-0003 --status doing|review|blocked|done [--note "..."]
  py ops/ops.py approval request --agent dev --task T-0003 --action "..." --why "..." --risk low|medium|high [--files a,b]
  py ops/ops.py approval list [--status pending]
  py ops/ops.py approval decide A-0002 --decision approved|rejected --by owner [--note "..."]
  py ops/ops.py report add --agent research --title "..." (--body "..." | --body-file path) [--task T-0003]
  py ops/ops.py status
  py ops/ops.py serve [--port 8790]        # dashboard at http://localhost:8790

Standard library only. Data lives in ops/board.json, ops/reports/ and ops/activity.jsonl.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

OPS = Path(__file__).resolve().parent
BOARD = OPS / "board.json"
LOCK = OPS / ".board.lock"
REPORTS = OPS / "reports"
ACTIVITY = OPS / "activity.jsonl"
TEAM = json.loads((OPS / "team.json").read_text(encoding="utf-8"))
AGENTS = {a["id"]: a for a in TEAM["agents"]}
STATUSES = ["todo", "doing", "waiting_approval", "review", "blocked", "done"]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def now():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


class Locked:
    """Cross-process lock so several agents can write the board safely."""
    def __enter__(self):
        for _ in range(100):
            try:
                self.fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                if time.time() - LOCK.stat().st_mtime > 30:  # stale lock
                    LOCK.unlink(missing_ok=True)
                time.sleep(0.1)
        raise SystemExit("board is busy, try again")

    def __exit__(self, *exc):
        os.close(self.fd)
        LOCK.unlink(missing_ok=True)


def load():
    if BOARD.exists():
        return json.loads(BOARD.read_text(encoding="utf-8"))
    return {"tasks": [], "approvals": [], "reports": [], "seq": {"T": 0, "A": 0, "R": 0}}


def save(b):
    tmp = BOARD.with_suffix(".tmp")
    tmp.write_text(json.dumps(b, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(BOARD)


def next_id(b, kind):
    b["seq"][kind] += 1
    return f"{kind}-{b['seq'][kind]:04d}"


def log(agent, event, text, ref=""):
    with ACTIVITY.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"at": now(), "agent": agent, "event": event, "text": text, "ref": ref}, ensure_ascii=False) + "\n")


def need_agent(a):
    if a not in AGENTS:
        raise SystemExit(f"unknown agent '{a}'. Use one of: {', '.join(AGENTS)}")


def find(items, id_):
    for x in items:
        if x["id"] == id_:
            return x
    raise SystemExit(f"{id_} not found")


# ---------------------------------------------------------------- commands

def task_add(a):
    need_agent(a.agent)
    with Locked():
        b = load()
        t = {"id": next_id(b, "T"), "title": a.title, "detail": a.detail or "", "agent": a.agent, "status": "todo",
             "created": now(), "updated": now(), "notes": []}
        b["tasks"].append(t)
        save(b)
    log(a.agent, "task_add", a.title, t["id"])
    print(t["id"])


def task_update(a):
    if a.status and a.status not in STATUSES:
        raise SystemExit(f"status must be one of {STATUSES}")
    with Locked():
        b = load()
        t = find(b["tasks"], a.id)
        if a.status == "done":
            open_apr = [x for x in b["approvals"] if x["task"] == t["id"] and x["status"] == "pending"]
            if open_apr:
                raise SystemExit(f"{t['id']} still has a pending approval ({open_apr[0]['id']}); it can't be done yet")
        if a.status:
            t["status"] = a.status
        if a.note:
            t["notes"].append({"at": now(), "text": a.note})
        t["updated"] = now()
        save(b)
    log(t["agent"], "task_update", f"{a.status or ''} {a.note or ''}".strip(), t["id"])
    print(f"{t['id']} -> {t['status']}")


def approval_request(a):
    need_agent(a.agent)
    if a.risk not in ("low", "medium", "high"):
        raise SystemExit("risk must be low, medium or high")
    with Locked():
        b = load()
        t = find(b["tasks"], a.task) if a.task else None
        r = {"id": next_id(b, "A"), "agent": a.agent, "task": a.task or "", "action": a.action, "why": a.why,
             "risk": a.risk, "files": [f.strip() for f in (a.files or "").split(",") if f.strip()],
             "status": "pending", "requested": now(), "decided": "", "by": "", "note": ""}
        b["approvals"].append(r)
        if t:
            t["status"] = "waiting_approval"
            t["updated"] = now()
        save(b)
    log(a.agent, "approval_request", a.action, r["id"])
    print(f"{r['id']} pending. Stop here and wait for the owner's decision.")


def approval_list(a):
    b = load()
    for r in b["approvals"]:
        if a.status and r["status"] != a.status:
            continue
        print(f"{r['id']} [{r['status']}] {r['agent']} · {r['action']} (risk {r['risk']}, task {r['task'] or '-'})"
              + (f" → {r['by']} {r['decided']} {r['note']}" if r["decided"] else ""))


def decide(id_, decision, by, note):
    if decision not in ("approved", "rejected"):
        raise SystemExit("decision must be approved or rejected")
    if by != "owner":
        raise SystemExit("only the owner can decide approvals (--by owner)")
    with Locked():
        b = load()
        r = find(b["approvals"], id_)
        if r["status"] != "pending":
            raise SystemExit(f"{id_} is already {r['status']}")
        r.update(status=decision, decided=now(), by="owner", note=note or "")
        if r["task"]:
            t = find(b["tasks"], r["task"])
            t["status"] = "doing" if decision == "approved" else "blocked"
            t["notes"].append({"at": now(), "text": f"{id_} {decision} by owner" + (f": {note}" if note else "")})
            t["updated"] = now()
        save(b)
    log("owner", f"approval_{decision}", r["action"], id_)
    return r


def approval_decide(a):
    r = decide(a.id, a.decision, a.by, a.note)
    print(f"{r['id']} {r['status']}")


def report_add(a):
    need_agent(a.agent)
    body = Path(a.body_file).read_text(encoding="utf-8") if a.body_file else (a.body or "")
    if not body.strip():
        raise SystemExit("report body is empty")
    REPORTS.mkdir(exist_ok=True)
    with Locked():
        b = load()
        rid = next_id(b, "R")
        slug = re.sub(r"[^0-9A-Za-z가-힣]+", "-", a.title).strip("-")[:40] or "report"
        path = REPORTS / f"{dt.date.today().isoformat()}_{rid}_{a.agent}_{slug}.md"
        path.write_text(f"# {a.title}\n\n- 작성: {AGENTS[a.agent]['name']} ({AGENTS[a.agent]['role']})\n- 일시: {now()}\n"
                        f"- 관련 작업: {a.task or '-'}\n\n{body}\n", encoding="utf-8")
        b["reports"].append({"id": rid, "agent": a.agent, "title": a.title, "task": a.task or "", "at": now(),
                             "file": path.relative_to(OPS).as_posix()})
        save(b)
    log(a.agent, "report", a.title, rid)
    print(rid, path)


def status(_):
    b = load()
    pending = [r for r in b["approvals"] if r["status"] == "pending"]
    print(f"승인 대기 {len(pending)}건")
    for r in pending:
        print(f"  {r['id']} {AGENTS[r['agent']]['name']}: {r['action']} (위험도 {r['risk']})")
    for ag in TEAM["agents"]:
        mine = [t for t in b["tasks"] if t["agent"] == ag["id"] and t["status"] != "done"]
        print(f"{ag['emoji']} {ag['name']}({ag['role']}): 진행 {len(mine)}건" + "".join(f"\n    {t['id']} [{t['status']}] {t['title']}" for t in mine))


# ---------------------------------------------------------------- dashboard

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, (OPS / "dashboard.html").read_text(encoding="utf-8"), "text/html; charset=utf-8")
        if self.path == "/api/board":
            b = load()
            act = ACTIVITY.read_text(encoding="utf-8").splitlines()[-60:] if ACTIVITY.exists() else []
            b["activity"] = [json.loads(x) for x in reversed(act)]
            b["team"] = TEAM
            return self._send(200, json.dumps(b, ensure_ascii=False))
        m = re.fullmatch(r"/api/reports/(R-\d{4})", self.path)
        if m:
            r = find(load()["reports"], m.group(1))
            return self._send(200, (OPS / r["file"]).read_text(encoding="utf-8"), "text/plain; charset=utf-8")
        self._send(404, '{"error":"not found"}')

    def do_POST(self):
        m = re.fullmatch(r"/api/approvals/(A-\d{4})", self.path)
        # Only accept decisions made from this computer's browser.
        if not m or self.client_address[0] not in ("127.0.0.1", "::1"):
            return self._send(404, '{"error":"not found"}')
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0)) or 0) or b"{}")
            r = decide(m.group(1), data.get("decision"), "owner", data.get("note", ""))
            self._send(200, json.dumps(r, ensure_ascii=False))
        except SystemExit as e:
            self._send(400, json.dumps({"error": str(e)}, ensure_ascii=False))


def serve(a):
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    print(f"Seoulmate 팀 대시보드: http://localhost:{a.port}  (끄려면 Ctrl+C)")
    srv.serve_forever()


def main():
    p = argparse.ArgumentParser(prog="ops")
    sp = p.add_subparsers(dest="cmd", required=True)

    t = sp.add_parser("task").add_subparsers(dest="sub", required=True)
    x = t.add_parser("add"); x.add_argument("--agent", required=True); x.add_argument("--title", required=True); x.add_argument("--detail"); x.set_defaults(fn=task_add)
    x = t.add_parser("update"); x.add_argument("id"); x.add_argument("--status"); x.add_argument("--note"); x.set_defaults(fn=task_update)

    ap = sp.add_parser("approval").add_subparsers(dest="sub", required=True)
    x = ap.add_parser("request"); x.add_argument("--agent", required=True); x.add_argument("--task"); x.add_argument("--action", required=True)
    x.add_argument("--why", required=True); x.add_argument("--risk", default="medium"); x.add_argument("--files"); x.set_defaults(fn=approval_request)
    x = ap.add_parser("list"); x.add_argument("--status"); x.set_defaults(fn=approval_list)
    x = ap.add_parser("decide"); x.add_argument("id"); x.add_argument("--decision", required=True); x.add_argument("--by", required=True)
    x.add_argument("--note"); x.set_defaults(fn=approval_decide)

    rp = sp.add_parser("report").add_subparsers(dest="sub", required=True)
    x = rp.add_parser("add"); x.add_argument("--agent", required=True); x.add_argument("--title", required=True); x.add_argument("--body")
    x.add_argument("--body-file"); x.add_argument("--task"); x.set_defaults(fn=report_add)

    sp.add_parser("status").set_defaults(fn=status)
    x = sp.add_parser("serve"); x.add_argument("--port", type=int, default=8790); x.set_defaults(fn=serve)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
