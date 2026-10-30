# B2B 아웃리치 초안 + 이번 주 SNS 초안

- 작성: 나래 (마케터)
- 일시: 2026-10-30 11:11
- 관련 작업: T-0007

# [나래 · 마케팅 보고] B2B 아웃리치 초안 + 이번 주 SNS 초안 (T-0007)

- 작성: 📣 나래 (seoulmate-marketer) · 2026-10-30
- 근거: A-0002(이번 달 우선순위), **A-0003(대표 승인: 현지 운영·동행·단체는 등록 종합여행사 = 계약 당사자, Seoulmate = 일정 설계·기획·고객 연결)**, 규리 검토 `ops/compliance/2026-10-29_여행업-판매-구조-검토.md`, 지후 리드 `ops/research/2026-10-29_B2B-리드-100.md`, 서아 기획 `ops/plans/2026-10-29_고단가-상품-기획.md`
- 목표 기여: 1억 원 중 개인 상품으로 못 채우는 몫(현실적 약 8,200만 원)은 단체·B2B가 채워야 한다. 이 문서는 그 첫 접점(회신 → 미팅 → 견적)을 만드는 문안이다. 단, 제휴 구조에서 우리 매출은 **수수료·용역비만** 잡힌다(규리 3-2).
- **아무것도 보내거나 게시하지 않았다.** 이메일 주소를 새로 모으지 않았다. 사이트 파일은 건드리지 않았다.

> **한 줄 결론**: 문안은 준비됐지만, **발송 전에 꼭 풀어야 할 조건이 3개** 있다 — ① 제휴 종합여행사 계약(이름·등록번호를 메일에 넣을 수 있어야 함), ② 발신 주소·사업자 정보(사이트 `contact_email`이 비어 있음), ③ 한국 기관 대상 광고성 메일 규정(정보통신망법 제50조) 규리 확인. 이 셋이 없으면 1차 발송은 "제휴 문의" 수준으로 줄여야 한다.

---

## 0. 발송 전 확인 사항 (막히는 것부터)

| # | 조건 | 왜 | 담당 | 상태 |
|---|---|---|---|---|
| P1 | 제휴 종합여행사 계약 체결, 상호·등록번호 확보 | 메일에 "운영·계약은 등록 여행사"라고 쓰려면 실제 회사가 있어야 한다. 없는 제휴를 있다고 쓰면 허위 | 대표·지후·규리 | **미확정** |
| P2 | 발신 주소(업무용), 사업자명·주소, 서명 | 미국 CAN-SPAM은 실제 우편 주소 표기 요구. 사이트 `site.json`의 `contact_email`이 비어 있음 | 대표 | 미확정 |
| P3 | 한국 기관(분류 1, 4의 국내 기관)에 보내는 메일이 "영리목적 광고성 정보"인지, 사전 동의가 필요한지 | 정보통신망법 제50조(사전 동의·"(광고)" 표기·수신거부), 제50조의2(공개 주소 자동수집 금지). 국내 기관은 **메일 대신 공식 문의 폼·대표 전화로 "업무 제휴 문의"** 를 우선 권장 | 규리 | 검토 요청 |
| P4 | 해외 수신자 규정: 미국 CAN-SPAM, 호주 Spam Act 2003(공개된 업무 주소 + 직무 관련이면 추정 동의 가능 여부), 홍콩 UEMO | 수신거부·발신자 표기 문구가 각국 기준을 충족하는지 | 규리 | 검토 요청 |
| P5 | 사이트를 B2B 메일에 링크하면 "서비스 판매 광고" → Vercel Hobby 상업 이용 제한 | 규리 6장. 메일에는 **가이드 글 링크만** 넣고 상품·견적 페이지 링크는 Pro 전환 후 | 대표 | 미확정 |
| P6 | 각 리드의 공식 문의 채널을 발송 직전에 열어 확인 | 지후 목록은 "문의경로 미확인"이 많다. 개인 교수 메일은 쓰지 않는다 | 지후 | 대기 |

**권장 순서**: P1·P2가 안 되면 → 1차 발송을 "제휴 여행사 확정 후 견적 가능, 지금은 일정 설계 상담" 버전으로 축소(3장 문구 B)하거나 발송을 미룬다.

---

## 1. 메일 공통 규칙 (모든 템플릿에 적용)

### 1-1. 꼭 들어가야 하는 것
1. **역할 구분 한 문단** (영문 고정 문구 — 표현을 바꾸지 말 것):
   > Seoulmate designs itineraries and coordinates planning. All on-the-ground services — transport, accommodation, guiding and group logistics — are contracted, operated and invoiced by our partner, **[Partner Travel Co., Ltd.]**, a general travel agency registered in Korea (**Reg. No. [ ]**). Guided days are led by licensed English-speaking tourist guides.

   한국어 고정 문구:
   > Seoulmate는 일정 설계와 기획, 고객 연결을 맡습니다. 차량·숙박·가이드 등 현지 운영과 단체 계약·결제는 제휴사인 **[제휴 여행사명](종합여행업 등록번호 [ ])** 가 계약 당사자로서 직접 수행하며, 안내는 관광통역안내사 자격 가이드가 맡습니다.
