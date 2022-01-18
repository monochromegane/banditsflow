from typing import List

from banditsflow import actor as act
from banditsflow import optimizer
from banditsflow import simulator as sim


def test_to_objective() -> None:
    result_0: List[act.ActionType] = [
        {"metric": {"cum_reward": 1.0, "dummy": 10.0}, "result": {"reward": 1.0}},
        {"metric": {"cum_reward": 1.0, "dummy": 10.0}, "result": {"reward": 0.0}},
        {"metric": {"cum_reward": 2.0, "dummy": 20.0}, "result": {"reward": 1.0}},
    ]
    result_1: List[act.ActionType] = [
        {"metric": {"cum_reward": 1.0, "dummy": 10.0}, "result": {"reward": 1.0}},
        {"metric": {"cum_reward": 2.0, "dummy": 20.0}, "result": {"reward": 1.0}},
        {"metric": {"cum_reward": 3.0, "dummy": 30.0}, "result": {"reward": 1.0}},
    ]
    results: sim.SimulationResultType = [result_0, result_1]

    objective_value = optimizer.to_objective("cum_reward", results)

    assert objective_value == (2.0 + 3.0) / 2
