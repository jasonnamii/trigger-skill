---
name: trigger-skill
description: 트리거 라우터 + glossary lazy-load 엔진 v2.2 Flash-Router. UP §도구우선게이트(Flash)에서 메시지 grep 후 hit ≥ 1 시 호출됨. args=트리거명 → references/glossary/{name}.md 단일 Read (~50토큰). 콤보 args → 구성 트리거 다발 Read. 32 정식명 + 10 콤보 verbatim. 핑퐁·리허설·작업계획 컨펌게이트 우선권. P1: 트리거발동, 트리거사전, 트리거스킬, trigger skill, hard-fire, 강제발동, 정식명사전, 글로서리게이트, 발동게이트, hit판정, 32정식명, 10콤보, 홈즈, 오컴, 제1원리, 베이지안, 엄브렐러, 아날로지, 연역수렴, 외과적, 수정4, 백본, 스켈레톤, SHE, 엘베피치, 타임스톤, 맥가이버, 넛지, 프리모르템, 트리아지, 줌, 절대자, 틀밖, 부작업, 주작업, 제출청소, 작업설계자, 핑퐁, 리허설, 작업계획, 복기, 이해당사자맵, 신뢰구간, 미궁, 마비, 시야, 벽, 카드없음, 장밋빛폭주, 제출직전, 복잡계, 박스, 복기방. P2: 발동해줘, 트리거 잡아, fire trigger, lookup definition, 정의 가져와. P3: trigger detection, deterministic invocation, hard-fire gate, glossary verbatim, args router, lazy load, flash router. P4: UP §도구우선게이트 grep hit ≥ 1 시. P5: 헤더 silent, 정의 verbatim 인용, 1줄 자연 융합. NOT: TRIZ·트리즈→triz / 이쁘니→design-skill.
license: Proprietary
---

# 트리거 스킬 v2.2 Flash-Router — Lazy Glossary

> **목표 = 발동 100% + verbatim · 호출당 ~80토큰.** UP §도구우선게이트(Flash)가 메시지 grep으로 hit 판정·invoke 강제. 본 스킬은 args 라우터 — args의 트리거명에 해당하는 단일 glossary 파일만 lazy-load.

> **핵심 키워드:** 트리거발동·트리거사전·트리거스킬·hard-fire·정식명사전·글로서리게이트·발동게이트·hit판정 — 메시지 등장 시 UP grep이 본 스킬 호출.

---

## §A. INVARIANT (3개)

### Rule 1 — Silent
헤더·박스·자기선언 출력 ✗. 본문 1줄 자연 융합.

### Rule 2 — Verbatim
응답에 로드된 glossary 파일의 정의·절차 키워드 ≥ 2개 verbatim 포함. "즉석·일반·대충" 일반추론 표현 ✗.

### Rule 3 — 컨펌게이트 우선권
핑퐁·리허설·작업계획 hit = 본실행(편집·생성·적용·INIT) 전 5단계 출력 → 컨펌 대기. "완성형 입력이라 OK"·"명령형 동사 우선" 자기합리화 = FAIL.

---

## §B. ROUTER — args → 단일 파일

### B-1. 정식명 32개 라우팅

args가 다음 중 하나면 `references/glossary/{args}.md` Read 1회:

```
홈즈 · 오컴 · 제1원리 · 베이지안 · 엄브렐러 · 아날로지 · 연역수렴
외과적 · 백본 · 스켈레톤 · SHE · 엘베피치 · 타임스톤
맥가이버 · 넛지 · 제출청소 · 작업설계자
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
- TRIZ / triz / 트리즈 → triz 스킬 (본 스킬 §B 적용 ✗)
- 이쁘니 → design-skill
- "트리거"·"스킬"·"엔진" 단독 → 일반명사 마스킹

---

## §C. 자체점검 (송출 직전 2항)

| # | 체크 | 위반 |
|---|------|------|
| 1 | 컨펌게이트(핑퐁·리허설·작업계획) hit인데 본실행 시작? | YES → 응답 폐기·5단계로 복귀 |
| 2 | 로드된 glossary 정의 키워드 ≥ 2개 verbatim 인용? | NO → 보강 |

UP §도구우선게이트가 0차 방어(grep·invoke), §C는 1차 방어(컨펌·verbatim).

---

## §D. References

- `references/glossary/{name}.md` — 32정식명 단위 정의 (라우터 타깃)
- `references/glossary/콤보-{name}.md` — 10콤보 구성 (라우터 타깃)
- `references/triggers-glossary.md` — 마스터 (B-3 폴백·백업)
- `references/protocol-cleanup.md` — 제출청소 13축 풀버전
- `references/protocol-designer.md` — 작업설계자 7단계 풀버전
- `references/protocol-edit4.md` — 수정4 L0~L4 풀버전

---

## §E. 미발동 신고
- 경로: `VAULT/Agent-Ops/_autoloop-lab/trigger-skill/changelog.md`
- 포맷: `YYYY-MM-DD · 누락트리거 · 메시지요약 · 원인추정`
- B-3 폴백 사용 시도 같은 포맷으로 기록

---

## Gotchas

| 함정 | 대응 |
|------|------|
| **UP grep 누락** | UP §도구우선게이트 CHECK가 응답 폐기. 본 스킬은 grep 후 호출됨 |
| **호출됐는데 silent 위반** | Rule 1 = 헤더·박스 출력 ✗. 본문 1줄 자연 융합 |
| **정의 일반추론 (글로서리 우회)** | Rule 2 = 로드된 파일 verbatim. 키워드 ≥ 2개 인용 |
| **컨펌게이트 hit인데 INIT 직행** | Rule 3 = 핑퐁·리허설·작업계획 5단계 먼저 |
| **args 미전달 환경** | §B-3 폴백 = 마스터 풀로드. changelog 기록 |
| **콤보 단일 Read 실수** | 콤보는 Read N+1회 (콤보 파일 + 구성 트리거 N개). 단일 Read = FAIL |
| **NOT 라우팅 무시** | TRIZ·이쁘니는 라우팅. 본 스킬 §B 적용 ✗ |
| **glossary 파일 누락·오타** | Read 실패 → §B-3 폴백. 누락은 SKILL 수정 사유 |

---

## §F. 헤리티지

- v1.0 — 강제발동 + glossary Read (references 풀로드)
- v2.0 Flash — UP grep + inline glossary 박제 (~1700토큰/호출, Read 0회)
- v2.1 Flash-Router (2026-04-28) — args 라우팅으로 lazy-load 복귀. 호출당 ~250토큰 (v2.0 대비 -85%)
- **v2.2 Vector-Sharp (2026-05-01)** — 28+9 → 32+10. 수정 6 (오컴·트리아지·아날로지·넛지·줌·엘베피치·베이지안·백본 발동조건+산출물 강제 박제) · 강화 5 (홈즈복기모드·틀밖종료문·수정4 L정의·작업설계자결재포인트·트리아지분배비율) · 신설 4 (복기·이해당사자맵·신뢰구간·콤보-복기방). 사각 메우기 + UP DNA·paper-engine 중복 해소.

**v2.2 변이 동기:** 형 피드백 — "트리거 정의가 일반 단어 수준이면 트리거가 필요 없어. 벡터가 뚜렷해야 함." → 6수정·5강화·4신설로 발동조건·산출물 강제, 사각(복기·이해충돌·신뢰구간) 메움.