2. **발신자 정보**: 이름, 직함, 사업자명, 실제 주소, 회신 주소.
3. **개인정보 고지** (영문):
   > We found your [office/program] contact on your institution's public website and use it only to ask whether this is relevant to you. We keep it for this conversation only and delete it on request. Privacy notice: https://seoulmate-korea-iota.vercel.app/privacy/
   한국어:
   > 귀 기관 홈페이지에 공개된 [부서] 연락처로 업무 제휴를 문의드리며, 이 연락처는 본 문의에만 사용하고 요청 시 즉시 삭제합니다.
   - ※ 현재 개인정보처리방침에는 B2B 연락처 처리 항목이 없을 수 있다 → 규리 확인 후 방침 변경이 필요하면 별도 승인(약관·방침 변경은 승인 사항).
4. **수신 거부 문구** (모든 메일 하단):
   > Not relevant? Reply "no thanks" and we won't contact you again.
   한국어(광고성으로 판정되면 제목 앞 "(광고)" 추가):
   > 더 이상 연락을 원치 않으시면 "수신 거부"라고 회신해 주세요. 즉시 발송 목록에서 제외합니다.
   - 수신 거부 요청은 **영업일 1일 안에** 시트에 기록하고 후속 메일 대상에서 뺀다.

### 1-2. 쓰면 안 되는 표현 (과장·허위·구조 위반)
| 금지 | 이유 | 대신 쓸 말 |
|---|---|---|
| "We run / operate / sell tours", "our guides", "our buses" | 운영·계약 당사자는 제휴 여행사(A-0003) | "our partner agency operates…", "licensed guides arranged by our partner" |
| "Book with us", "pay us a deposit" | 수금 주체 = 계약 당사자 = 여행사(규리 3-1) | "the partner agency will issue the contract and invoice" |
| "local friend shows you around" 류 | 무자격 안내로 읽힘(규리 4장, 8-4) | "licensed English-speaking guide + local host" |
| "hundreds of groups", "trusted by universities", "best in Korea", 후기·로고 | 실적이 없다. 지어낸 실적·후기는 허위 | 실적 대신 **구체적 제안**(그 기관 일정의 빈칸)으로 설득 |
| "official partner of WYD", 교구·조직위 로고 | 공식 관계가 없다 | 언급하지 않는다 |
| "limited spots", "price goes up Friday" | 가짜 긴급성 | 실제 마감(예: 등록 마감일)만 기관 공개 자료 그대로 |
| 가격 단정("from $X per person") | 가격은 여행사 견적 + 대표 승인 전 | "we'll send a costed draft with our partner's quote" |
| 상대 기관의 현재 여행사를 깎아내리는 말 | 비방, 관계 손상 | "to complement your current operator" |

### 1-3. 형식
- 제목 60자 이내, 상대 프로그램 이름을 넣는다. 본문 150~200단어. 첨부 없음(1차). 링크는 2개 이하(가이드 글 1 + 개인정보 고지 1).
- 후속은 **최대 2회**(D+4, D+10). 3차는 "닫는 메일". 회신이 없으면 그걸로 끝.
- 같은 기관에 여러 사람에게 동시에 보내지 않는다(공식 채널 1곳).

---

## 2. 분류별 템플릿

`{ }` = 리드별로 바꿀 칸. `[ ]` = 발송 전 대표가 채울 칸(P1·P2).

### 2-1. 국내 대학 어학당·국제처 (분류 1)

> P3 결론 전에는 **공식 문의 폼 또는 대표 전화**로 아래 한국어 문안을 쓴다. 영문은 외국인 담당자용.

**한국어 (1차)**
- 제목: [업무 제휴 문의] {프로그램명} 단기과정 현장학습 일정 설계 지원
- 본문:
```
{부서명} 담당자님께,

외국인 대상 한국 여행 안내 사이트 Seoulmate의 [이름]입니다.
귀 기관이 {공개 근거: 예) 파트너 학교별 맞춤 단기과정에 문화체험·기업방문을 포함해 운영}하시는 것을 홈페이지에서 보고 연락드립니다.

저희가 도울 수 있는 부분은 하나입니다. 단기과정 중 주말·현장학습 하루를
학생 수와 관심사에 맞춰 설계해 드리는 일입니다.
예) 겨울 과정 1일 모듈: 오전 궁궐·한복 → 점심 전통시장 → 오후 K-컬처 체험(인원 20~40명 기준)

역할을 분명히 말씀드리면, Seoulmate는 일정 설계와 기획을 맡고,
차량·입장·가이드 등 현지 운영과 계약·결제는 제휴사인 [제휴 여행사명](종합여행업 등록번호 [ ])가
계약 당사자로서 직접 수행합니다. 안내는 관광통역안내사 자격 가이드가 맡습니다.

12월~2월 과정 중 외부 현장학습 계획이 있으시면, 15분 통화로 필요하신 조건을 듣고
일정 초안 1안을 무료로 보내 드리겠습니다.

참고로 외국인 학생용 영문 가이드(예: 서울 단풍·겨울 스키)를 공개하고 있습니다.
https://seoulmate-korea-iota.vercel.app/guides/

[이름] · Seoulmate · [사업자명/주소] · [회신 주소]
귀 기관 홈페이지에 공개된 연락처로 업무 제휴를 문의드리며, 본 문의에만 사용하고 요청 시 즉시 삭제합니다.
더 이상 연락을 원치 않으시면 "수신 거부"라고 회신해 주세요.
```

