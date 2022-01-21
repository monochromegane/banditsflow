from typing import Dict, List, Protocol

from . import simulator as sim


class Reporter(Protocol):
    def __init__(self, outdir: str) -> None:
        ...

    def report(self, results: Dict[str, sim.SimulationResultType]) -> List[str]:
        ...


class ReporterLoader(Protocol):
    @staticmethod
    def load(name: str, outdir: str) -> Reporter:
        ...
