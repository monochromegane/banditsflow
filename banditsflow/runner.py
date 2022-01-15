import importlib
from typing import Any, Dict, cast

from . import optimizer as optim
from . import suggestion as suggest


class Runner:
    def __init__(self, scenario_name: str, actor_name: str) -> None:
        self.scenario_name = scenario_name
        self.actor_name = actor_name

    def optimize(
        self, n_trials: int, n_ite: int, direction: str, metric: str, seed: int
    ) -> Dict[str, Any]:
        loader = cast(
            suggest.SuggestionLoader, importlib.import_module("suggestion.loader")
        )
        optimizer = optim.Optimizer(self.actor_name, loader)
        study = optimizer.optimize(n_trials, n_ite, direction, metric, seed)

        return study.best_params
