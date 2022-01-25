from typing import Any, Dict, Optional, cast

from metaflow import Flow, Step
from metaflow.client.core import Task

from . import simulator as sim


class BanditsFlowData:
    def __init__(self, experiment_name: str) -> None:
        self.flow_name = "BanditsFlow"
        self.experiment_name = experiment_name

    def latest_best_params(
        self, scenario_name: str, actor_name: str
    ) -> Optional[Dict[str, Any]]:
        task = self._latest_actor_task("evaluate", scenario_name, actor_name)
        if task is None:
            return None

        return cast(Dict[str, Any], task.data.best_params)

    def latest_result(
        self, scenario_name: str, actor_name: str
    ) -> Optional[sim.SimulationResultType]:
        task = self._latest_actor_task("evaluate", scenario_name, actor_name)
        if task is None:
            return None

        return cast(sim.SimulationResultType, task.data.result)

    def _latest_actor_task(
        self, step_name: str, scenario_name: str, actor_name: str
    ) -> Optional[Task]:
        successful_runs = [
            run
            for run in Flow(self.flow_name).runs(
                f"experiment_name:{self.experiment_name}", f"scenario:{scenario_name}"
            )
            if run.successful
        ]
        if len(successful_runs) == 0:
            return None

        latest_successful_run = successful_runs[-1]
        step = Step(f"{self.flow_name}/{latest_successful_run.id}/{step_name}")

        actor_tasks = [task for task in step.tasks() if task.data.actor == actor_name]
        if len(actor_tasks) == 0:
            return None

        return actor_tasks[0]
