"""Тести циклу без звернень до API: рішення моделі підміняє сценарій."""
from agent.loop import run_agent


def scripted(decisions):
    queue = iter(decisions)

    def decide(goal, observations, step, max_steps):
        return next(queue)
    return decide


def test_lookup_then_finish():
    decide = scripted([
        {"action": "lookup_isolation_level", "arguments": {"name": "read committed"},
         "decision_summary": "Потрібні дані."},
        {"action": "finish", "arguments": {"answer": "Read Committed усуває dirty read."},
         "decision_summary": "Даних достатньо."},
    ])
    state = run_agent("Що таке Read Committed?", decide=decide)
    assert state.stop_reason == "finish"
    assert state.llm_calls == 2
    assert state.observations[0].startswith("read-committed:")


def test_uses_both_actions():
    decide = scripted([
        {"action": "lookup_isolation_level", "arguments": {"name": "read committed"}},
        {"action": "lookup_anomaly", "arguments": {"name": "non-repeatable read"}},
        {"action": "finish", "arguments": {"answer": "ok"}},
    ])
    state = run_agent("Тест", decide=decide)
    assert [r["action"] for r in state.trace] == [
        "lookup_isolation_level", "lookup_anomaly", "finish"]


def test_stops_at_max_steps():
    def endless(goal, observations, step, max_steps):
        return {"action": "lookup_isolation_level", "arguments": {"name": "serializable"}}
    state = run_agent("Зациклитися", decide=endless, max_steps=3)
    assert state.stop_reason == "max_steps"
    assert state.step == 3


def test_stops_at_max_llm_calls():
    def endless(goal, observations, step, max_steps):
        return {"action": "lookup_anomaly", "arguments": {"name": "dirty read"}}
    state = run_agent("Зациклитися", decide=endless, max_steps=10, max_llm_calls=2)
    assert state.stop_reason == "max_llm_calls"
    assert state.llm_calls == 2


def test_invalid_action_becomes_observation():
    decide = scripted([
        {"action": "rm_rf", "arguments": {}},
        {"action": "finish", "arguments": {"answer": "ok"}},
    ])
    state = run_agent("Тест", decide=decide)
    assert state.observations[0].startswith("ERROR: unknown action")
    assert state.stop_reason == "finish"


def test_not_found_is_observation():
    decide = scripted([
        {"action": "lookup_isolation_level", "arguments": {"name": "cursor stability"}},
        {"action": "finish", "arguments": {"answer": "Даних немає."}},
    ])
    state = run_agent("Опиши Cursor Stability", decide=decide)
    assert state.observations[0].startswith("NOT_FOUND")