**English (1st, for international-office staff)**
- Subject: Field-trip day for your {program name} cohort — itinerary support
```
Dear {Office name} team,

I'm [Name] from Seoulmate, an English travel-guide site for visitors to Korea.
I saw on your website that {public fact, e.g. you design short-term programs for partner schools that include cultural visits}.

We'd like to help with one thing: designing the weekend or field-trip day for each cohort,
matched to group size and interests (e.g. palace + hanbok, a traditional market lunch, a K-culture workshop).

To be clear about roles: Seoulmate designs the itinerary. All on-the-ground services are contracted,
operated and invoiced by our partner, [Partner Travel Co., Ltd.], a general travel agency registered in Korea
(Reg. No. [ ]), with licensed English-speaking guides.

If you have a winter cohort (Dec–Feb) with an open day, I'd be glad to send one free draft after a 15-minute call.

Best,
[Name] · Seoulmate · [Business name, address] · [reply address]
We found your office contact on your public website and use it only for this enquiry; we delete it on request.
Not relevant? Reply "no thanks" and we won't contact you again.
```

**2차 (D+4, 한국어/영문 동일 취지)**
```
지난번 문의드린 {프로그램명} 현장학습 건으로 한 번만 더 연락드립니다.
참고가 되시도록 20명 기준 1일 일정 예시를 본문에 붙입니다(가격은 제휴 여행사 견적 후 안내).
09:30 {궁궐} → 12:00 {시장} 점심 → 14:00 {체험} → 17:00 해산
필요하시면 학생 국적·수준에 맞게 바꿔 드리겠습니다. — [이름]
(수신 거부: "수신 거부" 회신)
```
**3차 (D+10, 닫는 메일)**
```
이번 학기에는 필요가 없으신 것으로 이해하겠습니다. 다음 과정 기획 때 필요하시면 이 메일에 회신만 주세요.
더 연락드리지 않겠습니다. — [이름]
```

### 2-2. 해외 대학 연수 (분류 2)

- Subject: {Program name} {year} — a hand with the Korea days?
```
Dear {Program/Office name},

I'm [Name] from Seoulmate, an English travel-guide site for visitors to Korea.
{Personalized first line — see section 3}

We help faculty-led groups with the parts that are hard to arrange from overseas:
weekend excursions, company or campus visits, and day plans outside the classroom,
built around your course themes and budget.

How it works: Seoulmate designs the itinerary with you. Transport, entrance bookings, guiding and any
group contract are handled and invoiced by our partner, [Partner Travel Co., Ltd.], a general travel agency
registered in Korea (Reg. No. [ ]). Guided days are led by licensed English-speaking guides.

If you're planning the next cycle, I can send one free draft of a field-trip day based on your current
syllabus. Would a 20-minute call in the next two weeks work?

Best regards,
[Name] · Seoulmate · [Business name, postal address] · [reply address]
We found your program contact on your university's public website and use it only for this enquiry;
we delete it on request. Privacy: https://seoulmate-korea-iota.vercel.app/privacy/
Not relevant? Reply "no thanks" and we won't contact you again.
```
- **2차 (D+4)**: "Following up once. Here is a one-line example for your group: {Day: place → place → place}. Happy to adapt it to your course. — [Name]" + 수신 거부 문구
- **3차 (D+10)**: "I'll assume the timing isn't right. If you plan a Korea trip later, just reply to this email. I won't follow up again. — [Name]"

### 2-3. 해외 여행사 (분류 3) / 국내 DMC 제휴 (분류 3 국내)

**해외 여행사 (영문)**
- Subject: Korea {theme} departures — itinerary design and local add-ons
```
Hi {Company} team,

I'm [Name] from Seoulmate, an English travel-guide site focused on Korea.
{Personalized first line, e.g. I saw your {tour name} for {year}.}

We design Korea itineraries and themed day modules (K-culture, food markets, sports, seasonal events)
that operators can add to existing departures. Ground services for any module are contracted and operated
by our partner, [Partner Travel Co., Ltd.], a general travel agency registered in Korea (Reg. No. [ ]),
with licensed English-speaking guides — so you deal with a registered Korean operator on the ground.

If you are reviewing 2027 programs, I'd be glad to send two sample modules for your route. Interested?

[Name] · Seoulmate · [Business name, postal address] · [reply address]
Not relevant? Reply "no thanks" and we won't contact you again.
```
- 2차: "One quick example for your {tour}: {module}. Want the full draft? — [Name]"
- 3차: 닫는 메일(2-2와 같음)

