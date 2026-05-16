# LLM Judge Bias Benchmark (lightweight reproduction)

LLM-as-a-judge 평가 방식의 세 가지 편향(in-family bias, position bias, self-preference)을 **두 명의 fighter (GPT-5.2 vs Claude-Opus-4.5), 세 명의 LLM 심판 (GPT-5 / Claude-Sonnet-4.5 / Gemini-2.5-Flash), 한 명의 인간 평가자**의 채점 결과를 비교하여 직접 확인하는 재현 실험. 총 4가지 다른 setup에서 동일 모델 쌍을 측정.

> ⚠️ **본 프로젝트는 학술적 contribution이 아니라 lightweight reproduction이다.** 다루는 모든 현상은 [Prior Work](#prior-work)에서 더 엄밀하게 검증됨. 학술적 인용/응용은 원본 논문을 참조.

## Headline Finding — 같은 모델 쌍, setup만 다르게 측정해도 GPT-5.2 A승률이 39~80%로 흩어진다

4가지 setup에서 동일한 두 모델(GPT-5.2 vs Claude-Opus-4.5)을 측정:

| Setup | n | 평가자 | GPT-5.2 A승률 (TIE 제외) |
|---|---|---|---|
| **v3 human baseline** | 50 | 인간 1명 (라벨 가림) | **39%** |
| v1 자작 챌린지 | 50 | LLM 심판 3종 평균 | 57% |
| v1 (Claude-Sonnet 단일) | 50 | Claude-Sonnet | 42% |
| v1 (GPT-5 단일) | 50 | GPT-5 | **72%** |
| **LogicKor (표준 한국어 벤치마크)** | 84 (42×2턴) | LLM 심판 3종 평균 | **62%** |
| LogicKor (Gemini-Flash 단일) | 84 | Gemini-Flash | **39%** |
| LogicKor (GPT-5 단일) | 84 | GPT-5 | **80%** |

**결론**: 인간 한 명의 판정(39%)과 LLM 심판 한 종(GPT-5 = 72-80%)의 격차가 **33-41%p**. 챌린지셋·심판 모델·턴 구조를 바꾸면 *같은 모델 비교*조차 결과가 흩어진다. 단일 LLM 심판 결과 하나만 보고 모델을 비교하는 것은 신뢰할 수 없다.

## 핵심 발견 4가지 (cross-setup 종합)

### 1. In-family bias는 모델마다 비대칭이다

| 심판 | 자기 답 선호 | 회피 패턴 (TIE 비율) |
|---|---|---|
| GPT-5.2 self-judge | **64%** | 26% |
| Claude-Opus self-judge | **22%** | **48%** |

GPT는 자기 답을 적극 선호, Claude는 회피적 TIE에 가까움. 본 setup의 Claude-Sonnet 심판이 가장 인간(39%)과 가까운 42%를 보인 이유 중 하나.

### 2. Position bias는 심판마다 천차만별

A/B 위치 교체 후 결론 유지율:

| 심판 | 50판 중 일치 라운드 | 해석 |
|---|---|---|
| GPT-5 | **41/50 (82%)** | 위치 무관, 진짜 family bias |
| Claude-Sonnet | 36/50 (72%) | 약함 |
| Gemini-Flash | **29/50 (58%)** | 약 절반이 position bias |

### 3. 스타일은 표면일 뿐 — 깊은 시그널이 결정

답변을 상대 모델 스타일로 재작성 후 재채점한 결과, 세 심판 모두 v1과 거의 동일한 판정 유지. 심판이 보는 것은 표면 문체가 아닌 내용·구조·논리 시그널.

### 4. 카테고리별로 family bias 강도가 폭발할 수 있다

LogicKor 코딩 카테고리에서 같은 코드를 보고:
- GPT-5 심판: 93% A 선택
- Gemini-Flash 심판: 14% A 선택
- **격차 79%p** (전체 평균 격차의 두 배)

반면 수학 카테고리는 모든 심판이 7-21%만 A → 객관적 정답 영역에서는 family bias 약화 (Claude-Opus가 한국어 수학에서 실제 강세). **평가 영역의 객관성 수준에 따라 family bias 크기가 결정된다.**

### 보너스: 만장일치 오류의 비대칭

LLM 심판 3개가 *모두* 같은 답을 골랐지만 인간이 다른 답을 고른 라운드 9건 중 8건이 GPT 과대평가 방향. 무작위 오류가 아닌 체계적 편향 시사 (Panickssery 2024 self-preference 결과와 일관).

## Documents

| 파일 | 내용 |
|---|---|
| [`results/ANALYSIS.md`](results/ANALYSIS.md) | v1 — 3개 심판 기본 비교, 챌린지별 case study (4,200자) |
| [`results/ANALYSIS_v2.md`](results/ANALYSIS_v2.md) | v2 — Position swap / self-judge / stylometric 통제 실험 (5,500자) |
| [`results/ANALYSIS_v3_human.md`](results/ANALYSIS_v3_human.md) | v3 — 인간 ground truth 추가, 만장일치 오류 비대칭 (4,000자) |
| [`results/ANALYSIS_logickor.md`](results/ANALYSIS_logickor.md) | LogicKor 표준 벤치마크 적용, 카테고리별 격차 분석 (4,500자) |

총 약 **18,000자 분량 한국어 분석** + 4개 setup 134 판정 × 3-5 평가자의 raw 데이터 공개.

## Experimental Setup

### Fighter (두 setup 공통)

- **Fighter A**: `gpt-5.2`
- **Fighter B**: `claude-opus-4-5-20251101`

### LLM Judges (4 setup 모두 동일)

- `gpt-5`, `claude-sonnet-4-5-20250929`, `gemini-2.5-flash`

### Challenge Sets

| | 자작 (v1-v3) | LogicKor |
|---|---|---|
| Entries | 50 | 42 |
| 구조 | 단일 턴 | 2턴 멀티턴 |
| 카테고리 | code/writing/reasoning/creative/korean × 10 | 추론/수학/글쓰기/코딩/이해/문법 × 7 |
| 출처 | 본 repo (`challenges.json` + `challenges-extended.json`) | [instructkr/LogicKor](https://github.com/instructkr/LogicKor) |
| 평가 단위 | 50 라운드 | 84 판정 (42 × 2턴) |

### Human Baseline

자작 챌린지 50개에 대해 1명이 라벨 가린 채 직접 채점. LogicKor에는 미적용.

## Tools

| Script | Purpose | Cost / call |
|---|---|---|
| `gladiator.py` | Fighter 응답 생성 + 단일 턴 judge 실행 | fighter + judge |
| `replay_judge.py` | 기존 답변 재사용, 새 judge / A·B swap 적용 | judge only |
| `restyle.py` | 답변을 상대 모델 스타일로 재작성 | 2× fighter rewrite |
| `human_baseline.py` | 인터랙티브 인간 채점 + LLM judge 일치율 계산 | 0 |
| `logickor_fight.py` | LogicKor 멀티턴 fighter (turn 1 → turn 2 with context) | 2× (A + B) fighter |
| `logickor_judge.py` | LogicKor 턴별 채점, 카테고리/턴별 집계 | judge × 2 per entry |

## Reproduction

### Dependencies

- Python 3.10+
- `httpx`
- OpenAI / Anthropic / Gemini API 호환 endpoint와 키

### Setup

```bash
git clone https://github.com/kngyeol/llm-judge-bias
cd llm-judge-bias
export OPENAI_API_KEY=<your_key>
pip install -e .     # 선택: judge-bias-{fight,replay,restyle,human} CLI 등록
```

### Run (자작 챌린지 50판)

```bash
# v1 (judge 3종 따로)
python3 gladiator.py --challenges challenges.json challenges-extended.json \
    --judge gpt-5 --tag judge-gpt5

# v2-A: Position swap
python3 replay_judge.py --from-battle results/battle_..._judge-gpt5 \
    --judge gpt-5 --swap-ab --tag swap-gpt5

# v2-B: Self-judge
python3 replay_judge.py --from-battle results/battle_..._judge-gpt5 \
    --judge gpt-5.2 --tag self-gpt

# v2-C: Stylometric (rewrite → re-judge)
python3 restyle.py --from-battle results/battle_..._judge-gpt5 --tag swap
python3 replay_judge.py --from-battle results/restyle_..._swap \
    --judge gpt-5 --tag stylometric-gpt5

# v3: Human baseline
python3 human_baseline.py            # interactive scoring
python3 human_baseline.py --compare  # LLM judge들과 일치율 계산
```

### Run (LogicKor 84 판정)

```bash
# 1. LogicKor 데이터 다운로드 (포함되어 있음)
# logickor_questions.jsonl

# 2. 멀티턴 fighter 실행 (~50분, 42 entries × 4 calls)
python3 logickor_fight.py --budget 6500

# 3. 3개 심판 병렬 실행 (~10-15분 each)
python3 logickor_judge.py --judge gpt-5            --tag logickor-gpt5
python3 logickor_judge.py --judge claude-sonnet-4-5 --tag logickor-claude
python3 logickor_judge.py --judge gemini-2.5-flash  --tag logickor-gemini
```

### Custom endpoints

기본 설정은 OpenAI / Anthropic / Gemini API 호환 프록시를 호출. 직접 endpoint를 쓰려면 `gladiator.py` 상단의 `GMS_*` 상수를 수정:

```python
GMS_OPENAI    = "https://api.openai.com/v1"
GMS_ANTHROPIC = "https://api.anthropic.com/v1"
GMS_GEMINI    = "https://generativelanguage.googleapis.com/v1beta"
```

## Directory Structure

```
.
├── gladiator.py                              # 기본 battle runner
├── replay_judge.py                           # 답변 재사용 + 재채점
├── restyle.py                                # 스타일 재작성
├── human_baseline.py                         # 인간 채점 CLI
├── logickor_fight.py                         # LogicKor 멀티턴 fighter
├── logickor_judge.py                         # LogicKor 턴별 judge
├── challenges.json                           # 자작 챌린지 10개
├── challenges-extended.json                  # 자작 챌린지 40개
├── logickor_questions.jsonl                  # LogicKor 42 entries
├── pyproject.toml
└── results/
    ├── ANALYSIS.md                           # v1
    ├── ANALYSIS_v2.md                        # v2
    ├── ANALYSIS_v3_human.md                  # v3
    ├── ANALYSIS_logickor.md                  # LogicKor
    ├── battle_*/                             # v1 결과 (3 심판 × 50판)
    ├── replay_*_swap-*/                      # v2 position swap
    ├── replay_*_self-*/                      # v2 self-judge
    ├── replay_*_stylometric-*/               # v2 stylometric
    ├── restyle_*/                            # v2 restyle 답변
    ├── human_baseline/                       # v3 인간 채점
    │   ├── progress.json
    │   └── comparison.json
    ├── logickor_fights/                      # LogicKor 답변 raw
    └── logickor_judge_*/                     # LogicKor 3 심판 채점
```

## Position of This Project

본 프로젝트는 **선행 연구의 lightweight 재현**이다. Novel research가 아니라:
- 학계가 이미 검증한 현상(self-preference, position bias, family bias)을 최신 모델(GPT-5.2, Claude-Opus-4.5, Gemini-2.5-Flash)로 직접 확인
- 30분~1시간이면 누구나 본인 데이터로 같은 실험을 돌릴 수 있는 도구 모음 제공
- 한국어를 포함한 챌린지셋에서의 정성적 사례 기록
- 동일 모델 쌍을 4가지 setup으로 측정하여 **setup 효과가 model 차이만큼 클 수 있다**는 메타 시그널 기록

학술적 기여를 원한다면 아래 **Prior Work**의 논문들과 KUDGE / JudgeLM 같은 대규모 데이터셋을 참고하라.

## Prior Work

이 프로젝트가 다루는 모든 핵심 현상은 다음 선행 연구에서 더 엄밀하게 검증됨:

### Self-preference & Family Bias

- **Panickssery et al., NeurIPS 2024** — [LLM Evaluators Recognize and Favor Their Own Generations](https://arxiv.org/abs/2404.13076)
  - Self-recognition 능력과 self-preference 강도 사이 선형 상관관계 입증
  - Fine-tuning 통제 실험으로 인과 관계 분석
- **Wataoka et al., NeurIPS 2024** — [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819)
  - 정량 메트릭 제안, Chatbot Arena 33,000 대화로 검증
  - Self-preference 원인 = 낮은 perplexity 답변 선호 가설 입증
- **["Play Favorites" (arXiv:2508.06709)](https://arxiv.org/abs/2508.06709)** — Self-bias 측정 통계 방법

### LLM Judge Bias Taxonomy

- **Zheng et al., NeurIPS 2023** — [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)
  - LLM-as-a-judge 개념 정립, position/verbosity bias 최초 분류
  - GPT-4 심판이 인간과 80% 일치율 달성 보고
- **["Justice or Prejudice?" (2024)](https://llm-judge-bias.github.io/)** — 12가지 LLM-as-judge bias 분류, CALM 자동 평가 프레임워크 ([dataset](https://github.com/Y0oMu/LLM-Judge-Bias-Dataset))

### Datasets & Tools

- **[JudgeLM (ICLR 2025 Spotlight)](https://github.com/baaivision/JudgeLM)** — 100k judge samples 학습셋 + 5k validation, position/knowledge/format bias 정의 + mitigation (swap augmentation, reference support)
- **[Awesome-LLMs-as-Judges](https://github.com/CSHaitao/Awesome-LLMs-as-Judges)** — 분야 survey repo

### 한국어 LLM 평가

- **KUDGE (Son et al., 2024)** — [LLM-as-a-Judge & Reward Model: What They Can and Cannot Do](https://arxiv.org/abs/2409.11239)
  - 최초 비영어 meta-evaluation 데이터셋, **한국어 human annotations 5,012개**
  - Korean/English bilingual, pointwise + pairwise 평가
  - 본 프로젝트 N=50, 인간 1명과 비교하면 **약 100배 규모**
- **[LogicKor](https://github.com/instructkr/LogicKor)** — 한국어 MT-Bench 적응 버전, Korean grammar 카테고리 포함 (본 repo에서 챌린지셋만 차용)
- **[Horangi](https://github.com/wandb/llm-leaderboard-korean)** — 한국어 LLM 평가 프레임워크 (GLP + ALT 두 축)
- **[KMMLU](https://arxiv.org/abs/2402.11548)** — 한국어 MMLU (45개 전문 분야)
- **[KLUE](https://github.com/KLUE-benchmark/KLUE)** — 한국어 NLU 8 task 벤치마크

## Limitations

본 프로젝트의 통계적·방법론적 한계:

1. **표본 부족**
   - 자작 N=50, LogicKor N=84 (Chatbot Arena: 33k, KUDGE: 5k, JudgeLM: 100k와 비교)
   - 인간 채점자 1명 → inter-rater reliability 측정 불가
   - 통계적 유의성 검정 미수행
2. **모델 tier 불균등** — LLM 심판 (GPT-5 / Sonnet-4.5 / Flash-2.5)이 동일 등급 아님 → "family bias"와 "tier 차이" 분리 불가
3. **챌린지 편향**
   - 자작 챌린지: 1인 작성자 취향 반영
   - LogicKor: 챌린지셋 자체의 평가축이 fighter 한쪽에 유리할 가능성 미통제
4. **Stylometric rewrite 품질 미통제** — 답변을 상대 스타일로 재작성한 결과의 품질 일관성 미측정
5. **Self-judge 분리 불가** — 모델이 자기 응답 스타일을 인지했을 가능성을 통제하지 못함 (Panickssery et al. 2024는 fine-tuning으로 분리)
6. **포지션 라벨 표면적 swap만 수행** — `A`/`B` 라벨 자체를 다른 토큰으로 바꾸는 통제 미수행
7. **LogicKor 멀티턴 평가 단일 prompt** — 두 턴을 보고 한 번에 판정, 턴별 가중치 미분리
8. **LogicKor reference 미활용** — 일부 entries의 `references` 필드 정답 후보 미사용
9. **단일 시드, 1회 측정** — 같은 setup 반복 측정으로 분산 미측정
10. **선행 연구 미사전 검토** — 설계 시 위 Prior Work 미숙지. 사후 정렬한 결과 본 프로젝트의 주요 발견은 모두 기존 보고와 일치하거나 더 약한 형태임

## License

MIT (본 repo의 코드·자작 챌린지·분석 문서). LogicKor 챌린지셋은 [원본 라이센스](https://github.com/instructkr/LogicKor)를 따름.

## Contributing

우선순위:
- 다수 인간 채점자 (inter-rater reliability 측정)
- 추가 모델 가족 (Llama, Qwen, Mistral, DeepSeek 등)
- Forced-binary 채점 옵션 (TIE 금지)
- 다국어 챌린지셋 (영어/일본어/중국어 등)
- 라벨 이름 자체 randomization (A/B 외 다른 토큰)
- LogicKor reference 기반 자동 채점 모드
- 분산 측정 (같은 setup 반복 실행)
