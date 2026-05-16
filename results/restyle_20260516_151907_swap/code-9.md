# 딕셔너리 정렬  (code)

**문제**
> Python 딕셔너리 d = {'a': 3, 'b': 1, 'c': 2}를 값 기준 내림차순으로 정렬한 새 딕셔너리를 반환하는 한 줄 코드를 작성하라. 코드만.

## 🅰️  GPT-5.2
```python
dict(sorted(d.items(), key=lambda x: x[1], reverse=True))
```

## 🅱️  Claude-Opus-4.5
```python
{ k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True) }
```

## ⚖️  심판 (RESTYLED — replay_judge.py 로 채점 필요)
(아직 심판 호출 전. 이 디렉토리에 replay_judge.py --from-battle 이 디렉토리 ... 실행)
