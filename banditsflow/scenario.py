from typing import Any, Dict, Protocol

LineType = Dict[str, Any]
SynopsisType = Dict[str, Any]


class Scenario(Protocol):
    def synopsis(self) -> SynopsisType:
        ...

    def scan(self) -> bool:
        ...

    def line(self) -> LineType:
        ...


class ScenarioLoader(Protocol):
    @staticmethod
    def load(name: str) -> Scenario:
        ...
