---
name: trigger-skill
description: v2.3 Active-Fire. 다음 트리거 단어가 메시지에 **하나라도 등장 시 즉시 발동**=`references/glossary/{name}.md` Read 1회→verbatim 인용→1줄 자연 융합. 미발동=TOP-LEVEL FAIL. **정식명 31**: 홈즈·오컴·제1원리·베이지안·엄브렐러·아날로지·연역수렴·외과적·백본·스켈레톤·SHE·엘베피치·타임스톤·맥가이버·넛지·프리모르템·트리아지·줌·절대자·틀밖·부작업·주작업·수정4·복기·이해당사자맵·신뢰구간·작업설계자·핑퐁·리허설·작업계획. **콤보 10** (콤보-{name}.md+구성 다발 Read·순서=관점→분석→구조→판단→실행): 미궁·마비·시야·벽·카드없음·장밋빛폭주·제출직전·복잡계·박스·복기방. 핑퐁·리허설·작업계획 hit=본실행 전 컨펌게이트 5단계 필수. P1: 트리거발동, 트리거사전, 트리거스킬, trigger skill, hard-fire, 강제발동, 글로서리게이트, hit판정, 홈즈, 오컴, 제1원리, 베이지안, 엄브렐러, 아날로지, 연역수렴, 외과적, 수정4, 백본, 스켈레톤, SHE, 엘베피치, 타임스톤, 맥가이버, 넛지, 프리모르템, 트리아지, 줌, 절대자, 틀밖, 부작업, 주작업, 작업설계자, 핑퐁, 리허설, 작업계획, 복기, 이해당사자맵, 신뢰구간, 미궁, 마비, 시야, 벽, 카드없음, 장밋빛폭주, 제출직전, 복잡계, 박스, 복기방. P2: 발동해줘, 트리거 잡아, 트리거로 봐, 정의 가져와, fire trigger, apply trigger. P3: deterministic invocation, hard-fire gate, active fire, mandatory invocation. P4: 31정식명·10콤보 등장 즉시 자동 발동. P5: silent, verbatim, 1줄 융합. NOT: TRIZ→triz-skill / 이쁘니→design-skill / 제출청소·14축·AI박멸·휴머나이즈·외부송출·submission cleanup→submission-cleanup 스킬 / 일반명사 "트리거" 단독→마스킹.
license: Proprietary
---

# 트리거 스킬 v2.3 Active-Fire — Lazy Glossary

> **목표 = 발동 100% + verbatim · 호출당 ~80토큰.** description 능동 명령형으로 Claude 자율발동 + UP §도구우선게이트(Flash) grep 이중 안전망. 본 스킬은 args 라우터 — args의 트리거명에 해당하는 단일 glossary 파일만 lazy-load.

> **핵심 키워드:** 트리거발동·트리거사전·트리거스킬·hard-fire·정식명사전·글로서리게이트·발동게이트·hit판정 — 메시지 등장 시 무조건 자동 발동.

---

## §A. INVARIANT (4개)

### Rule 0 — Active-Fire (능동 발동 의무)
description의 31정식명·10콤보 트리거 단어가 메시지에 **하나라도** 등장하면 Claude는 **즉시 자동 발동**한다. UP 게이트 호출을 기다리지 않는다. args 누락 시 메시지에서 트리거명 자체추출 → `references/glossary/{name}.md` Read. **미발동 = TOP-LEVEL FAIL** → 응답 폐기·재시작.

### Rule 1 — Silent
헤더·박스·자기선언 출력 ✗. 본문 1줄 자연 융합.

### Rule 2 — Verbatim
응답에 로드된 glossary 파일의 정의·절차 키워드 ≥ 2개 verbatim 포함. "즉석·일반·대충" 일반추론 표현 ✗.

### Rule 3 — 컨펌게이트 우선권
핑퐁·리허설·작업계획 hit = 본실행(편집·생성·적용·INIT) 전 5단계 출력 → 컨펌 대기. "완성형 입력이라 OK"·"명령형 동사 우선" 자기합리화 = FAIL.

---

## §B. ROUTER — args → 단일 파일

### B-1. 정식명 31개 라우팅

args가 다음 중 하나면 `references/glossary/{args}.md` Read 1회:

