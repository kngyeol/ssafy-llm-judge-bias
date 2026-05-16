# LogicKor 적용 — 한국어 멀티턴에서는 결과가 달라진다

> v1/v2/v3 모두 본인 자작 챌린지 50개로 진행. 이번엔 한국어 LLM 평가 표준 벤치마크 [**LogicKor**](https://github.com/instructkr/LogicKor)의 42 entries × 2 turns = 84 판정으로 같은 도구를 돌렸다.

## 1. Setup 차이

| 항목 | v1~v3 (자작 50) | LogicKor |
|---|---|---|
| 챌린지 출처 | 본인 작성 | instructkr/LogicKor (한국어 LLM 평가 표준) |
| 단위 | 단일 턴 | **2턴 멀티턴** (Q1 → Q2가 Q1 답변을 참조) |
| 카테고리 | code/writing/reasoning/creative/korean | 추론/수학/글쓰기/코딩/이해/문법 |
| 라이센스 | MIT (본인) | LogicKor 라이센스 |
| 평가 단위 | 50 라운드 | 84 판정 (42 × 2턴) |

Fighter는 v1과 동일: **GPT-5.2 vs Claude-Opus-4.5**, 심판도 동일: **GPT-5 / Claude-Sonnet-4.5 / Gemini-2.5-Flash**.

## 2. 전체 결과

| Judge | A승 | B승 | TIE | ERR | A승률 (TIE 제외) |
|---|---|---|---|---|---|
| **GPT-5** | 47 | 12 | 25 | 0 | **80%** |
| Claude-Sonnet | 34 | 16 | 34 | 0 | 68% |
| **Gemini-Flash** | 31 | 49 | 3 | 1 | **39%** |

v1 자작 챌린지와 정반대 패턴이 등장:

| | v1 자작 (A승률) | LogicKor (A승률) | 변화 |
|---|---|---|---|
| GPT-5 심판 | 72% | 80% | +8pp |
| Claude-Sonnet | 42% | 68% | **+26pp** |
| Gemini-Flash | 58% | **39%** | **-19pp** |

**Claude 심판은 LogicKor에서 GPT를 훨씬 더 좋아하고, Gemini는 정반대로 Claude 손을 들었다.** 같은 모델 쌍, 같은 심판인데 챌린지 출처만 바꿔도 결과가 이렇게 다르다.

## 3. 카테고리별 — 진짜 알맹이

| Category | GPT-5 (A) | Claude (A) | Gemini (A) | 평균 | 해석 |
|---|---|---|---|---|---|
| **수학** | 1/14 (7%) | 1/14 (7%) | 3/14 (21%) | **12%** | **Claude 압승 만장일치** |
| **문법** | 4/14 (29%) | 4/14 (29%) | 2/14 (14%) | 24% | Claude 우세 만장일치 |
| **추론** | 7/14 (50%) | 5/14 (36%) | 9/14 (64%) | 50% | 평균 호각, 심판별 분산 |
| **코딩** | **13/14 (93%)** | 5/14 (36%) | **2/14 (14%)** | 48% | **family bias 폭발 — 79%p 격차** |
| **이해** | 9/14 (64%) | 9/14 (64%) | 7/14 (50%) | 59% | GPT 약간 우세, 비교적 일관 |
| **글쓰기** | 13/14 (93%) | 10/14 (71%) | 8/14 (62%) | 75% | GPT 우세 만장일치 |

### 3.1 수학 (가장 큰 만장일치)

심판 3개가 모두 Claude 손을 들어주는 영역. **GPT-5 본인도 자기 family 답을 7%만 선택**. v2 self-judge에서 발견한 "객관적 형식 위반 앞에선 self-bias 사라짐" 패턴과 일치 — 수학은 정답이 명확하니까 family bias가 통하지 않음.

이건 Claude-Opus가 실제로 한국어 수학에서 GPT-5.2보다 낫다는 신호일 가능성 높음. 단, **계산 검증을 하지는 않았음 — Claude가 정답을 더 잘 맞췄는지, 단지 더 잘 설명했는지는 불분명.**

### 3.2 코딩 — Family bias 극단

GPT-5 심판: 13/14 (93%) → 자기 family 압도적
Claude 심판: 5/14 (36%) → 자기 family Claude 손
**Gemini 심판: 2/14 (14%)** → Claude 압도적 손
**격차: 79%p**

이건 v1·v2에서 본 가장 큰 family bias보다 더 극단적이다 (v1 자작 GPT vs Claude 심판 = 30%p). 한국어 코딩 챌린지가 family bias를 가장 잘 드러내는 영역이라는 시사.

가설: 코딩 평가는 "스타일·관례·assumption" 같은 주관적 차원이 많아서 심판이 자기 모델의 코딩 스타일을 정상으로 보는 경향이 강할 수 있음. 수학과 달리 "객관적 정답" 검증이 어려운 코드 (예: API 디자인, 변수 네이밍, 에러 핸들링 스타일)에서 심판은 자기 family의 관습을 따른 답을 선호.

### 3.3 글쓰기 — GPT 만장일치 우위

수학과 정반대로 모든 심판이 GPT 우위(62-93%). 한국어 글쓰기에선 GPT-5.2가 실제 더 좋다는 신호일 수도, 또는 LogicKor 글쓰기 챌린지가 GPT 스타일을 선호하는 평가축으로 설계됐을 수도.

### 3.4 문법 — Claude 우위 만장일치

한국어 문법 카테고리는 LogicKor에만 있는 특화 영역. 세 심판 모두 GPT를 14-29%만 선택 → Claude-Opus가 한국어 문법 처리에서 강세.

## 4. Turn 1 vs Turn 2 — GPT가 멀티턴에서 강해진다

| Judge | Turn 1 A승 | Turn 2 A승 | 증감 |
|---|---|---|---|
| GPT-5 | 19/42 (45%) | **28/42 (67%)** | **+22pp** |
| Claude-Sonnet | 17/42 (40%) | 17/42 (40%) | 0pp |
| Gemini-Flash | 13/42 (31%) | 18/41 (44%) | +13pp |

**GPT-5 심판은 Turn 2에서 GPT-5.2 선호가 폭증.** Turn 1에서 45%였던 게 Turn 2에서 67%로 22%p 점프.

해석 가설 2가지:
1. **GPT-5.2가 실제 multi-turn 일관성이 더 좋음** — Turn 2가 Turn 1을 잘 받쳐줘서 GPT-5 심판(같은 family라 그런 일관성을 잘 인지)이 가산점
2. **GPT-5 심판이 멀티턴 평가에서 더 family-biased** — Turn 2 평가가 Turn 1 컨텍스트를 보면서 자기 family 스타일을 추가로 인식

Claude 심판은 Turn 1/Turn 2 동일 비율 → 멀티턴에 흔들리지 않음 (또는 멀티턴 정보를 활용 못 함).

## 5. LogicKor 공식 리더보드와의 비교

LogicKor 공식 평가는 **단일 모델 1~10점 scoring** (MT-Bench 방식)이지 본 프로젝트의 pairwise A/B/TIE가 아님. 따라서 점수 직접 비교 불가.

다만 다음은 알 수 있음:
- LogicKor 리더보드에서 Claude-Opus 시리즈와 GPT 시리즈는 항상 상위권에서 박빙
- 본 결과의 평균 (대략 A승률 60% 근처)는 "박빙이지만 GPT가 약간 우위" 정도로 LogicKor 평균 점수 흐름과 합치

## 6. v1~v3 + LogicKor 종합 — 4번 측정한 결론

| 측정 | A승률 (GPT-5.2) | n | 비고 |
|---|---|---|---|
| v1 자작 (3 심판 평균) | 57% | 50 | 자작 챌린지 |
| v3 human (인간 1명) | 39% | 50 | ground truth |
| LogicKor (3 심판 평균) | 62% | 84 | 표준 한국어 벤치마크 |

세 setup의 결과가 흩어진다 (39%~62%). **결국 "GPT-5.2 vs Claude-Opus" 같은 단순 비교조차도 챌린지셋과 채점 방식에 의해 크게 좌우된다는 게 가장 견고한 결론.** 어느 한 setup의 결과만 보고 "X가 Y보다 낫다"고 단정짓는 건 위험.

## 7. 한계

- **Multi-turn judging은 단일 prompt** — 두 턴을 보고 한 번에 판정. 턴별 가중치 미분리.
- **Reference 답변 미활용** — LogicKor entries 일부는 `references` 필드에 정답 후보 있으나 본 평가에선 사용 안 함. Reference 사용하면 평가 더 객관적.
- **Single seed, 1 trial** — 같은 챌린지를 여러 번 돌려 분산 측정 안 함.
- **LogicKor 1차 데이터 archived** — repo가 archived(2024-10-17)라 챌린지셋 업데이트 가능성 낮음. 새로운 한국어 평가셋으로 옮길 시점 가까움.

## 8. 데이터 위치

- 답변: `results/logickor_fights/{01-42}.json` (각 entry 2턴 × 2 fighter)
- 심판 결과:
  - `results/logickor_judge_*_logickor-gpt5/` (GPT-5)
  - `results/logickor_judge_*_logickor-claude/` (Claude-Sonnet)
  - `results/logickor_judge_*_logickor-gemini/` (Gemini-Flash)
- 각 결과 디렉토리에 `_results.json` (집계) + `{id:02d}.md` (양 답변 + 심판 코멘트)

## 9. 다음에 할 만한 것

1. **LogicKor에 v3 human baseline 적용** — 42 entries × 2턴이라 35-40분 정도. v3 human_baseline.py 약간 수정 필요 (멀티턴 표시).
2. **Reference 기반 자동 채점** — `references` 필드 있는 entries만 분리해서 정답 일치도 평가.
3. **LogicKor 공식 single-model scoring 방식 추가** — pairwise 외에 1-10점 scoring도 돌려서 두 방식 일관성 비교.
4. **2-trial 분산 측정** — 같은 setup 두 번 돌려서 우연 효과 측정.
