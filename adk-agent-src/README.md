# adk-agent (ЛР 1, варіант 10)

Цей каталог містить лише власні файли: `app/agent.py`, `app/environment.py`,
`app/__init__.py`, `tests/unit/test_environment.py`. Каркас створює Agents CLI:

    cd ~/ai-agents/lab01-agents
    mv adk-agent adk-agent-src                     # зберегти мої файли
    agents-cli create adk-agent --prototype --yes
    cp -r adk-agent-src/app/{agent.py,environment.py,__init__.py} adk-agent/app/
    cp adk-agent-src/tests/unit/test_environment.py adk-agent/tests/unit/
    cd adk-agent && agents-cli install
    # у .env: закоментувати GOOGLE_*, додати GEMINI_API_KEY
    agents-cli playground
    agents-cli run "Які аномалії допускають Read Committed, Repeatable Read і Serializable?"
    agents-cli lint && uv run pytest tests/unit tests/integration

Якщо `app/__init__.py` у каркасі відрізняється, залиште версію каркаса.
