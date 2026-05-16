#!/usr/bin/env python3
"""
기존 배틀의 두 답변을 '상대편 스타일로' 재작성한 새 라운드 디렉토리 생성.
다음 단계로 replay_judge.py 돌리면 stylometric 실험 완성.

전략:
  원본:        A=GPT내용+GPT스타일,  B=Claude내용+Claude스타일
  restyle 후:  A=GPT내용+Claude스타일, B=Claude내용+GPT스타일
  → 심판이 스타일로 판단했다면 결과 뒤집힘
  → 내용으로 판단했다면 결과 유지
"""
import argparse, json, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gladiator import call, RESULTS_DIR
from replay_judge import parse_round_md, load_battle

RESTYLE_SYS = """너는 글을 다른 모델의 스타일로 다시 쓰는 작업을 맡았다.
- 내용·정보·정답·길이·포맷은 최대한 보존
- 톤·어휘·문장구조·인사말 등 표면 스타일만 너의 자연스러운 스타일로 바꿔라
- 새 정보 추가/제거 금지
- 출력은 재작성된 답변만, 메타 코멘트 금지"""

def restyle(answer: str, original_prompt: str, restyler: dict) -> str:
    msg = f"""다음은 원래 문제와 답변이다. 이 답변을 너의 자연스러운 스타일로 다시 써라.

[원래 문제]
{original_prompt}

[원래 답변]
{answer}

[너의 스타일로 재작성한 답변]"""
    return call(restyler, msg, system=RESTYLE_SYS)

# 재작성자 (= 원본 모델의 반대편)
GPT_RESTYLER = {"name": "GPT-5.2", "model": "gpt-5.2", "kind": "openai"}
CLAUDE_RESTYLER = {"name": "Claude-Opus-4.5", "model": "claude-opus-4-5-20251101", "kind": "anthropic"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--from-battle", required=True)
    p.add_argument("--tag", required=True)
    p.add_argument("--budget", type=int, default=10000)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    battle_dir = Path(args.from_battle)
    rounds = load_battle(battle_dir)
    if not rounds:
        sys.exit("❌ 라운드 0개")

    # 비용: 각 라운드당 Claude 1회(=50) + GPT 1회(=20) = 70 credit
    cost = len(rounds) * 70
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"원본 배틀  : {battle_dir.name}")
    print(f"라운드 수  : {len(rounds)}")
    print(f"재작성 모델: A→Claude스타일 (Claude-Opus), B→GPT스타일 (GPT-5.2)")
    print(f"예상 비용  : 약 {cost:,} credit")
    print(f"예산 한도  : {args.budget:,} credit")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    if cost > args.budget:
        sys.exit("❌ 예산 초과")
    if args.dry_run:
        print("(dry-run)")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = RESULTS_DIR / f"restyle_{timestamp}_{args.tag}"
    out_dir.mkdir()

    for i, r in enumerate(rounds, 1):
        print(f"\n[{i}/{len(rounds)}] {r['id']} — {r['name']}", flush=True)
        try:
            print(f"  → A(원본 GPT 내용)을 Claude 스타일로...", flush=True)
            new_a = restyle(r["ans_a"], r["prompt"], CLAUDE_RESTYLER)
            print(f"  → B(원본 Claude 내용)을 GPT 스타일로...", flush=True)
            new_b = restyle(r["ans_b"], r["prompt"], GPT_RESTYLER)
        except Exception as e:
            print(f"  ❌ {e}")
            continue

        # 원본 gladiator.py 결과 포맷과 호환되게 저장
        md = f"""# {r['name']}  ({r['category']})

**문제**
> {r['prompt']}

## 🅰️  GPT-5.2
{new_a}

## 🅱️  Claude-Opus-4.5
{new_b}

## ⚖️  심판 (RESTYLED — replay_judge.py 로 채점 필요)
(아직 심판 호출 전. 이 디렉토리에 replay_judge.py --from-battle 이 디렉토리 ... 실행)
"""
        (out_dir / f"{r['id']}.md").write_text(md, encoding="utf-8")

    # 메타데이터
    meta = {
        "timestamp": timestamp,
        "tag": args.tag,
        "source_battle": battle_dir.name,
        "restyle": {
            "a_restyler": CLAUDE_RESTYLER,
            "b_restyler": GPT_RESTYLER,
            "intent": "원본 A(GPT 내용)을 Claude 스타일로, 원본 B(Claude 내용)을 GPT 스타일로",
        },
        "note": "내용은 GPT/Claude 그대로, 스타일만 뒤바뀐 상태. replay_judge.py로 심판 채점 진행.",
    }
    (out_dir / "_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ {out_dir}")
    print(f"  다음 단계: replay_judge.py --from-battle {out_dir} --judge <name> --tag stylometric-<name>")

if __name__ == "__main__":
    main()
