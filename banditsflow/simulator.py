import importlib
from typing import Dict, Union, cast

from . import actor as act
from . import scenario

ParamsType = Dict[str, Union[None, bool, int, float, str]]


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

    def run(self, n_ite: int, params: ParamsType, seed: int) -> None:
        for ite in range(n_ite):
            self._run_simulation(ite, params, seed + ite)

    def _run_simulation(self, current_ite: int, params: ParamsType, seed: int) -> None:
        scenario = self.scenario_loader.load(self.scenario_name)
        actor = self.actor_loader.load(self.actor_name, params, seed)

        while scenario.scan():
            line = scenario.line()
            action = actor.act(line)

            print(action)
