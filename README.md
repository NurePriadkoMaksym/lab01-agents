# lab01-agents (варіант 10: рівні ізоляції транзакцій SQL)

- `manual-agent/` — власний цикл Observe-Reason-Act-Evaluate (без фреймворку), 17 тестів
- `adk-agent/` — той самий агент на Google ADK 2.14.1, 8 тестів
- `docs/` — паспорт агента (`AGENT-CARD.md`) і шаблон таблиці експерименту
- `experiments/adk/` — сирі події ADK-агента для п’яти запитів

## Швидкий старт

```bash
cp manual-agent/.env.example manual-agent/.env
cp adk-agent/.env.example adk-agent/.env  

# 2. Власний агент
cd manual-agent
uv sync
uv run pytest -q                                  
uv run python main.py "Порівняй Read Uncommitted і Serializable"


cd ../adk-agent
agents-cli install
agents-cli lint                                   
uv run pytest tests/unit tests/integration -q     
agents-cli run "Які рівні ізоляції допускають dirty read?"
```

