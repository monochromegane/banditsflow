from metaflow import FlowSpec, Parameter, step
from metaflow.datastore.inputs import Inputs


class BanditsFlow(FlowSpec):  # type: ignore
    param_actor = Parameter("actor", type=str, multiple=True, help="Name of actor")

    @step
    def start(self) -> None:
        self.next(self.optimize, foreach="param_actor")

    @step
    def optimize(self) -> None:
        self.next(self.evaluate)

    @step
    def evaluate(self) -> None:
        self.next(self.join)

    @step
    def join(self, inputs: Inputs) -> None:
        self.next(self.plot)

    @step
    def plot(self) -> None:
        self.next(self.end)

    @step
    def end(self) -> None:
        pass
