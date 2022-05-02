import importlib
import types
from typing import Any, Dict, List, Optional, Type, cast

from . import actor as act
from . import logger
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
        mute: bool = False,
    ) -> None:
        self.scenario_name = scenario_name

        scenario_loader_module = self.__class__.import_module("scenario.loader")
        self.scenario_loader = cast(
            Type[scenario.ScenarioLoader],
            getattr(scenario_loader_module, "Loader"),  # noqa: B009
        )
        suggestion_loader_module = self.__class__.import_module("suggestion.loader")
        self.suggestion_loader = cast(
            Type[suggest.SuggestionLoader],
            getattr(suggestion_loader_module, "Loader"),  # noqa: B009
        )

        if actor_name is not None:
            self.actor_name: str = actor_name
            actor_loader_module = self.__class__.import_module("actor.loader")
            self.actor_loader = cast(
                Type[act.ActorLoader],
                getattr(actor_loader_module, "Loader"),  # noqa: B009
            )

        if reporter_name is not None:
            self.reporter_name: str = reporter_name
            reporter_loader_module = self.__class__.import_module("reporter.loader")
            self.reporter_loader = cast(
                Type[report.ReporterLoader],
                getattr(reporter_loader_module, "Loader"),  # noqa: B009
            )

        self.logger = logger.Logger(mute=mute)

    def optimize(
        self,
        n_trials: int,
        timeout: float,
        direction: str,
        metric: str,
        seed: int,
        revival: bool = False,
        latest_best_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if latest_best_params is None or revival:
            self.logger.log(
                f"Optimizing parameters for {self.actor_name} on {self.scenario_name} scenario..."
            )
            return self._optimize(n_trials, timeout, direction, metric, seed)
        else:
            self.logger.log(
                f"Use cached parameters for {self.actor_name} on {self.scenario_name} scenario."
            )
            return latest_best_params

    def _optimize(
        self,
        n_trials: int,
        timeout: float,
        direction: str,
        metric: str,
        seed: int,
    ) -> Dict[str, Any]:
        optimizer = optim.Optimizer(
            self.scenario_loader, self.actor_loader, self.suggestion_loader
        )
        study = optimizer.optimize(
            n_trials,
            timeout,
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
        revival: bool = False,
        latest_result: Optional[sim.SimulationResultType] = None,
    ) -> sim.SimulationResultType:
        if latest_result is None or revival:
            self.logger.log(
                f"Evaluating with {self.actor_name} on {self.scenario_name} scenario..."
            )
            return self._evaluate(n_ite, params, callbacks, seed)
        else:
            self.logger.log(
                f"Use cached result with {self.actor_name} on {self.scenario_name} scenario."
            )
            return latest_result

    def _evaluate(
        self,
        n_ite: int,
        params: act.ParamsType,
        callbacks: List[sim.ActionCallbackType],
        seed: int,
    ) -> sim.SimulationResultType:
        simulator = sim.Simulator(self.scenario_loader, self.actor_loader)

        return simulator.run(
            n_ite,
            self.scenario_name,
            self.actor_name,
            params,
            callbacks,
            "evaluate",
            seed,
        )

    def report(
        self, outdir: str, results: Dict[str, sim.SimulationResultType]
    ) -> List[str]:
        reporter = self.reporter_loader.load(self.reporter_name, outdir)

        return reporter.report(results)

    @staticmethod
    def import_module(name: str) -> types.ModuleType:
        return importlib.import_module(name)