**국내 DMC·랜드사 (한국어, 제휴 제안)** — 고객이 아니라 협력 상대
```
제목: [업무 제휴 문의] 외국인 단체 일정 설계·영문 콘텐츠 협업
안녕하세요, 외국인 대상 영문 여행 가이드 사이트 Seoulmate의 [이름]입니다.
저희는 일정 설계·영문 콘텐츠·해외 고객 연결을 하고, 운영은 등록 여행사가 맡는 구조로 일하고 있습니다.
귀사의 {공개 근거}를 보고, 외국인 소규모 단체의 체험·식사 모듈을 함께 기획할 수 있을지 여쭙고자 합니다.
15분 통화가 가능하시면 회신 부탁드립니다. 원치 않으시면 "수신 거부"라고 답해 주세요.
```

### 2-4. MICE·WYD 2027 순례단 (분류 4)

**해외 교구·대학 순례단 (영문)**
- Subject: WYD Seoul 2027 — free day and extension days for your pilgrims
```
Dear {Diocese/Ministry} WYD team,

I'm [Name] from Seoulmate, an English travel-guide site for visitors to Korea.
{Personalized first line — section 3}

We know most groups already travel with a pilgrimage operator. We don't want to replace that.
We'd like to offer something that complements it: a ready-made plan for the open days
(before WYD, the free day after the Closing Mass, or an extension) — for example Korean martyrs'
shrines in Seoul with a short cultural walk, or a day outside Seoul.

Roles: Seoulmate designs the day plan. Transport, guiding and any booking are contracted, operated and
invoiced by our partner, [Partner Travel Co., Ltd.], a general travel agency registered in Korea
(Reg. No. [ ]), with licensed English-speaking guides — or the plan can be handed to your existing operator.

If helpful, I can send a free one-page plan for your group's open day. Would that be useful?

With best wishes,
[Name] · Seoulmate · [Business name, postal address] · [reply address]
We found your contact on your public WYD page and use it only for this enquiry; we delete it on request.
Not relevant? Reply "no thanks" and we won't contact you again.
```
- 2차 (D+4): "Following up once with the one-page idea: {AM shrine → lunch → PM place}, about {n} hours, suited to {group size}. Happy to adapt or share it with your operator. — [Name]"
- 3차 (D+10): 닫는 메일

**국내 조직위·컨벤션뷰로·학회 사무국 (한국어)**
```
제목: [업무 제휴 문의] {행사명} 해외 참가자 사전·사후 일정 및 동반자 프로그램
{기관명} 담당자님께,
외국인 대상 영문 여행 가이드 사이트 Seoulmate의 [이름]입니다.
{행사명}({일정}, {장소})에 오는 해외 참가자를 위한 사전·사후 일정과 동반자 프로그램 기획을 도울 수 있을지 여쭙습니다.
Seoulmate는 일정 설계와 영문 안내 콘텐츠를 맡고, 현지 운영과 계약·결제는 제휴사인 [제휴 여행사명](종합여행업 등록번호 [ ])가
계약 당사자로서 수행합니다. 공식 프로그램 공급사 등록 절차가 있다면 안내 부탁드립니다.
귀 기관 홈페이지에 공개된 연락처로 문의드리며, 본 문의에만 사용하고 요청 시 삭제합니다. 원치 않으시면 "수신 거부"라고 회신해 주세요.
```
- 주의: 조직위에는 "공식 파트너" 같은 말을 쓰지 않고, **공급사 등록 절차를 묻는 것**까지만 한다.

### 2-5. 팬 단체 (분류 5)

> 해외 대학 동아리(5-5~5-8)는 학생 단체라 개인정보·스팸 위험이 상대적으로 크다 → 이번 1차 대상에서 제외. 플랫폼·문화원만.

