from typing import Any, Dict, List
from unittest.mock import Mock, patch

from banditsflow import actor as act
from banditsflow import runner


def test_optimize_is_not_called_when_revival_false_and_cache_is_found() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor", mute=True)

        new_best_params = {"status": "new"}
        latest_best_params = {"status": "latest"}
        with patch.object(r, "_optimize") as mock_optimize:
            mock_optimize.return_value = new_best_params
            best_params = r.optimize(
                1,
                "maximize",
                "metric",
                1,
                revival=False,
                latest_best_params=latest_best_params,
            )

            mock_optimize.assert_not_called()
            assert best_params["status"] == "latest"


def test_optimize_is_called_when_revival_false_and_cache_is_not_found() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor", mute=True)

        new_best_params = {"status": "new"}
        with patch.object(r, "_optimize") as mock_optimize:
            mock_optimize.return_value = new_best_params
            best_params = r.optimize(
                1, "maximize", "metric", 1, revival=False, latest_best_params=None
            )
            mock_optimize.assert_called_once()
            assert best_params["status"] == "new"


def test_optimize_is_called_when_revival_true_and_cache_is_not_found() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor", mute=True)

        new_best_params = {"status": "new"}
        with patch.object(r, "_optimize") as mock_optimize:
            mock_optimize.return_value = new_best_params
            best_params = r.optimize(
                1, "maximize", "metric", 1, revival=True, latest_best_params=None
            )
            mock_optimize.assert_called_once()
            assert best_params["status"] == "new"


def test_optimize_is_called_when_revival_true_and_cache_is_found() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor", mute=True)

        new_best_params = {"status": "new"}
        latest_best_params = {"status": "latest"}
        with patch.object(r, "_optimize") as mock_optimize:
            mock_optimize.return_value = new_best_params
            best_params = r.optimize(
                1,
                "maximize",
                "metric",
                1,
                revival=True,
                latest_best_params=latest_best_params,
            )
            mock_optimize.assert_called_once()
            assert best_params["status"] == "new"


def test_evaluate_is_called_when_revival_false_and_cache_is_found() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor", mute=True)

        new_result = [[{"metric": {"name": 0.0}, "result": {"status": "new"}}]]
        latest_result: List[List[act.ActionType]] = [
            [{"metric": {"name": 0.0}, "result": {"status": "latest"}}]
        ]
        callback = Mock()
        with patch.object(r, "_evaluate") as mock_evaluate:
            mock_evaluate.return_value = new_result
            result = r.evaluate(
                1, {}, [callback], 1, revival=False, latest_result=latest_result
            )
            mock_evaluate.assert_not_called()
            callback.assert_not_called()
            assert result[0][0]["result"]["status"] == "latest"


def test_evaluate_is_called_when_revival_false_and_cache_is_not_found() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor", mute=True)

        new_result = [[{"metric": {"name": 0.0}, "result": {"status": "new"}}]]
        with patch.object(r, "_evaluate") as mock_evaluate:
            mock_evaluate.return_value = new_result
            result = r.evaluate(1, {}, [], 1, revival=False, latest_result=None)
            mock_evaluate.assert_called_once()
            assert result[0][0]["result"]["status"] == "new"


def test_evaluate_is_called_when_revival_true_and_cache_is_not_found() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor", mute=True)

        new_result = [[{"metric": {"name": 0.0}, "result": {"status": "new"}}]]
        with patch.object(r, "_evaluate") as mock_evaluate:
            mock_evaluate.return_value = new_result
            result = r.evaluate(1, {}, [], 1, revival=True, latest_result=None)
            mock_evaluate.assert_called_once()
            assert result[0][0]["result"]["status"] == "new"


def test_evaluate_is_called_when_revival_true_and_cache_is_found() -> None:
    class MockLoaderModule:
        Loader: Dict[Any, Any] = {}

    with patch.object(runner.Runner, "import_module", return_value=MockLoaderModule):
        r = runner.Runner("scenario", actor_name="actor", mute=True)

        new_result = [[{"metric": {"name": 0.0}, "result": {"status": "new"}}]]
        latest_result: List[List[act.ActionType]] = [
            [{"metric": {"name": 0.0}, "result": {"status": "latest"}}]
        ]
        with patch.object(r, "_evaluate") as mock_evaluate:
            mock_evaluate.return_value = new_result
            result = r.evaluate(1, {}, [], 1, revival=True, latest_result=latest_result)
            mock_evaluate.assert_called_once()
            assert result[0][0]["result"]["status"] == "new"
