# LLM 심판 편향 실험 — GPT vs Claude × 3명의 심판 + 1명의 인간

> 같은 50개 챌린지에 두 LLM이 답하고, 3개 LLM 심판 + 1명의 인간이 채점.
> **인간이 보기엔 Claude가 19승 vs GPT 12승**. LLM 심판들은 GPT를 +20~33%p 과대평가.
> **LLM-as-a-judge는 production에 못 쓸 수준 (인간과 30~38% 일치)**.

LLM-as-a-judge 평가 방식의 in-family bias 검증을 위한 3단계 실험:
- **v1** 기본 격투 — [ANALYSIS.md](results/ANALYSIS.md)
- **v2** 통제 실험 (position swap + self-judge + stylometric) — [ANALYSIS_v2.md](results/ANALYSIS_v2.md)
- **v3** 인간 baseline — [ANALYSIS_v3_human.md](results/ANALYSIS_v3_human.md)

## TL;DR

### A 선호율 (TIE 제외, GPT-5.2가 얼마나 이겼나)

| 평가자 | A 선호율 | 인간 대비 편향 |
|---|---|---|
| **🧑 인간 (ground truth)** | **39%** | **(기준)** |
| Claude-Sonnet 심판 | 42% | **+3%p ← 가장 정확** |
| Gemini-Flash 심판 | 58% | +19%p |
| GPT-5 심판 | 72% | **+33%p ← 거대한 family bias** |

### 라운드별 일치율

| 비교 | 일치 |
|---|---|
| LLM 심판 ↔ LLM 심판 | 44–62% |
| **LLM 심판 ↔ 인간** | **30–38%** (무작위 baseline 33%!) |

### 핵심 발견 4가지

1. **인간 ground truth는 Claude 손**: 인간 채점에선 Claude-Opus 19승 vs GPT-5.2 12승. v1·v2의 "GPT 우위"는 LLM 심판들의 환상.
2. **LLM 심판 만장일치 오류 8:1로 GPT 편향**: 3개 심판이 모두 같은 답을 골랐는데 인간이 다른 답을 고른 9건 중 8건이 GPT 과대평가.
3. **Position bias는 모델마다 다르다**: GPT-5는 거의 0, Claude는 6%, Gemini는 무려 50%가 위치에 의해 흔들림 (v2 swap).
4. **Self-preference도 비대칭**: GPT-5.2는 자기 답 64% 선호 vs Claude-Opus는 22% (회피적). v2 self-judge.

## 실험 설계

- **선수 A**: GPT-5.2 (`gpt-5.2`)
- **선수 B**: Claude-Opus-4.5 (`claude-opus-4-5-20251101`)
- **챌린지 50개**: code / writing / reasoning / creative / korean 각 10개
- **심판 3명**: GPT-5, Claude-Sonnet-4.5, Gemini-2.5-Flash
- **총 비용**: 약 14,000 SSAFY GMS 크레딧

## 디렉토리 구조

```
.
├── gladiator.py                              # 메인 실행 스크립트
├── challenges.json                           # 챌린지 10개 (시드)
├── challenges-extended.json                  # 챌린지 40개 (확장)
└── results/
    ├── ANALYSIS.md                           # 📊 분석 + 결론
    ├── battle_..._judge-gpt5/                # GPT-5 심판 결과
    ├── battle_..._judge-claude/              # Claude 심판 결과
    └── battle_..._judge-gemini/              # Gemini 심판 결과
        ├── _SUMMARY.md                       # 사람이 읽는 요약
        ├── _results.json                     # 기계가 읽는 집계
        └── <challenge_id>.md                 # 라운드별 상세 (양 답변 + 심판 코멘트)
```

## v2 도구 모음 (방법론 강화)

v1의 한계(position bias, single seed, family vs tier 혼동)를 보완하기 위한 추가 실험 도구:

| 도구 | 목적 | 비용 |
|---|---|---|
| `replay_judge.py` | 기존 답변 재사용, 새 심판/위치교체로 재채점 | 심판 호출만 (저렴) |
| `restyle.py` | 답변을 상대 스타일로 재작성 → 스타일 vs 내용 분리 | rewrite + 재채점 |
| `human_baseline.py` | 본인이 라벨 가린 채 50판 채점 → LLM 심판과 일치율 측정 | 0 (시간만) |