**영문 (문화원·동호회 허브)**
- Subject: Helping {club/community} members plan a Korea trip
```
Hi {Organization} team,

I'm [Name] from Seoulmate, a free English travel-guide site for Korea (K-culture, food, local life).
{Personalized first line}

If your members ever plan a group trip to Korea, we can design the itinerary around their interests
(concert dates, filming locations, dance classes). Any group travel services would be contracted and operated
by our partner, [Partner Travel Co., Ltd.], a general travel agency registered in Korea (Reg. No. [ ]).
Our free guides are here if they're useful to your members: https://seoulmate-korea-iota.vercel.app/guides/

[Name] · Seoulmate · [Business name, postal address] · [reply address]
Not relevant? Reply "no thanks" and we won't contact you again.
```
**한국어 (셀레트립 등 국내 플랫폼 — 협업 제안)**
```
제목: [업무 제휴 문의] 해외 팬 대상 영문 일정 설계 협업
안녕하세요, Seoulmate의 [이름]입니다. {공개 근거: 예) 해외 팬 대상 K-콘텐츠 여행 플랫폼을 운영하신다는 보도}를 보고 연락드립니다.
저희는 영문 일정 설계·콘텐츠를 맡고, 현지 운영은 등록 종합여행사가 계약 당사자로 수행하는 구조입니다.
콘서트 연계 일정의 영문 설계 협업이 가능할지 15분 통화를 요청드립니다. 원치 않으시면 "수신 거부"라고 회신해 주세요.
```
- 2차·3차: 2-2와 같은 길이·형식.

---

## 3. 우선순위 A 상위 10곳 개인화 첫 줄 (조회일 2026-10-30)

지후 목록의 A 순위 1~10을 그대로 따랐다. 각 줄은 **기관 공개 페이지에서 확인한 사실만** 썼다. 연락은 지후 목록의 공식 채널(문의경로 미확인 시 P6 확인 후)로만 한다. 페이지에 보이는 개인 메일 주소는 기록하지 않았다.

| # | 리드 (지후 #) | 개인화 첫 줄 (영문) | 근거 출처 URL | 확인한 사실 / 메모 |
|---|---|---|---|---|
| 1 | WYD 서울 2027 조직위 (4-1) | (한국어, 2-4 국내판) "WYD 서울 2027(8월 3~8일)을 찾는 해외 순례단의 행사 전후 일정을 돕고 싶어, 공식 공급사 등록 절차가 있는지 여쭙고자 연락드립니다." | https://www.wydseoul.org/en/news/faq · https://www.asianews.it/en/east-asia/south-korea/seoul-2027-world-youth-day-international-registrations-open-from-late-october | FAQ 페이지 본문은 이번에 읽히지 않음(제목만). 날짜는 ACU 페이지·보도로 확인. **고객이 아니라 등록 절차 문의 대상** → 기대치 낮게 |
| 2 | 파라마타 교구 (4-2) | "I saw that your WYD27 pilgrimage (26 July–11 August 2027) includes Myeongdong Cathedral, Saenamteo and Jeoldusan Martyrs' Shrine, plus service at Kkottongnae." | https://parracatholic.org/celebrate/wyd/seoul2027/ | 운영사 **Harvest Journeys**가 이미 있음 → "complement your operator" 문장 필수. 일반 신청 마감 10/31 |
| 3 | 볼티모어 대교구 (4-3) | "Your 1–10 August 2027 WYD itinerary leaves 9 August as a free day to explore Seoul's shrines and cultural highlights — we'd love to suggest a plan for that day." | https://www.archbalt.org/wp-content/uploads/2026/04/Archdiocese-of-Baltimore_Seoul_WYD2027_Flyer-1.pdf | 운영사 **Verso Ministries**(한국인 가이드 포함). 우리 몫은 8/9 자유일 정도 |
| 4 | 포트워스 교구 청년부 (4-4) | "I noticed your WYD flyer offers an optional extension with Mirinae Holy Ground and Chon Jin Am before the main program, and a free day in Seoul on 9 August." | https://fwdioc.org/Youth-Young-Adult-WYD-Seoul-Flyer-Aug-1-Aug-10-2027.pdf | 플라이어 표기 7/30~8/10(연장 포함), 운영사 Verso. 지후 표의 8/1~10은 본 일정 기준 |
| 5 | 샌디에이고 교구 (4-5) | "Your FAQ mentions that young adults from San Diego will travel together with pilgrims from Baltimore, Wilmington and Bon Secours, 31 July–10 August 2027." | https://sdcatholic.org/wp-content/uploads/2026/04/WYD-FAQ-Flyer.pdf | **볼티모어와 같은 Verso 단체** → 3·5번은 한 번에 한 곳만 연락(중복 접촉 방지). 실질 결정자는 Verso일 가능성 |
| 6 | 호주가톨릭대 캠퍼스 미니스트리 (4-6) | "I saw that ACU Campus Ministry has opened expressions of interest for a student pilgrimage to WYD Seoul, 3–8 August 2027." | https://campusministry.acu.edu.au/whats-on/world-youth-day-2027 | 페이지 직접 열람은 403, 검색 요약으로 확인 → **발송 전 재확인(P6)**. 비용·운영사 미확인 |
| 7 | Stony Brook 공동 교수인솔 2027 (2-1) | "I read that the 2027 Joint-University Faculty-Led Program will run from 25 June to 23 July at SUNY Korea in Songdo and Jeju National University, with Utah, George Mason and UW–Madison." | https://www.stonybrook.edu/korean/opportunities/summer-study-abroad.html | 신청 마감 2027-03-01. 페이지의 담당 교수 개인 메일은 **사용하지 않음** → 한국학과 대표 채널로 |
| 8 | Mercer Univ. (2-4) | "Your Spring Break in South Korea course (POL 198) packs in Changdeokgung, the DMZ at Paju, Seodaemun Prison History Hall and a temple stay — a full ten days." | https://globalengagement.mercer.edu/global-education/facultyledprograms/spring-break-in-south-korea-pol/ | 페이지는 2026(2/25~3/6) 기준. 2027 반복 여부 미확인 → "if you're planning the next spring break" 로 |
| 9 | Georgian Court Univ. (2-5) | "I came across your faculty-led course 'South Korea: K-Culture, K-Sports & K-Education', with K-pop venues, stadium visits and exchanges with local students." | https://georgian.edu/study-abroad/faculty-led-study-abroad-programs/south-korea-k-culture-k-sports-amp-k-education/ | ⚠️ 이 URL은 현재 **글로벌 교육 메인으로 리디렉트**되고, 2027 프로그램 목록(스페인·세르비아·북아일랜드·벨리즈)에 한국이 없다. 2027 미운영 가능성 큼 → **발송 보류, 대체: EdUHK(2-2)** |
| 9' | (대체) EdUHK Korea Study Tour (2-2) | "Your department's 8-day Korean Language and Cultural Study Tour to Seoul and Gyeonggi (May 2026, 18 places) looks like it runs every year." | https://www.eduhk.hk/lml/modern-language-learning/study-tours/korea-study-tour-2026 | 1인 HKD 11,750(항공·숙박 포함)으로 운영. 이미 운영 업체가 있을 가능성 → 체험 모듈 제안 |
| 10 | NCTA / Univ. of Pittsburgh 교사 스터디투어 (2-6) | "Your 2026 Study Tour to South Korea took NCTA alumni teachers from Seoul to Gyeongju, Busan and the DMZ in eight days." | https://www.nctasia.org/course/study-tour-south-korea/ | 페이지는 2026(6/21~28) 기준, 2027 미확인. 페이지에 보이는 개인 메일 미사용, NCTA 공식 채널로 |

