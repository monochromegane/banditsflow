from metaflow import FlowSpec, Parameter, step
from metaflow.datastore.inputs import Inputs

from . import runner as run


class BanditsFlow(FlowSpec):  # type: ignore
    param_scenario = Parameter("scenario", type=str, help="Name of scenario")
    param_actor = Parameter("actor", type=str, multiple=True, help="Name of actor")

    @step
    def start(self) -> None:
        self.next(self.optimize, foreach="param_actor")

    @step
    def optimize(self) -> None:
        actor_name = self.input
        runner = run.Runner(self.param_scenario, actor_name)
        self.best_params = runner.optimize(1, 1, "maximize", "reward", 1)

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
