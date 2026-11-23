"""Середовище агента: перевірені відомості про рівні ізоляції транзакцій SQL.

Детермінований код без LLM. Джерела фактів:
  [1] ISO/IEC 9075 (SQL), частина 2 Foundation: рівні ізоляції та феномени
      P1 dirty read, P2 non-repeatable read, P3 phantom.
  [2] PostgreSQL Documentation, розділ 13.2 "Transaction Isolation".
  [3] H. Berenson et al. "A Critique of ANSI SQL Isolation Levels",
      ACM SIGMOD, 1995 (snapshot isolation, write skew).
"""

LEVELS: dict[str, str] = {
    "read-uncommitted": (
        "Read Uncommitted: найнижчий рівень ізоляції за стандартом SQL; "
        "транзакція може читати незафіксовані зміни інших транзакцій. "
        "Допускає dirty read, non-repeatable read і phantom read. "
        "У PostgreSQL цей рівень поводиться як Read Committed."
    ),
    "read-committed": (
        "Read Committed: кожен запит бачить лише дані, зафіксовані до його "
        "початку. Усуває dirty read, але допускає non-repeatable read і "
        "phantom read. Рівень за замовчуванням у PostgreSQL."
    ),
    "repeatable-read": (
        "Repeatable Read: повторне читання тих самих рядків у межах "
        "транзакції дає той самий результат. За стандартом SQL усуває dirty "
        "read і non-repeatable read, але допускає phantom read; у PostgreSQL "
        "рівень реалізовано на знімках даних, і phantom read там не виникає."
    ),
    "serializable": (
        "Serializable: найвищий рівень; результат паралельних транзакцій "
        "еквівалентний деякому їхньому послідовному виконанню. Усуває dirty "
        "read, non-repeatable read і phantom read. Транзакцію може бути "
        "відхилено через конфлікт серіалізації, тоді її треба повторити."
    ),
    "snapshot": (
        "Snapshot: транзакція працює зі знімком даних на момент свого "
        "початку. Не входить до чотирьох рівнів стандарту SQL. Запобігає "
        "dirty read, non-repeatable read і phantom read, але допускає "
        "аномалію write skew."
    ),
}

ANOMALIES: dict[str, str] = {
    "dirty-read": (
        "Dirty read: транзакція читає зміни іншої транзакції, ще не "
        "зафіксовані; якщо та відкотиться, прочитані дані ніколи не існували. "
        "Допускає лише Read Uncommitted."
    ),
    "non-repeatable-read": (
        "Non-repeatable read: повторне читання того самого рядка в межах "
        "однієї транзакції дає інше значення, бо інша транзакція змінила "
        "рядок і зафіксувала зміну. Допускають Read Uncommitted і Read "
        "Committed."
    ),
    "phantom-read": (
        "Phantom read: повторний запит з тією самою умовою повертає інший "
        "набір рядків, бо інша транзакція додала або видалила рядки й "
        "зафіксувала зміни. За стандартом SQL допускають Read Uncommitted, "
        "Read Committed і Repeatable Read."
    ),
}

NOT_FOUND = "NOT_FOUND"


def normalize_name(name: str) -> str:
    """Зводить 'Read Committed', 'read_committed', ' READ-COMMITTED ' до 'read-committed'."""
    return name.strip().lower().replace(" ", "-").replace("_", "-")


def lookup_isolation_level(name: str) -> str:
    """Return verified information about one SQL transaction isolation level.

    Use it when the user asks about a specific isolation level such as
    read uncommitted, read committed, repeatable read, serializable or snapshot.

    Args:
        name: identifier of the level, for example "read committed" or "serializable".

    Returns:
        "<id>: <description>" or a line starting with NOT_FOUND.
    """
    key = normalize_name(name)
    if key not in LEVELS:
        return f"{NOT_FOUND}: no verified information about isolation level '{name}'."
    return f"{key}: {LEVELS[key]}"


def lookup_anomaly(name: str) -> str:
    """Return verified information about one transaction concurrency anomaly.

    Use it when the user asks about an anomaly such as dirty read,
    non-repeatable read or phantom read, or which levels allow it.

    Args:
        name: identifier of the anomaly, for example "dirty read" or "phantom read".

    Returns:
        "<id>: <description>" or a line starting with NOT_FOUND.
    """
    key = normalize_name(name)
    if key not in ANOMALIES:
        return f"{NOT_FOUND}: no verified information about anomaly '{name}'."
    return f"{key}: {ANOMALIES[key]}"
