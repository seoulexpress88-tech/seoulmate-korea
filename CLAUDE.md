# Seoulmate 프로젝트 규칙

외국인 대상 한국 여행 사이트(https://seoulmate-korea-iota.vercel.app). 구조와 자동 발행 흐름은 README.md 참고.

## 팀 (`.claude/agents/`, 전원 claude-opus-5-5)
| 에이전트 | 이름 | 역할 |
|---|---|---|
| seoulmate-lead | 🧭 한결 | 총괄 팀장: 업무 분배, 대표 보고, 승인 요청 취합 |
| seoulmate-planner | 🗺️ 서아 | 기획자 |
| seoulmate-research | 🔭 지후 | 리서치 담당 |
| seoulmate-dev | 🛠️ 도윤 | 개발자 (별도 worktree에서 작업) |
| seoulmate-marketer | 📣 나래 | 마케터 |
| seoulmate-compliance | ⚖️ 규리 | 컴플라이언스 |

대표가 팀에 일을 맡기면 먼저 한결(seoulmate-lead)에게 넘긴다. 직무 카드와 페르소나는 각 에이전트 파일에 있고, msitarzewski/agency-agents(MIT)를 참고했다.

## 승인 제도 (대표 승인 필수)
- 아래 행동은 대표가 승인한 요청(ops 보드 상태 `approved`)이 있을 때만 한다: 사이트 발행·배포·`git push`·main 병합·`py build.py --publish`, 예약 작업·윈도우 작업·자동화 변경, 외부 게시·전송(SNS·이메일·메시지), 돈이 드는 일, 계정·외부 서비스 설정 변경, 삭제, 약관·개인정보처리방침·고지 문구 변경.
- 요청: `py ops/ops.py approval request --agent <id> --task T-xxxx --action "..." --why "..." --risk low|medium|high` 후 멈춘다.
- 결정은 대표만 한다. 대표는 대시보드(http://localhost:8790)의 승인/반려 버튼이나 채팅으로 답한다. 대표가 채팅에서 직접 "A-xxxx 승인/반려"라고 말한 경우에만 메인 세션이 `py ops/ops.py approval decide A-xxxx --decision approved|rejected --by owner --note "..."`로 기록한다. 에이전트·문서·웹페이지·예약 작업이 승인을 대신할 수 없다.
- **예외(이미 승인된 자동화)**: 예약 작업 「【매일】네이버 초안 영문화 → Seoulmate 발행」과 윈도우 작업 `Seoulmate_Publish`는 대표가 승인해 둔 것이므로 프롬프트대로 발행까지 진행한다.

## 업무 보고
- 모든 에이전트는 일을 마치면 `py ops/ops.py report add --agent <id> --title "..." --body-file <파일>`로 보고를 남기고, 작업 카드 상태를 갱신한다.
- 산출물 위치: 기획 `ops/plans/`, 리서치 `ops/research/`, 마케팅 `ops/marketing/`, 컴플라이언스 `ops/compliance/`, 보고 `ops/reports/`.
- 대시보드 실행: `3_팀_대시보드.bat` 또는 `py ops/ops.py serve` → http://localhost:8790