### v2 실험 예시

```bash
# Position bias 통제: A/B 위치 교체해서 재채점
python3 replay_judge.py --from-battle results/battle_..._judge-gpt5 \
  --judge gpt-5 --swap-ab --tag swap-gpt5 --budget 2000

# Self-judge: 모델이 자기 답을 직접 채점
python3 replay_judge.py --from-battle results/battle_..._judge-gpt5 \
  --judge gpt-5.2 --tag self-gpt --budget 2000

# Stylometric: 스타일을 뒤바꾼 답변으로 재대결
python3 restyle.py --from-battle results/battle_..._judge-gpt5 --tag swap
python3 replay_judge.py --from-battle results/restyle_..._swap \
  --judge gpt-5 --tag stylometric-gpt --budget 2000

# Human baseline: 직접 채점 (인터랙티브)
python3 human_baseline.py
python3 human_baseline.py --compare    # 채점 후 LLM 심판들과 일치율 비교
```

### 설치 (선택)

```bash
pip install -e .

# 그러면 어디서든:
judge-bias-fight --help
judge-bias-replay --help
judge-bias-restyle --help
judge-bias-human --help
```

## 재현 방법

### 1. 의존성

- Python 3.10+ (gladiator.py가 `str | None` 같은 신문법 사용)
- `httpx` (`pip install httpx`)
- OpenAI-호환 / Anthropic 호환 / Gemini 호환 endpoint 키

### 2. API 키 설정

SSAFY 학생이라면 GMS 프록시를 그대로 쓸 수 있다:

```bash
export OPENAI_API_KEY="<GMS_KEY>"
```

다른 프록시/직접 endpoint를 쓰려면 `gladiator.py` 상단의 `GMS_*` 상수를 본인 endpoint로 교체.

### 3. 실행

```bash
# dry-run으로 비용 추산
python3 gladiator.py --challenges challenges.json challenges-extended.json --dry-run

# 한 챌린지만 (스모크 테스트)
python3 gladiator.py --only writing-2 --judge gemini-2.5-flash --budget 200

# 본 실험 (3 심판 각각)
python3 gladiator.py --challenges challenges.json challenges-extended.json --judge gpt-5            --tag judge-gpt5    --budget 6000
python3 gladiator.py --challenges challenges.json challenges-extended.json --judge claude-sonnet-4-5 --tag judge-claude  --budget 6000
python3 gladiator.py --challenges challenges.json challenges-extended.json --judge gemini-2.5-flash  --tag judge-gemini  --budget 6000
```

### 4. CLI 옵션

```
--challenges PATH ...   챌린지 JSON 파일 (여러 개 가능, 합쳐짐)
--judge NAME            gpt-5 | claude-sonnet-4-5 | gemini-2.5-flash | <model_id>
--tag SUFFIX            결과 디렉토리 이름 접미사
--only CHALLENGE_ID     특정 챌린지 하나만 실행
--budget N              누적 credit 한도 (기본 10000, 초과 시 abort)
--dry-run               호출 없이 비용 추산만
```

## 관련 작업

이 실험은 학술 작업이 아니라 학생 1인이 주말에 돌린 작은 검증이다. 더 깊이 들어가고 싶다면:

- **논문**: ["Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"](https://arxiv.org/abs/2306.05685) (Zheng et al., 2023) — position bias / verbosity bias 다룸
- **벤치마크**: [JudgeBench](https://huggingface.co/datasets/PKU-Alignment/JudgeBench) — 대규모 심판 평가 데이터셋

## 한계

[ANALYSIS.md §5](results/ANALYSIS.md#5-한계--솔직하게)에 자세히 적었다. 요약:
- 표본 50개는 통계적으로 약함
- 심판 3종이 동급 모델이 아님 (Sonnet vs Flash vs GPT-5)
- A/B 위치 편향 미통제
- 단일 시드, 분산 미측정

## 라이선스

MIT — 자유롭게 fork / 확장 / 인용 가능

## 기여

PR 환영합니다. 특히:
- 챌린지 추가 (한국어 외 언어, 도메인 특화)
- 심판 모델 추가 (Llama, Qwen, Mistral 등)
- A/B 위치 자동 셔플 옵션
- 분산 측정 (같은 챌린지 N회 반복)
