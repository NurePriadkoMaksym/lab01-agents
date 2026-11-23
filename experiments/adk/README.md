# ADK-агент: сирі результати перевірок

Запуски виконано 16.11.2026 через `agents-cli run -v "<запит>"` (події сервера ADK).
Конфігурація: `gemini-3.5-flash` (API обслуговує її як `gemini-3.6-flash`).

| Файл | Запит | Виклики інструментів | LLM-виклики | Час подій, с |
|---|---|---|---|---|
| `queryE.txt` | Що таке транзакція в СУБД? | 0 | 1 | ~1.5 |
| `queryB.txt` | Порівняй Read Uncommitted і Serializable | 2 × `lookup_isolation_level` | 2 | 3.8 |
| `queryD.txt` | Опиши рівень ізоляції Cursor Stability | 1 × `lookup_isolation_level` → NOT_FOUND | 2 | 3.2 |
| `query_own.txt` | Які рівні ізоляції допускають dirty read? | `lookup_anomaly` + `lookup_isolation_level` | 2 | 3.7 |
| `queryA_lite.txt` | Розкажи про рівень ізоляції Read Committed | 1 × `lookup_isolation_level` | 2 | 1.5 |
| `queryC_lite.txt` | Які аномалії допускають Read Committed, Repeatable Read і Serializable? | 6 викликів (3 рівні + 3 аномалії) | 2 | 1.9 |

`queryA_lite.txt` і `queryC_lite.txt` виконано на `gemini-3.1-flash-lite`, бо денну квоту
`gemini-3.5-flash` вичерпано. Файли `queryA_429.txt` і `queryC_429.txt` — журнали цієї
відмови (429 RESOURCE_EXHAUSTED, 20 запитів/добу на безкоштовному рівні).

Головний результат: на запиті D агент отримав `NOT_FOUND` і прямо визнав відсутність
перевірених даних; one-shot у `manual-agent/experiments/raw_results.json` натомість
вигадав докладний опис Cursor Stability.
