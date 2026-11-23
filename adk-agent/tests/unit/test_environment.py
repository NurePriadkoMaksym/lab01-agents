from app.environment import NOT_FOUND, lookup_anomaly, lookup_isolation_level


def test_existing_level():
    assert lookup_isolation_level("read committed").startswith("read-committed:")


def test_unknown_level():
    assert lookup_isolation_level("cursor stability").startswith(NOT_FOUND)


def test_anomaly():
    assert lookup_anomaly("dirty read").startswith("dirty-read:")
