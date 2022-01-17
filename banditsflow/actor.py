from typing import Any, Dict, Protocol, TypedDict, Union

from . import scenario

ParamsType = Dict[str, Union[None, bool, int, float, str]]


class ActionType(TypedDict):
    metric: Dict[str, float]
    result: Dict[str, Any]


class Actor(Protocol):
    def __init__(self, name: str, params: ParamsType, seed: int) -> None:
        ...

    def act(self, line: scenario.LineType) -> ActionType:
        ...


class ActorLoader(Protocol):
    @staticmethod
    def load(name: str, params: ParamsType, seed: int) -> Actor:
        ...
