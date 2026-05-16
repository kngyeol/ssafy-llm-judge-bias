# LLM Judge Bias Benchmark

LLM-as-a-judge 평가 방식에서 발생하는 세 가지 편향을 측정하는 벤치마크:
- **In-family bias** — 심판 모델이 같은 family 답변을 더 선호하는 경향
- **Position bias** — A/B 라벨 위치에 따라 판정이 흔들리는 정도
- **Self-preference** — 모델이 자기 자신의 답변을 채점할 때 발생하는 편향

같은 50개 챌린지에 두 모델(GPT-5.2 vs Claude-Opus-4.5)의 답변을 받아, 3개 LLM 심판(GPT-5 / Claude-Sonnet-4.5 / Gemini-2.5-Flash)과 1명의 인간이 채점한 결과를 비교한다.

## Key Findings

### A 선호율 (TIE 제외, GPT-5.2 답변을 선택한 비율)

| 평가자 | A 선호율 | 인간 대비 편향 |
|---|---|---|
| Human (ground truth) | 39% | — |
| Claude-Sonnet | 42% | +3pp |
| Gemini-Flash | 58% | +19pp |
| GPT-5 | 72% | +33pp |

### 라운드별 일치율

- LLM 심판 ↔ LLM 심판: 44–62%
- **LLM 심판 ↔ 인간: 30–38%** (3-class random baseline 33%)

### 만장일치 오류의 비대칭

LLM 심판 3개가 *모두* 같은 답을 골랐지만 인간이 다른 답을 고른 라운드는 9건. 그중 8건이 GPT 과대평가 방향, 1건이 Claude 과대평가. 무작위 오류로 보기 어려운 체계적 편향.

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
git clone https://github.com/kngyeol/ssafy-llm-judge-bias
cd ssafy-llm-judge-bias
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

## Limitations

- N=50 단일 시드, 인간 채점자 1명 → 통계적 검정력 제한
- LLM 심판 모델 tier 불균등 (GPT-5 / Sonnet-4.5 / Flash-2.5)
- Stylometric rewrite 품질 일관성 미통제
- Self-judge에서 모델이 자기 응답 스타일을 인지했을 가능성 분리 불가
- 챌린지가 한국어 + 영어 코드/SQL 혼합으로 모델별 강점 영역 편향 가능

## Related Work

- Zheng et al., 2023 — [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) (position bias, verbosity bias)
- [JudgeBench](https://huggingface.co/datasets/PKU-Alignment/JudgeBench) — large-scale judge evaluation dataset

## License

MIT

## Contributing

우선순위:
- 다수 인간 채점자 (inter-rater reliability 측정)
- 추가 모델 가족 (Llama, Qwen, Mistral, DeepSeek 등)
- Forced-binary 채점 옵션 (TIE 금지)
- 다국어 챌린지셋 (영어/일본어/중국어 등)
- 라벨 이름 자체 randomization (A/B 외 다른 토큰)
