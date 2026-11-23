import pytest

from agent.errors import DecisionError
from agent.validator import validate_decision


def test_valid_lookup():
    validate_decision({"action": "lookup_isolation_level", "arguments": {"name": "snapshot"}})
    validate_decision({"action": "lookup_anomaly", "arguments": {"name": "dirty read"}})


@pytest.mark.parametrize("decision", [
    {"action": "drop_table", "arguments": {}},                          # немає у whitelist
    {"action": "lookup_isolation_level", "arguments": {}},              # бракує аргументу
    {"action": "lookup_anomaly", "arguments": {"name": 42}},            # хибний тип
    {"action": "lookup_anomaly", "arguments": {"name": "  "}},          # порожній рядок
    {"action": "finish"},                                               # немає arguments
])
def test_invalid_decisions(decision):
    with pytest.raises(DecisionError):
        validate_decision(decision)
