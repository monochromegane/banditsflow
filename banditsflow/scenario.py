from typing import Any, Dict, Protocol

LineType = Dict[str, Any]


class Scenario(Protocol):
    def scan(self) -> bool:
        ...

    def line(self) -> LineType:
        ...


class ScenarioLoader(Protocol):
    @staticmethod
    def load(name: str) -> Scenario:
        ...
