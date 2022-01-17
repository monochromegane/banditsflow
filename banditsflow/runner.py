import importlib
from typing import Any, Dict, Type, cast

from . import actor as act
from . import optimizer as optim
from . import scenario
from . import suggestion as suggest


class Runner:
    def __init__(self, scenario_name: str, actor_name: str) -> None:
        self.scenario_name = scenario_name
        self.actor_name = actor_name
        self.scenario_loader = cast(
            Type[scenario.ScenarioLoader], importlib.import_module("scenario.loader")
        )
        self.actor_loader = cast(
            Type[act.ActorLoader], importlib.import_module("actor.loader")
        )
        self.suggestion_loader = cast(
            Type[suggest.SuggestionLoader], importlib.import_module("suggestion.loader")
        )

    def optimize(
        self, n_trials: int, n_ite: int, direction: str, metric: str, seed: int
    ) -> Dict[str, Any]:
        optimizer = optim.Optimizer(
            self.scenario_loader, self.actor_loader, self.suggestion_loader
        )
        study = optimizer.optimize(
            n_trials,
            n_ite,
            self.scenario_name,
            self.actor_name,
            direction,
            metric,
            seed,
        )

        return study.best_params
