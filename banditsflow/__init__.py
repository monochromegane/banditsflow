from metaflow import FlowSpec, Parameter, step
from metaflow.datastore.inputs import Inputs

from . import runner as run


class BanditsFlow(FlowSpec):  # type: ignore
    param_scenario = Parameter("scenario", type=str, help="Name of scenario")
    param_actor = Parameter("actor", type=str, multiple=True, help="Name of actor")
    param_n_ite = Parameter("n_ite", type=int, default=1, help="Number of simulation")
    param_seed = Parameter("seed", type=int, default=1, help="Seed of seed")
    param_n_trials = Parameter(
        "n_trials", type=int, default=1, help="Number of optimization"
    )
    param_optimization_direction = Parameter(
        "optimization_direction",
        type=str,
        default="maximize",
        help="Name of direction for optimization",
    )
    param_optimization_metric = Parameter(
        "optimization_metric",
        type=str,
        help="Name of simulation metric for optimization",
    )

    @step
    def start(self) -> None:
        self.next(self.optimize, foreach="param_actor")

    @step
    def optimize(self) -> None:
        actor_name = self.input
        runner = run.Runner(self.param_scenario, actor_name)
        self.best_params = runner.optimize(
            self.param_n_trials,
            self.param_n_ite,
            self.param_optimization_direction,
            self.param_optimization_metric,
            self.param_seed,
        )

        self.next(self.evaluate)

    @step
    def evaluate(self) -> None:
        actor_name = self.input
        runner = run.Runner(self.param_scenario, actor_name)
        self.results = runner.evaluate(
            self.param_n_ite,
            self.best_params,
            [],
            self.param_seed + self.param_n_trials,
        )

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