```
홈즈 · 오컴 · 제1원리 · 베이지안 · 엄브렐러 · 아날로지 · 연역수렴
외과적 · 백본 · 스켈레톤 · SHE · 엘베피치 · 타임스톤
맥가이버 · 넛지 · 작업설계자
프리모르템 · 트리아지 · 핑퐁 · 리허설 · 작업계획
줌 · 절대자 · 틀밖
부작업 · 주작업 · 수정4
복기 · 이해당사자맵 · 신뢰구간
```

### B-2. 콤보 10개 라우팅

args가 콤보명이면 `references/glossary/콤보-{args}.md` Read → 구성 트리거 추출 → 각 구성 트리거 `references/glossary/{name}.md` 다발 Read:

```
미궁 · 마비 · 시야 · 벽 · 카드없음 · 장밋빛폭주 · 제출직전 · 복잡계 · 박스 · 복기방
```

콤보 복합 순서: 관점 → 분석 → 구조 → 판단 → 실행

### B-3. args 미전달·매칭 실패 폴백

args 누락 OR 사전에 없는 토큰 → `references/triggers-glossary.md` 마스터 Read (구버전 풀로드). 폴백 사용 시 changelog 1줄 기록.

### B-4. NOT 라우팅
- TRIZ / triz-skill / 트리즈 → triz-skill 스킬 (본 스킬 §B 적용 ✗)
- 이쁘니 → design-skill
- 제출청소 / 14축 / AI박멸 / 휴머나이즈 / 외부송출 / submission cleanup → **submission-cleanup 스킬** (본 스킬 §B 적용 ✗·자산 이전 완료)
- "트리거"·"스킬"·"엔진" 단독 → 일반명사 마스킹

---

## §C. 자체점검 (송출 직전 3항)

| # | 체크 | 위반 |
|---|------|------|
| 0 | 메시지에 31정식명·10콤보 단어 hit인데 glossary Read 0회? | YES → 응답 폐기·Read 후 재작성 |
| 1 | 컨펌게이트(핑퐁·리허설·작업계획) hit인데 본실행 시작? | YES → 응답 폐기·5단계로 복귀 |
| 2 | 로드된 glossary 정의 키워드 ≥ 2개 verbatim 인용? | NO → 보강 |

Claude 자율발동(Rule 0)이 0차 방어, UP §도구우선게이트가 0.5차(이중 안전망), §C는 1차 방어(자체점검).

---

## §D. References

- `references/glossary/{name}.md` — 31정식명 단위 정의 (라우터 타깃)
- `references/glossary/콤보-{name}.md` — 10콤보 구성 (라우터 타깃)
- `references/triggers-glossary.md` — 마스터 (B-3 폴백·백업)
- `references/protocol-designer.md` — 작업설계자 7단계 풀버전
- `references/protocol-edit4.md` — 수정4 L0~L4 풀버전
- (제출청소 자산은 **submission-cleanup 스킬**로 이전 — `submission-cleanup/references/ai-not-canon.md`·`protocol-cleanup.md`·`scripts/cleanup_scanner.py`)

---

## §E. 미발동 신고
- 경로: `VAULT/Agent-Ops/_autoloop-lab/trigger-skill/changelog.md`
- 포맷: `YYYY-MM-DD · 누락트리거 · 메시지요약 · 원인추정`
- B-3 폴백 사용 시도 같은 포맷으로 기록

---

## Gotchas

| 함정 | 대응 |
|------|------|
| **UP grep 누락 / Claude 자율발동 실패** | Rule 0 Active-Fire — description 31+10 단어 등장 시 즉시 발동. UP 게이트는 이중 안전망일 뿐 |
| **호출됐는데 silent 위반** | Rule 1 = 헤더·박스 출력 ✗. 본문 1줄 자연 융합 |
| **정의 일반추론 (글로서리 우회)** | Rule 2 = 로드된 파일 verbatim. 키워드 ≥ 2개 인용 |
| **컨펌게이트 hit인데 INIT 직행** | Rule 3 = 핑퐁·리허설·작업계획 5단계 먼저 |
| **args 미전달 환경** | 메시지에서 트리거명 자체추출 → 단일 Read. 폴백은 §B-3 (마스터 풀로드) |
| **콤보 단일 Read 실수** | 콤보는 Read N+1회 (콤보 파일 + 구성 트리거 N개). 단일 Read = FAIL |
| **NOT 라우팅 무시** | TRIZ·이쁘니는 라우팅. 본 스킬 §B 적용 ✗ |
| **glossary 파일 누락·오타** | Read 실패 → §B-3 폴백. 누락은 SKILL 수정 사유 |

