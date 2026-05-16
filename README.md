# LLM Judge Bias Benchmark (lightweight reproduction)

LLM-as-a-judge 평가 방식의 세 가지 편향을 50라운드 규모로 직접 확인하는 재현 실험:
- **In-family bias** — 심판 모델이 같은 family 답변을 더 선호하는 경향
- **Position bias** — A/B 라벨 위치에 따라 판정이 흔들리는 정도
- **Self-preference** — 모델이 자기 자신의 답변을 채점할 때 발생하는 편향

같은 50개 챌린지에 두 모델(GPT-5.2 vs Claude-Opus-4.5)의 답변을 받아, 3개 LLM 심판(GPT-5 / Claude-Sonnet-4.5 / Gemini-2.5-Flash)과 1명의 인간이 채점한 결과를 비교한다.

> ⚠️ **본 프로젝트는 학술적 contribution이 아니라 lightweight reproduction이다.** 다루는 모든 현상은 [Prior Work](#prior-work)에서 더 엄밀하게 검증됨. 학술적 인용/응용은 원본 논문을 참조.

## Key Findings (이 setup 기준, n=50, 인간 1명)

### A 선호율 (TIE 제외, GPT-5.2 답변을 선택한 비율)

| 평가자 | A 선호율 | 인간 대비 편향 |
|---|---|---|
| Human (ground truth) | 39% | — |
| Claude-Sonnet | 42% | +3pp |
| Gemini-Flash | 58% | +19pp |
| GPT-5 | 72% | +33pp |

### 라운드별 일치율

- LLM 심판 ↔ LLM 심판: 44–62%
- LLM 심판 ↔ 인간: 30–38% (3-class random baseline 33%)

> 참고: Zheng et al. 2023의 MT-Bench setup에서는 GPT-4 심판이 인간과 **80% 일치율**을 기록. 본 setup의 낮은 수치는 (1) 챌린지 도메인 차이, (2) 인간 1명의 채점 편향, (3) 한국어 비중 등의 요인이 섞임. 본 데이터는 **이 setup 한정** 보고이며 LLM-as-a-judge 일반에 대한 결론으로 해석 금지.

### 만장일치 오류의 비대칭

LLM 심판 3개가 *모두* 같은 답을 골랐지만 인간이 다른 답을 고른 라운드는 9건. 그중 8건이 GPT 과대평가 방향, 1건이 Claude 과대평가. n=9 표본에선 통계적 검정력 약하나, Panickssery 2024 등 선행 연구의 self-preference 결과와 방향 일치.

### Position swap 강도 (v2 통제 실험)

| 심판 | swap 후 라운드 일치 | 해석 |
|---|---|---|
| GPT-5 | 41/50 (82%) | 위치 무관, 진짜 family bias |
| Claude-Sonnet | 36/50 (72%) | 위치에 약간 흔들림 |
| Gemini-Flash | 29/50 (58%) | 약 절반이 position bias |

### Self-preference 비대칭 (v2)

같은 모델이 자기 답을 채점할 때:
- GPT-5.2 → 자기 답 64% 선호
- Claude-Opus → 자기 답 22% 선호 (TIE 48%)

## Documents

| 파일 | 내용 |
|---|---|
| [`results/ANALYSIS.md`](results/ANALYSIS.md) | v1 — 3개 심판 기본 비교 (4,200자) |
| [`results/ANALYSIS_v2.md`](results/ANALYSIS_v2.md) | v2 — Position swap / self-judge / stylometric 통제 실험 (5,500자) |
| [`results/ANALYSIS_v3_human.md`](results/ANALYSIS_v3_human.md) | v3 — 인간 ground truth 추가 (4,000자) |

## Experimental Setup

- **Fighter A**: `gpt-5.2`
- **Fighter B**: `claude-opus-4-5-20251101`
- **LLM Judges**: `gpt-5`, `claude-sonnet-4-5-20250929`, `gemini-2.5-flash`
- **Challenges**: 50개 — `code` / `writing` / `reasoning` / `creative` / `korean` 각 10개
- **Human Judge**: 1명, 50개 라운드 라벨 가린 채 직접 채점

## Tools

| Script | Purpose | Cost |
|---|---|---|
| `gladiator.py` | Fighter 응답 생성 + judge 실행 | fighter + judge |
| `replay_judge.py` | 기존 답변 재사용, 새 judge / A·B swap 적용 | judge only |
| `restyle.py` | 답변을 상대 모델 스타일로 재작성 | 2× fighter rewrite |
| `human_baseline.py` | 인터랙티브 인간 채점 + LLM judge 일치율 계산 | 0 |

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

### Run

```bash
# 챌린지 합쳐서 v1 실행 (judge 3종 따로 따로)
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
├── challenges.json                           # 챌린지 10개
├── challenges-extended.json                  # 챌린지 40개
├── pyproject.toml
└── results/
    ├── ANALYSIS.md / ANALYSIS_v2.md / ANALYSIS_v3_human.md
    ├── battle_*/                             # v1 결과
    ├── replay_*_swap-*/                      # v2 position swap
    ├── replay_*_self-*/                      # v2 self-judge
    ├── replay_*_stylometric-*/               # v2 stylometric
    ├── restyle_*/                            # v2 restyle 원본
    └── human_baseline/
        ├── progress.json                     # 인간 채점 raw
        └── comparison.json                   # LLM judge 비교 결과
```

## Position of This Project

본 프로젝트는 **선행 연구의 lightweight 재현**이다. Novel research가 아니라:
- 학계가 이미 검증한 현상(self-preference, position bias, family bias)을 최신 모델(GPT-5.2, Claude-Opus-4.5, Gemini-2.5-Flash)로 직접 확인
- 30분~1시간이면 누구나 본인 데이터로 같은 실험을 돌릴 수 있는 도구 모음 제공
- 한국어를 포함한 챌린지셋에서의 정성적 사례 기록

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
- **[LogicKor](https://huggingface.co/spaces/instructkr/LogicKor-leaderboard)** — 한국어 MT-Bench 적응 버전, Korean grammar 카테고리 포함
- **[Horangi](https://github.com/wandb/llm-leaderboard-korean)** — 한국어 LLM 평가 프레임워크 (GLP + ALT 두 축)
- **[KMMLU](https://arxiv.org/abs/2402.11548)** — 한국어 MMLU (45개 전문 분야)
- **[KLUE](https://github.com/KLUE-benchmark/KLUE)** — 한국어 NLU 8 task 벤치마크

## Limitations

이 프로젝트의 통계적·방법론적 한계:

1. **표본 부족**
   - N=50 단일 시드 (Chatbot Arena: 33k, KUDGE: 5k, JudgeLM: 100k와 비교)
   - 인간 채점자 1명 → inter-rater reliability 측정 불가
   - 통계적 유의성 검정 미수행
2. **모델 tier 불균등** — LLM 심판 (GPT-5 / Sonnet-4.5 / Flash-2.5)이 동일 등급 아님 → "family bias"와 "tier 차이" 분리 불가
3. **챌린지 편향** — 한국어 + 영어 코드/SQL 혼합. 제작자(작성자) 1인의 취향이 반영됨
4. **Stylometric rewrite 품질 미통제** — 답변을 상대 스타일로 재작성한 결과의 품질 일관성 미측정
5. **Self-judge 분리 불가** — 모델이 자기 응답 스타일을 인지했을 가능성을 통제하지 못함 (Panickssery et al. 2024는 fine-tuning으로 분리)
6. **포지션 라벨 표면적 swap만 수행** — `A`/`B` 라벨 자체를 다른 토큰(`답변1`/`답변2`, 무작위 토큰 등)으로 바꾸는 통제 미수행
7. **선행 연구 미사전 검토** — v1 설계 시 위 Prior Work를 모르고 시작함. 사후 정렬한 결과 본 프로젝트의 주요 발견은 모두 기존 보고와 일치하거나 더 약한 형태임

## License

MIT

## Contributing

우선순위:
- 다수 인간 채점자 (inter-rater reliability 측정)
- 추가 모델 가족 (Llama, Qwen, Mistral, DeepSeek 등)
- Forced-binary 채점 옵션 (TIE 금지)
- 다국어 챌린지셋 (영어/일본어/중국어 등)
- 라벨 이름 자체 randomization (A/B 외 다른 토큰)
