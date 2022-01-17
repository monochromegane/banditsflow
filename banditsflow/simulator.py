import importlib
from typing import Dict, List, Protocol, Union, cast

from . import actor as act
from . import scenario

SimulationResultType = List[List[act.ActionType]]


class ActionCallbackType(Protocol):
    def __call__(self, current_ite: int, step: int, action: act.ActionType) -> None:
        ...


class Simulator:
    def __init__(self, scenario_name: str, actor_name: str):
        self.scenario_name = scenario_name
        self.scenario_loader = cast(
            scenario.ScenarioLoader, importlib.import_module("scenario.loader")
        )
        self.actor_name = actor_name
        self.actor_loader = cast(
            act.ActorLoader, importlib.import_module("actor.loader")
        )

    def run(
        self,
        n_ite: int,
        params: act.ParamsType,
        callbacks: List[ActionCallbackType],
        seed: int,
    ) -> SimulationResultType:
        results: SimulationResultType = []
        for ite in range(n_ite):
            result = self._run_scenario(ite, params, callbacks, seed + ite)
            results.append(result)

        return results

    def _run_scenario(
        self,
        current_ite: int,
        params: act.ParamsType,
        callbacks: List[ActionCallbackType],
        seed: int,
    ) -> List[act.ActionType]:
        scenario = self.scenario_loader.load(self.scenario_name)
        actor = self.actor_loader.load(self.actor_name, params, seed)

        result: List[act.ActionType] = []
        while scenario.scan():
            line = scenario.line()
            action = actor.act(line)

            for callback in callbacks:
                callback(current_ite, len(result), action)

            result.append(action)

        return result
