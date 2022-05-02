from typing import Type

import optuna

from . import actor as act
from . import scenario
from . import simulator as sim
from . import suggestion as suggest


class Optimizer:
    def __init__(
        self,
        scenario_loader: Type[scenario.ScenarioLoader],
        actor_loader: Type[act.ActorLoader],
        suggestion_loader: Type[suggest.SuggestionLoader],
    ) -> None:
        self.scenario_loader = scenario_loader
        self.actor_loader = actor_loader
        self.suggestion_loader = suggestion_loader

    def optimize(
        self,
        n_trials: int,
        timeout: float,
        scenario_name: str,
        actor_name: str,
        direction: str,
        metric: str,
        seed: int,
    ) -> optuna.study.Study:
        suggestions = self.suggestion_loader.load(actor_name)
        suggester = suggest.Suggester(suggestions)

        def objective(trial: optuna.trial.Trial) -> float:
            params = suggester.suggest(trial)

            simulator = sim.Simulator(self.scenario_loader, self.actor_loader)
            results = simulator.run(
                1,
                scenario_name,
                actor_name,
                params,
                [],
                "optimize",
                seed,
            )

            return to_objective(metric, results)

        study = optuna.create_study(
            direction=direction, sampler=optuna.samplers.TPESampler(seed=seed)
        )
        study.optimize(
            objective, n_trials=n_trials, timeout=(timeout if timeout > 0.0 else None)
        )

        return study


def to_objective(metric: str, results: sim.SimulationResultType) -> float:
    last_metrics = [result[-1]["metric"] for result in results]
    objective_values = [
        last_metric[metric] for last_metric in last_metrics if metric in last_metric
    ]
    return sum(objective_values) / len(objective_values)
