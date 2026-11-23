    cp .env.example .env     # вписати GEMINI_API_KEY
    uv sync
    uv run pytest -q
    uv run python main.py "Порівняй Read Uncommitted і Serializable"
    uv run python main.py "Порівняй Read Uncommitted і Serializable" --mode oneshot
    uv run python main.py "Опиши рівень ізоляції Cursor Stability"
    uv run python main.py "Порівняй Read Uncommitted і Serializable" --max-steps 1   # зупинка за max_steps
