from typing import List, Protocol, Type

from . import actor as act
from . import scenario

SimulationResultType = List[List[act.ActionType]]


class ActionCallbackType(Protocol):
    def __call__(self, current_ite: int, step: int, action: act.ActionType) -> None:
        ...


class Simulator:
    def __init__(
        self,
        scenario_loader: Type[scenario.ScenarioLoader],
        actor_loader: Type[act.ActorLoader],
    ) -> None:
        self.scenario_loader = scenario_loader
        self.actor_loader = actor_loader

    def run(
        self,
        n_ite: int,
        scenario_name: str,
        actor_name: str,
        params: act.ParamsType,
        callbacks: List[ActionCallbackType],
        seed: int,
    ) -> SimulationResultType:
        results: SimulationResultType = []
        for ite in range(n_ite):
            result = self._run_scenario(
                ite, scenario_name, actor_name, params, callbacks, seed + ite
            )
            results.append(result)

        return results

    def _run_scenario(
        self,
        current_ite: int,
        scenario_name: str,
        actor_name: str,
        params: act.ParamsType,
        callbacks: List[ActionCallbackType],
        seed: int,
    ) -> List[act.ActionType]:
        scenario = self.scenario_loader.load(scenario_name)
        actor = self.actor_loader.load(actor_name, params, seed)

        result: List[act.ActionType] = []
        while scenario.scan():
            line = scenario.line()
            action = actor.act(line)

            for callback in callbacks:
                callback(current_ite, len(result), action)

            result.append(action)

        return result