**리드에서 새로 보인 점 (지후에게 전달)**
- 미국 교구 3곳(4-3·4-4·4-5)은 모두 **Verso Ministries**, 파라마타는 **Harvest Journeys**가 운영한다. 지상 수배 결정권은 교구보다 이 운영사에 있을 가능성이 크다. 운영사를 리드에 넣을지(공식 채널만) 지후가 판단. 나는 연락처를 모으지 않았다.
- 교구에 보내는 메일은 "운영사를 대체"가 아니라 "자유일·연장일 보완"으로만 쓴다. 기대 매출은 작다(1일 모듈).

---

## 4. 개인 고객 유입 최소 운영 계획 (③) — 이번 주 게시 3건 초안

가설: 지금 시기에 맞는 실용 정보(단풍 막바지, 귤 따기 제철, 스키 개장 전)를 주면 저장·클릭이 생긴다. Reddit은 링크 없이 답만 줘서 신뢰를 쌓는다.
측정: Pinterest 저장·외부 클릭, Instagram 저장·프로필 링크 클릭, Reddit 추천·댓글. 사이트 측은 해당 가이드 페이지뷰(전주 대비).
규칙: 상품 판매·"book now" 문구 없음(결제 구조·Vercel 미정). 제휴 링크 없음. 사진은 **우리가 권리를 가진 이미지만**(없으면 텍스트 카드 디자인).

### 4-1. Pinterest (핀 1개) — 11/1(일) 게시안
- 링크: https://seoulmate-korea-iota.vercel.app/guides/seoul-autumn-foliage-2026-guide/
- 핀 제목: Seoul Autumn Leaves 2026: 6 Free Spots by Subway
- 설명:
```
Seoul's ginkgo trees usually peak from late October to mid-November. Six easy spots for first-time visitors,
all reachable by subway: Deoksugung Stonewall Road, Samcheong-dong Road, Changdeokgung Secret Garden
(guided tour only, book ahead), Namsan Park, Seoul Forest and Bukhansan. Most are free.
Tip: ginkgo leaves fall fast after rain or wind, so check the forecast.
#seoultravel #koreaautumn #seoulfall #koreatravel #ginkgo
```
- 이미지 문구(세로 1000×1500): "SEOUL AUTUMN LEAVES 2026 · 6 free spots by subway · peak: late Oct–mid Nov"
- 보드: "Korea in Autumn"

