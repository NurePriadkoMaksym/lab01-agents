from agent.environment import NOT_FOUND, lookup_anomaly, lookup_isolation_level


def test_existing_level():
    assert lookup_isolation_level("serializable").startswith("serializable:")


def test_name_is_normalized():
    assert lookup_isolation_level(" Read_Committed ").startswith("read-committed:")


def test_unknown_level():
    assert lookup_isolation_level("cursor stability").startswith(NOT_FOUND)


def test_existing_anomaly():
    assert lookup_anomaly("Phantom Read").startswith("phantom-read:")


def test_unknown_anomaly():
    assert lookup_anomaly("write skew").startswith(NOT_FOUND)
