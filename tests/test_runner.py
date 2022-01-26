from typing import Any, Dict
from unittest.mock import Mock, patch

from banditsflow import runner


def test_optimize_is_called_when_cache_is_disabled() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor")

        new_best_params = {"status": "new"}
        with patch.object(r, "_optimize", return_value=new_best_params):
            best_params = r.optimize(1, "maximize", "metric", 1)
            assert best_params["status"] == "new"


def test_evaluate_is_called_when_cache_is_disabled() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor")

        new_result = [[{"metric": {"name": 0.0}, "result": {"status": "new"}}]]
        with patch.object(r, "_evaluate", return_value=new_result):
            result = r.evaluate(1, {}, [], 1)
            assert result[0][0]["result"]["status"] == "new"