**❌WRONG / ✅CORRECT — 능동 발동 vs 수동 대기**

❌ WRONG: 형이 "홈즈로 봐줘"라고 적었는데 Claude가 "UP 게이트가 호출 안 했네"라며 자율판단으로 일반추론 응답. 트리거 정의 Read 0회.

✅ CORRECT: "홈즈" 단어 hit 즉시 `references/glossary/홈즈.md` Read 1회 → 정의 verbatim 키워드 2개 이상 인용 → 본문 1줄 자연 융합. UP 게이트 호출 여부 무관.

---

## §F. 헤리티지

- v1.0 — 강제발동 + glossary Read (references 풀로드)
- v2.0 Flash — UP grep + inline glossary 박제 (~1700토큰/호출, Read 0회)
- v2.1 Flash-Router (2026-04-28) — args 라우팅으로 lazy-load 복귀. 호출당 ~250토큰 (v2.0 대비 -85%)
- v2.2 Vector-Sharp (2026-05-01) — 28+9 → 32+10. 수정 6·강화 5·신설 4. 사각 메우기 + UP DNA·shaper-skill 중복 해소.
- **v2.3 Active-Fire (2026-05-03)** — description 수동태("호출됨") → 능동 명령형("반드시 즉시 발동") 전환. Rule 0 Active-Fire 신설 = Claude 자율발동 의무화. UP 게이트는 이중 안전망으로 격하. P2·P3 어휘 확장(트리거 발동·트리거로 봐·apply trigger 등). ❌WRONG/✅CORRECT 1쌍 박제. **변이 동기:** 형 피드백 — "발동이 너무 안돼. 대놓고 적어도 발동적용이 안돼." → 진단 결과 description이 수동 서술형이라 Claude가 자율판단으로 우회. 능동 명령형 전환으로 발동률 회복.

- **v2.5 Diet-Submission-Out (2026-05-04)** — 제출청소 자산 일체 → **submission-cleanup 스킬로 분리·이전**. 정식명 32→31. P1·§B-1·§B-4·§D 모두 갱신. `references/ai-not-canon.md`·`protocol-cleanup.md`·`scripts/cleanup_scanner.py` 삭제. `glossary/제출청소.md`는 라우팅 마커 1줄로 압축. 콤보-제출직전 갱신 (스켈레톤→submission-cleanup 호출). NOT 라우팅에 "제출청소·14축·AI박멸·휴머나이즈·외부송출·submission cleanup→submission-cleanup 스킬" 추가. **변이 동기:** 형 피드백 — "트리거 스킬에서 삭제하고 제출청소 스킬을 따로 만드는거야. 독립적으로. 그러면 더 강력하게 만들 수 있잖아." → 책임 직교성(verbatim 1줄 vs 14축 절차) 진단 → 분리. trigger-skill은 "단어→정의 1줄 융합" 본질로 다이어트.

- **v2.4 Cleanup-AI-Not (2026-05-04)** — 제출청소 13축 → 14축 확장. 축4 분리(모델명·생성흔적만) + 축14 신설(AI아님 종합·7서브슬롯: 미사여구·한자투·자신없는어미·것남용·강조부사·AI메타·AI사족). 정본 단일화: `references/ai-not-canon.md` 신규 — UP §L2·shaper-skill·trigger-skill 모두 본 정본 참조 (1뎁스 위임). `scripts/cleanup_scanner.py` 신규 (Python 스캐너·LLM 판단 0%·토큰 절감). **변이 동기:** 형 피드백 — "제출 청소를 확장하고 싶어. AI가 아닌 작업. 아주아주아주 철저하게 AI 아닌 문서." → 정본 흩어짐(UP·shaper·제출청소 각자) → 단일 정본 신규 + Python 스캐너로 결정주의 박멸.

**v2.2 변이 동기:** 형 피드백 — "트리거 정의가 일반 단어 수준이면 트리거가 필요 없어. 벡터가 뚜렷해야 함." → 6수정·5강화·4신설로 발동조건·산출물 강제, 사각(복기·이해충돌·신뢰구간) 메움.
