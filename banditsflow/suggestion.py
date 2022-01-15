from typing import List, Optional, Protocol, Sequence, TypedDict, Union


class Suggestion(TypedDict):
    name: str
    type_: str


class CategoricalSuggestion(Suggestion):
    choices: Sequence[Union[None, bool, int, float, str]]


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
