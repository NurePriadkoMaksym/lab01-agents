"""Запускає 5 запитів A-E на one-shot і власному агентові, зберігає сирі дані.

Запуск (потрібен ключ у .env, ~15 викликів API):
    uv run python experiments/run_experiment.py
Результат: experiments/raw_results.json. Правильність, обґрунтованість і
галюцинації оцінюйте ВРУЧНУ за еталоном з environment.py (табл. 8.2 МВ).
ADK-агента запускайте через agents-cli і переписуйте дані з Playground.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.loop import run_agent  # noqa: E402
from baseline import one_shot_answer  # noqa: E402

QUERIES = {
    "A": "Розкажи про рівень ізоляції Read Committed",
    "B": "Порівняй Read Uncommitted і Serializable",
    "C": "Які аномалії допускають Read Committed, Repeatable Read і Serializable?",
    "D": "Опиши рівень ізоляції Cursor Stability",
    "E": "Що таке транзакція в СУБД?",
}


def main() -> None:
    out = Path(__file__).parent / "raw_results.json"
    results = []
    for qtype, query in QUERIES.items():
        print(f"\n>>> Running Query {qtype}: {query}")
        t = time.perf_counter()
        answer = one_shot_answer(query)
        results.append({
            "type": qtype,
            "system": "one-shot",
            "query": query,
            "answer": answer,
            "llm_calls": 1,
            "actions": 0,
            "seconds": round(time.perf_counter() - t, 2)
        })
        out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        time.sleep(3)  # пауза проти HTTP 429

        t = time.perf_counter()
        state = run_agent(query)
        results.append({
            "type": qtype,
            "system": "manual-agent",
            "query": query,
            "answer": state.final_answer,
            "llm_calls": state.llm_calls,
            "actions": sum(1 for r in state.trace if r["action"].startswith("lookup")),
            "stop_reason": state.stop_reason,
            "seconds": round(time.perf_counter() - t, 2)
        })
        out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        time.sleep(3)
    print(f"\nsaved: {out}")


if __name__ == "__main__":
    main()
