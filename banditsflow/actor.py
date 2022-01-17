from typing import Any, Dict, Protocol, TypedDict

from . import scenario
from . import simulator as sim


class ActionType(TypedDict):
    metric: Dict[str, float]
    result: Dict[str, Any]


class Actor(Protocol):
    def __init__(self, name: str, params: sim.ParamsType, seed: int) -> None:
        ...

    def act(self, line: scenario.LineType) -> ActionType:
        ...


class ActorLoader(Protocol):
    @staticmethod
    def load(name: str, params: sim.ParamsType, seed: int) -> Actor:
        ...
