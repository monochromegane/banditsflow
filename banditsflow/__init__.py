from typing import Dict

import mlflow
from metaflow import FlowSpec, Parameter, current, step
from metaflow.datastore.inputs import Inputs

from . import actor as act
from . import runner as run


class BanditsFlow(FlowSpec):  # type: ignore
    param_git_tag = Parameter("git_tag", type=str, help="Name of Git tag")
    param_git_commit = Parameter("git_commit", type=str, help="Hash of Git commit")
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
            self.param_optimization_direction,
            self.param_optimization_metric,
            self.param_seed,
        )

        self.next(self.evaluate)

    @step
    def evaluate(self) -> None:
        actor_name = self.input
        runner = run.Runner(self.param_scenario, actor_name)

        with mlflow.start_run(
            experiment_id=self._experiment_id(),
            run_name=current.run_id,
            tags=self._experiment_tags(),
        ):
            params_for_log = {"scenario": self.param_scenario, "actor": actor_name}
            params_for_log.update(self.best_params)
            mlflow.log_params(params_for_log)

            def callback(current_ite: int, step: int, action: act.ActionType) -> None:
                for key, value in action["metric"].items():
                    mlflow.log_metric(f"{key}_{current_ite}", value, step=step)

            self.results = runner.evaluate(
                self.param_n_ite,
                self.best_params,
                [callback],
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

    def _experiment_id(self) -> str:
        experiment_name = self.param_git_tag

        experiment = mlflow.get_experiment_by_name(experiment_name)
        experiment_id: str
        if experiment is not None:
            experiment_id = experiment.experiment_id
        else:
            experiment_id = mlflow.create_experiment(experiment_name)

        return experiment_id

    def _experiment_tags(self) -> Dict[str, str]:
        return {
            "step": current.step_name,
            "git_tag": self.param_git_tag,
            "git_commit": self.param_git_commit,
        }
