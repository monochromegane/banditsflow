import tempfile
from typing import Dict

import mlflow
from metaflow import FlowSpec, Parameter, current, step
from metaflow.datastore.inputs import Inputs

from . import actor as act
from . import data
from . import runner as run


class BanditsFlow(FlowSpec):  # type: ignore
    param_experiment_name = Parameter(
        "experiment_name",
        type=str,
        required=True,
        help="Name of experiment like a Git tag name.",
    )
    param_experiment_revision = Parameter(
        "experiment_revision",
        type=str,
        required=True,
        help="Revision of experiment like a hash of Git commit",
    )
    param_scenario = Parameter(
        "scenario", type=str, required=True, help="Name of scenario"
    )
    param_actor = Parameter(
        "actor", type=str, required=True, multiple=True, help="Name of actor"
    )
    param_reporter = Parameter(
        "reporter", type=str, required=True, help="Name of reporter"
    )
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
        required=True,
        help="Name of simulation metric for optimization",
    )
    param_revival_optimization_by = Parameter(
        "revival_optimization_by",
        type=str,
        multiple=True,
        help="Name of actor who acts optimization step again for current experiment",
    )
    param_revival_evaluation_by = Parameter(
        "revival_evaluation_by",
        type=str,
        multiple=True,
        help="Name of actor who acts evaluation step again for current experiment",
    )

    @step
    def start(self) -> None:
        self.next(self.optimize, foreach="param_actor")

    @step
    def optimize(self) -> None:
        actor_name = self.input
        self.actor = actor_name

        flow_data = data.BanditsFlowData(self.param_experiment_name)
        latest_best_params = flow_data.latest_best_params(
            self.param_scenario, actor_name
        )

        if (
            latest_best_params is None
            or actor_name in self.param_revival_optimization_by
        ):
            runner = run.Runner(self.param_scenario, actor_name=actor_name)
            self.best_params = runner.optimize(
                self.param_n_trials,
                self.param_optimization_direction,
                self.param_optimization_metric,
                self.param_seed,
            )
        else:
            self.best_params = latest_best_params

        self.next(self.evaluate)

    @step
    def evaluate(self) -> None:
        actor_name = self.input
        self.actor = actor_name
        runner = run.Runner(self.param_scenario, actor_name=actor_name)

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

            flow_data = data.BanditsFlowData(self.param_experiment_name)
            latest_result = flow_data.latest_result(self.param_scenario, actor_name)
            if latest_result is None or actor_name in self.param_revival_evaluation_by:
                self.result = runner.evaluate(
                    self.param_n_ite,
                    self.best_params,
                    [callback],
                    self.param_seed + self.param_n_trials,
                )
            else:
                for current_ite, result in enumerate(latest_result):
                    for current_step, action in enumerate(result):
                        callback(current_ite, current_step, action)
                self.result = latest_result

        self.next(self.join)

    @step
    def join(self, inputs: Inputs) -> None:
        self.results = {input_.actor: input_.result for input_ in inputs}
        self.next(self.report)

    @step
    def report(self) -> None:
        runner = run.Runner(self.param_scenario, reporter_name=self.param_reporter)

        with mlflow.start_run(
            experiment_id=self._experiment_id(),
            run_name=current.run_id,
            tags=self._experiment_tags(),
        ):
            with tempfile.TemporaryDirectory() as dirname:
                report_paths = runner.report(dirname, self.results)

                for path in report_paths:
                    mlflow.log_artifact(path)

        self.next(self.end)

    @step
    def end(self) -> None:
        pass

    def _experiment_id(self) -> str:
        experiment_name = self.param_experiment_name

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
            "experiment_name": self.param_experiment_name,
            "experiment_revision": self.param_experiment_revision,
        }
