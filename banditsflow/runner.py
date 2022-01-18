import importlib
from typing import Any, Dict, List, Optional, Type, cast

from . import actor as act
from . import optimizer as optim
from . import reporter as report
from . import scenario
from . import simulator as sim
from . import suggestion as suggest


class Runner:
    def __init__(
        self,
        scenario_name: str,
        *,
        actor_name: Optional[str] = None,
        reporter_name: Optional[str] = None,
    ) -> None:
        self.scenario_name = scenario_name

        self.scenario_loader = cast(
            Type[scenario.ScenarioLoader], importlib.import_module("scenario.loader")
        )
        self.suggestion_loader = cast(
            Type[suggest.SuggestionLoader], importlib.import_module("suggestion.loader")
        )

        if actor_name is not None:
            self.actor_name: str = actor_name
            self.actor_loader = cast(
                Type[act.ActorLoader], importlib.import_module("actor.loader")
            )

        if reporter_name is not None:
            self.reporter_name: str = reporter_name
            self.reporter_loader = cast(
                Type[report.ReporterLoader],
                importlib.import_module("reporter.loader"),
            )

    def optimize(
        self, n_trials: int, direction: str, metric: str, seed: int
    ) -> Dict[str, Any]:
        optimizer = optim.Optimizer(
            self.scenario_loader, self.actor_loader, self.suggestion_loader
        )
        study = optimizer.optimize(
            n_trials,
            self.scenario_name,
            self.actor_name,
            direction,
            metric,
            seed,
        )

        return study.best_params

    def evaluate(
        self,
        n_ite: int,
        params: act.ParamsType,
        callbacks: List[sim.ActionCallbackType],
        seed: int,
    ) -> sim.SimulationResultType:
        simulator = sim.Simulator(self.scenario_loader, self.actor_loader)

        return simulator.run(
            n_ite, self.scenario_name, self.actor_name, params, callbacks, seed
        )

    def report(
        self, outdir: str, results: Dict[str, sim.SimulationResultType]
    ) -> List[str]:
        reporter = self.reporter_loader.load(self.reporter_name, outdir)

        return reporter.report(results)
