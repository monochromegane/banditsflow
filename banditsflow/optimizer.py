from typing import List, Type, cast

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
        n_ite: int,
        scenario_name: str,
        actor_name: str,
        direction: str,
        metric: str,
        seed: int,
    ) -> optuna.study.Study:
        suggestions = self.suggestion_loader.load(actor_name)

        def objective(trial: optuna.trial.Trial) -> float:
            params = suggestions_to_params(suggestions, trial)

            simulator = sim.Simulator(self.scenario_loader, self.actor_loader)
            results = simulator.run(
                n_ite, scenario_name, actor_name, params, [], seed + trial.number
            )

            return to_objective(metric, results)

        study = optuna.create_study(
            direction=direction, sampler=optuna.samplers.TPESampler(seed=seed)
        )
        study.optimize(objective, n_trials=n_trials)

        return study


def suggestions_to_params(
    suggestions: List[suggest.SuggestionType], trial: optuna.trial.Trial
) -> act.ParamsType:
    params: act.ParamsType = {}
    for unknown_suggestion in suggestions:
        name = unknown_suggestion["name"]
        type_ = unknown_suggestion["type_"]

        suggestion: suggest.SuggestionType
        if type_ == "categorical":
            suggestion = cast(suggest.CategoricalSuggestion, unknown_suggestion)
            params[name] = trial.suggest_categorical(name, suggestion["choices"])
        elif type_ == "discrete_uniform":
            suggestion = cast(suggest.DiscreteUniformSuggestion, unknown_suggestion)
            params[name] = trial.suggest_discrete_uniform(
                name, suggestion["low"], suggestion["high"], suggestion["q"]
            )
        elif type_ == "float":
            suggestion = cast(suggest.FloatSuggestion, unknown_suggestion)
            params[name] = trial.suggest_float(
                name,
                suggestion["low"],
                suggestion["high"],
                step=suggestion["step"],
                log=suggestion["log"],
            )
        elif type_ == "int":
            suggestion = cast(suggest.IntSuggestion, unknown_suggestion)
            params[name] = trial.suggest_int(
                name,
                suggestion["low"],
                suggestion["high"],
                step=suggestion["step"],
                log=suggestion["log"],
            )
        elif type_ == "loguniform":
            suggestion = cast(suggest.LogUniformSuggestion, unknown_suggestion)
            params[name] = trial.suggest_loguniform(
                name, suggestion["low"], suggestion["high"]
            )
        elif type_ == "uniform":
            suggestion = cast(suggest.UniformSuggestion, unknown_suggestion)
            params[name] = trial.suggest_uniform(
                name, suggestion["low"], suggestion["high"]
            )

    return params


def to_objective(metric: str, results: sim.SimulationResultType) -> float:
    return 0.0