### 4-2. Instagram (캐러셀 5장) — 11/3(화) 게시안
- 주제: Jeju tangerine picking with kids (가이드: https://seoulmate-korea-iota.vercel.app/guides/jeju-tangerine-picking-kids/ — 인스타 본문 링크는 클릭이 안 되므로 "link in bio")
- 슬라이드:
  1. "Tangerine picking in Jeju 🍊 when to go"
  2. "Season: Oct–Jan. Fully orange from mid-November (October fruit is still greenish)"
  3. "Cost: about ₩5,000–20,000 per person. Open-field farms ~₩7,000–11,000 for 1–2 kg"
  4. "Jeju Citrus Expo: Nov 19–23, 2026, Seogwipo. Under 13 free"
  5. "Many farms take bookings only in Korean — ask your hotel to call. Full guide: link in bio"
- 캡션:
```
Planning Jeju with kids this November? Tangerine farms are one of the easiest family activities on the island.
Go after mid-November for the classic orange orchards, and pair Hueree Natural Park with the Citrus Expo
(both in Namwon) on the same day. Prices and hours change, so check with the farm before you go.
Full guide with three family-friendly farms → link in bio
#jeju #jejuisland #koreawithkids #familytravel #koreatravel #tangerine
```
- 확인: 가격·날짜는 가이드 본문 그대로. 게시 직전 Expo 공식 공지 재확인.

### 4-3. Reddit (r/koreatravel 답변형 글, **링크 없음**) — 11/5(목) 게시안
- 형식: 새 글보다 **기존 질문 스레드 답변**을 우선. 맞는 질문이 없으면 아래 정보 글. 서브레딧 규칙(자기 홍보·링크) 게시 직전 확인.
- 제목: Skiing near Seoul this winter (2026–27) — what I'd tell a first-timer
- 본문:
```
A few people have asked about skiing on a Seoul trip, so here's what's useful to know:

- Season: roughly late Nov/Dec to March. 2026–27 opening dates aren't announced yet (resorts usually confirm in November). Last season Phoenix opened Nov 21. Early-season snow is mostly machine-made; Jan–Feb is the most reliable.
- Closest: Konjiam (~1 hr from Seoul), fine for a half day or night skiing. Vivaldi Park (Hongcheon) is ~1.5 hrs.
- Olympic resorts: Yongpyong and Phoenix in Pyeongchang. KTX from Seoul Station to Jinbu (Odaesan) or Pyeongchang, then shuttle/taxi.
- Rental: every resort rents skis, boards and clothing. Bring your own gloves, goggles and layers to save money.
- Crowds: weekends and Korean school holidays (late Dec–Feb) are busy; weekdays are much quieter.
- Don't book non-refundable rooms for late November until your resort confirms its opening date.
- Pyeongchang often drops well below -10°C in January; heat packs are sold at every convenience store.

Happy to answer questions about getting there from Seoul.
```
- 고지: 계정 프로필에 Seoulmate 소속을 밝힌다(숨기지 않음). 본문에 링크·상호 없음. 누가 출처를 물으면 그때만 가이드 링크.

### 4-4. 이번 주 운영
| 날 | 할 일 | 담당 |
|---|---|---|
| 10/31(토) | 승인 결과 확인, 이미지 2종 제작(텍스트 카드) | 나래 |
| 11/1(일) | Pinterest 핀 게시 | 대표(승인 후) |
| 11/3(화) | Instagram 캐러셀 게시 | 대표(승인 후) |
| 11/5(목) | Reddit 답변/글 게시 | 대표(승인 후) |
| 11/7(토) | 3건 지표 기록 → 주간 보고 | 나래 |

키워드 중복 확인: 세 글 모두 사이트 내 다른 글과 주제가 겹치지 않는다(서울 단풍 1건, 제주 귤 1건, 스키 1건).

---

## 5. 성과 지표와 2주 일정

### 5-1. 지표 (1차 10곳 + SNS 3건)
| 지표 | 정의 | 목표(2주) | 근거 |
|---|---|---|---|
| 발송 수 | 1차 메일/폼 접수 건 | 10 | A 상위 10 |
| 회신율 | 사람 회신 ÷ 발송 (자동응답 제외, "no thanks" 포함) | **20% 이상(2건+)** | 개인화 콜드 메일 일반 범위 추정 — 근거 수치 없음, 2주 뒤 실제로 보정 |
| 긍정 회신 | 정보·통화 요청 | 1~2건 | |
| 미팅 수 | 화상/전화 실시 | **1건 이상** | |
| 일정 초안 송부 | 무료 1안 발송 | 1건 | |
| 수신 거부 | 거부 요청 | 기록·1일 내 처리 100% | 규정 준수 지표 |
| 견적(제휴사 명의) | 여행사 견적 발송 | 0~1건 | P1 해결 시에만 |
| SNS | 3건 게시, 저장·클릭 합계 | 기준선 만들기(목표 없음) | 첫 게시라 비교 대상 없음 |
| 가이드 페이지뷰 | 단풍·귤·스키 3페이지 | 전주 대비 증가 여부 | 측정 도구 확인 필요(도윤) |

> 정직한 기대치: 2주 안에 **매출(입금)이 생길 가능성은 낮다.** B2B는 결정에 1~3개월(지후). 이 실험의 목적은 "회신·미팅이 생기는 메시지·분류가 무엇인지"를 찾는 것이다.

### 5-2. 2주 일정 (10/30 ~ 11/13)
| 날짜 | 할 일 | 담당 |
|---|---|---|
| 10/30(금) | 초안 완성, 승인 요청 | 나래 |
| 10/30~31 | 규리 문안 검토(P3·P4·개인정보 고지), 지후 채널 확인(P6) | 규리·지후 |
| ~11/1(일) | **대표 승인** + 제휴 여행사·발신 정보(P1·P2) 확정 | 대표 |
| 11/1 | Pinterest 게시 | 대표 |
| 11/2(월) | 1차 발송 10곳 (해외: 상대 현지 오전 시간대 / 국내: 공식 폼) | 대표 |
| 11/3(화) | Instagram 게시 | 대표 |
| 11/5(목) | Reddit 게시 | 대표 |
| 11/6(금) | 2차 후속(D+4), 회신 분류 | 나래 초안 · 대표 발송 |
| 11/7(토) | SNS 주간 지표 보고 | 나래 |
| 11/9~11 | 미팅 진행, 일정 초안 1안 송부(서아) | 대표·서아 |
| 11/12(목) | 3차 닫는 메일(D+10) | 대표 |
| 11/13(금) | 2주 결과 보고: 회신율·미팅·분류별 반응 → 다음 20곳 문안 수정 | 나래 |

### 5-3. 기록 방법
- 발송 기록 시트(로컬, `ops/marketing/` 아래, 승인 후 생성): 기관 · 분류 · 채널(폼/메일) · 1차/2차/3차 날짜 · 회신 여부 · 수신 거부 여부 · 다음 행동. **개인 이름·개인 메일은 적지 않는다**(기관 공식 채널명만).

---

## 6. 승인 요청 내용
- 행동: B2B 소개 메일 1차 발송(우선순위 A 10곳, Georgian Court는 EdUHK로 대체 가능) 및 이번 주 SNS 게시 3건(Pinterest·Instagram·Reddit)
- 조건: P1(제휴 여행사 확정)·P2(발신 정보)·P3/P4(규리 검토) 충족 전에는 B2B 발송 안 함. SNS 3건은 P1과 무관하게 진행 가능(상품 언급 없음).
- 위험도: 보통 — 외부 연락·게시, 스팸 규정, 실체 없는 제휴 표기 위험. 문안에서 과장·허위·운영 주체 오인 표현을 뺐다.

## 출처 (조회일 2026-10-30)
- https://parracatholic.org/celebrate/wyd/seoul2027/
- https://www.archbalt.org/wp-content/uploads/2026/04/Archdiocese-of-Baltimore_Seoul_WYD2027_Flyer-1.pdf
- https://fwdioc.org/Youth-Young-Adult-WYD-Seoul-Flyer-Aug-1-Aug-10-2027.pdf
- https://sdcatholic.org/wp-content/uploads/2026/04/WYD-FAQ-Flyer.pdf
- https://campusministry.acu.edu.au/whats-on/world-youth-day-2027 (403, 검색 요약으로 확인)
- https://www.wydseoul.org/en/news/faq (본문 미표시) · https://www.asianews.it/en/east-asia/south-korea/seoul-2027-world-youth-day-international-registrations-open-from-late-october (지후 출처)
- https://www.stonybrook.edu/korean/opportunities/summer-study-abroad.html
- https://globalengagement.mercer.edu/global-education/facultyledprograms/spring-break-in-south-korea-pol/
- https://georgian.edu/study-abroad/faculty-led-study-abroad-programs/south-korea-k-culture-k-sports-amp-k-education/ (→ https://georgian.edu/global-education/ 리디렉트)
- https://www.eduhk.hk/lml/modern-language-learning/study-tours/korea-study-tour-2026
- https://www.nctasia.org/course/study-tour-south-korea/
- 사이트 가이드: /guides/seoul-autumn-foliage-2026-guide/, /guides/jeju-tangerine-picking-kids/, /guides/skiing-in-korea-2026-27-resorts-near-seoul/ (모두 HTTP 200 확인)
- 규정 언급(정보통신망법 제50조·제50조의2, CAN-SPAM, 호주 Spam Act 2003, 홍콩 UEMO)은 나래의 일반 이해이며 **규리 확인 전 결론 아님**.

---
[나래 · 마케팅 보고] B2B 아웃리치 초안 + 이번 주 SNS 초안
제안/결과: 분류별 템플릿 5종(국내판 포함)·후속 2회, A 상위 10곳 개인화 첫 줄(근거 URL), 표현 규칙, SNS 3건, 지표·2주 일정
지표: 기준선 없음(첫 발송) → 2주 목표 회신율 20%+, 미팅 1건+
문구·초안 위치: ops/marketing/2026-10-30_B2B-아웃리치-초안.md
승인 요청: 이 보고와 함께 요청

