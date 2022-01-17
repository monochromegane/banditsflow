from unittest.mock import Mock, call

from banditsflow import actor as act
from banditsflow import scenario
from banditsflow import simulator as sim


class DummyScenarioLoader:
    @staticmethod
    def load(name: str) -> scenario.Scenario:
        return DummyScenario()


class DummyScenario:
    def __init__(self) -> None:
        self.i = -1

    def scan(self) -> bool:
        self.i += 1
        return self.i < 2

    def line(self) -> scenario.LineType:
        return {"i": self.i}


class DummyEchoActorLoader:
    @staticmethod
    def load(name: str, params: act.ParamsType, seed: int) -> act.Actor:
        return DummyEchoActor(name, params, seed)


class DummyEchoActor:
    def __init__(self, name: str, params: act.ParamsType, seed: int) -> None:
        self.name = name
        self.params = params
        self.seed = seed

    def act(self, line: scenario.LineType) -> act.ActionType:
        return {"metric": line, "result": line}


def test_actor_receives_scenario_lines_in_run_scenario() -> None:
    simulator = sim.Simulator(DummyScenarioLoader, DummyEchoActorLoader)
    result = simulator._run_scenario(0, "", "", {}, [], 0)
    assert len(result) == 2  # Number of scenario lines
    assert result[0]["metric"]["i"] == 0  # Content of scenario line 0
    assert result[1]["metric"]["i"] == 1  # Content of scenario line 1


def test_callbacks_are_called_with_parameters_in_run_scenario() -> None:
    simulator = sim.Simulator(DummyScenarioLoader, DummyEchoActorLoader)
    callback_0 = Mock()
    callback_1 = Mock()
    current_ite = 0
    result = simulator._run_scenario(
        current_ite, "", "", {}, [callback_0, callback_1], 0
    )

    assert callback_0.call_count == 2
    list_args = callback_0.call_args_list
    for i in range(2):
        assert call(current_ite, i, {"metric": {"i": i}, "result": {"i": i}})

    assert callback_1.call_count == 2
    list_args = callback_1.call_args_list
    for i in range(2):
        assert call(current_ite, i, {"metric": {"i": i}, "result": {"i": i}})
