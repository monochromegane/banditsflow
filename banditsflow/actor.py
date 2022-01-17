from typing import Any, Dict, Protocol

from . import scenario
from . import simulator as sim

ActionType = Dict[str, Any]


class Actor(Protocol):
    def __init__(self, name: str, params: sim.ParamsType, seed: int) -> None:
        ...

    def act(self, line: scenario.LineType) -> ActionType:
        ...


class ActorLoader(Protocol):
    @staticmethod
    def load(name: str, params: sim.ParamsType, seed: int) -> Actor:
        ...
