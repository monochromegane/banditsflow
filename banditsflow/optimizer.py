from typing import Dict, List, Union, cast

import optuna

from . import suggestion as suggest

ParamsType = Dict[str, Union[None, bool, int, float, str]]


class Optimizer:
    def __init__(self, actor_name: str, loader: suggest.SuggestionLoader) -> None:
        self.actor_name = actor_name
        self.loader = loader

    def optimize(self, n_trials: int, n_ite: int, direction: str, metric: str) -> None:
        suggestions = self.loader.load(self.actor_name)

        def objective(trial: optuna.trial.Trial) -> float:
            params = suggestions_to_params(suggestions, trial)

            print(params)
            return 0.0


def suggestions_to_params(
    suggestions: List[suggest.SuggestionType], trial: optuna.trial.Trial
) -> ParamsType:
    params: ParamsType = {}
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