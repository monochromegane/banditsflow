from typing import List, Optional, Protocol, Sequence, TypedDict, Union, cast

from . import actor as act

CategoricalChoiceType = Union[None, bool, int, float, str]


class Suggestion(TypedDict):
    name: str
    type_: str


class CategoricalSuggestion(Suggestion):
    choices: Sequence[CategoricalChoiceType]


class DiscreteUniformSuggestion(Suggestion):
    low: float
    high: float
    q: float


class FloatSuggestion(Suggestion):
    low: float
    high: float
    step: Optional[float]
    log: bool


class IntSuggestion(Suggestion):
    low: int
    high: int
    step: int
    log: bool


class LogUniformSuggestion(Suggestion):
    low: float
    high: float


class UniformSuggestion(Suggestion):
    low: float
    high: float


SuggestionType = Union[
    CategoricalSuggestion,
    DiscreteUniformSuggestion,
    FloatSuggestion,
    IntSuggestion,
    LogUniformSuggestion,
    UniformSuggestion,
]


class SuggestionLoader(Protocol):
    @staticmethod
    def load(name: str) -> List[SuggestionType]:
        ...


class Trial(Protocol):
    def suggest_categorical(
        self, name: str, choices: Sequence[CategoricalChoiceType]
    ) -> CategoricalChoiceType:
        ...

    def suggest_discrete_uniform(
        self, name: str, low: float, high: float, q: float
    ) -> float:
        ...

    def suggest_float(
        self,
        name: str,
        low: float,
        high: float,
        *,
        step: Optional[float] = None,
        log: bool = False,
    ) -> float:
        ...

    def suggest_int(
        self, name: str, low: int, high: int, step: int = 1, log: bool = False
    ) -> int:
        ...

    def suggest_loguniform(self, name: str, low: float, high: float) -> float:
        ...

    def suggest_uniform(self, name: str, low: float, high: float) -> float:
        ...


class Suggester:
    def __init__(self, suggestions: List[SuggestionType]) -> None:
        self.suggestions = suggestions

    def suggest(self, trial: Trial) -> act.ParamsType:
        params: act.ParamsType = {}
        for unknown_suggestion in self.suggestions:
            name = unknown_suggestion["name"]
            type_ = unknown_suggestion["type_"]

            suggestion: SuggestionType
            if type_ == "categorical":
                suggestion = cast(CategoricalSuggestion, unknown_suggestion)
                params[name] = self._suggest_categorical(name, suggestion, trial)
            elif type_ == "discrete_uniform":
                suggestion = cast(DiscreteUniformSuggestion, unknown_suggestion)
                params[name] = self._suggest_discrete_uniform(name, suggestion, trial)
            elif type_ == "float":
                suggestion = cast(FloatSuggestion, unknown_suggestion)
                params[name] = self._suggest_float(name, suggestion, trial)
            elif type_ == "int":
                suggestion = cast(IntSuggestion, unknown_suggestion)
                params[name] = self._suggest_int(name, suggestion, trial)
            elif type_ == "loguniform":
                suggestion = cast(LogUniformSuggestion, unknown_suggestion)
                params[name] = self._suggest_loguniform(name, suggestion, trial)
            elif type_ == "uniform":
                suggestion = cast(UniformSuggestion, unknown_suggestion)
                params[name] = self._suggest_uniform(name, suggestion, trial)

        return params

    def _suggest_categorical(
        self, name: str, suggestion: CategoricalSuggestion, trial: Trial
    ) -> CategoricalChoiceType:
        return trial.suggest_categorical(name, suggestion["choices"])

    def _suggest_discrete_uniform(
        self, name: str, suggestion: DiscreteUniformSuggestion, trial: Trial
    ) -> float:
        return trial.suggest_discrete_uniform(
            name, suggestion["low"], suggestion["high"], suggestion["q"]
        )

    def _suggest_float(
        self, name: str, suggestion: FloatSuggestion, trial: Trial
    ) -> float:
        return trial.suggest_float(
            name,
            suggestion["low"],
            suggestion["high"],
            step=suggestion["step"],
            log=suggestion["log"],
        )

    def _suggest_int(self, name: str, suggestion: IntSuggestion, trial: Trial) -> int:
        return trial.suggest_int(
            name,
            suggestion["low"],
            suggestion["high"],
            step=suggestion["step"],
            log=suggestion["log"],
        )

    def _suggest_loguniform(
        self, name: str, suggestion: LogUniformSuggestion, trial: Trial
    ) -> float:
        return trial.suggest_loguniform(name, suggestion["low"], suggestion["high"])

    def _suggest_uniform(
        self, name: str, suggestion: UniformSuggestion, trial: Trial
    ) -> float:
        return trial.suggest_uniform(name, suggestion["low"], suggestion["high"])
