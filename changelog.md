# trigger-skill autoloop changelog

**날짜:** 2026-04-27
**모드:** turbo (α=1.0, auto_scorable 100%)
**iteration 수:** 3 (변이 1 + 안정성 검증 2)
**최종 점수:** 40/40 (100.0%) · baseline 대비 +18.2pt

---

## baseline

| 메트릭 | 값 |
|--------|-----|
| eval cases | 22 |
| auto_scorable | 22/22 (α=1.0) |
| baseline pass | **18/22 (81.8%)** |
| 실패 케이스 | C01·C02·C03·C04 (콤보 4종 전부) |
| 원인 | scanner의 COMBOS phrases에 콤보명 단독 미등록 |

## iter1 — keep ✅

**변이 가설:** 콤보명("미궁", "마비", "박스", "장밋빛폭주", "제출직전", "복잡계", "시야", "벽", "카드없음")이 사용자 메시지에 등장해도 hit 0건. SKILL.md §2 콤보 테이블에는 "미궁이야·미궁 상태" 같은 결합 예시가 박혀있는데 scanner가 이를 못 잡음.

**수정:** `scripts/trigger_scanner.py` 의 `COMBOS` 리스트에서 각 콤보의 phrases 배열 첫 항목으로 콤보명 자체를 추가.

```python
("미궁", ["백본","제1원리"], ["미궁","근본원리","근본적","본질적"], ["박스","복잡계"]),
("마비", ["트리아지","홈즈"], ["마비"], ["장밋빛폭주","카드없음"]),
("박스", ["틀밖","제1원리"], ["박스","다시 생각","다시생각","처음부터 다시"], ["미궁","시야"]),
# ... 9개 콤보 전부
```

**결과:** 22/22 (100%) · +18.2pt · 단일 변이 = 단일 가설 = 단일 eval 타겟 (콤보 hit) 만족.

## iter2 — 안정성 검증 (+10 cases)

부정문(`백본 안 잡았어`)·복수 트리거(`백본 잡고 제1원리까지`)·NOT 라우팅(`트리즈 발동`)·인용(`어제 절대자 언급함`)·영문(`ping pong 가자`·`dry-run 돌려`) 등 10개 추가.

**결과:** 32/32 (100%) — 변이 1이 edge case에서도 견고.

## iter3 — 안정성 검증 (+8 cases)

일반명사 마스킹(`트리거 정의가 뭐야`)·콤보+조사(`미궁이 깊다`·`박스를 깨자`)·멀티 트리거(`줌 아웃하고 절대자로`)·영문(`EDIT4로 수정`)·픽션 캐릭터(`맥가이버는 천재야`) 등 8개 추가.

**결과:** 40/40 (100%) — 3회 연속 95%+ pass, 자동 종료 조건 도달.

---

## 산출물

- `scripts/trigger_scanner.py` — 콤보명 단독 hit 지원 (변이 1)
- `evals/cases.json` — 40 cases (positive 10 + fiction 3 + combo 4 + negative 5 + edge 10 + hard 8)
- `scripts/score.py` — auto_scorable 채점기
- `_results/baseline.txt` · `iter1.txt` · `iter2.txt` · `iter3.txt`
- `_results/results.tsv` — iteration 추이

## SKILL.md 변경

**변경 없음.** 변이는 scanner 코드 한 곳만. SKILL.md 본문은 이미 콤보 단독 hit을 의도하고 작성됨 (§2 콤보 테이블의 "미궁이야·미궁 상태" 예시) → scanner가 SKILL.md 의도를 따라가는 형태로 정렬됨.

## Gotchas (autoloop 부산물)

- baseline 81.8% 원인이 SKILL.md가 아니라 scanner였음 — eval로 들어가지 않으면 발견 불가능했던 결함.
- turbo 모드(α=1.0)는 변이 1회로 100% 도달 후 안정성 검증 2회로 충분.
- 복합 변이(SKILL.md + scanner 동시 수정)였으면 귀인 불가 → 단일 변이 원칙이 먹혔다.
