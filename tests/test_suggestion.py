from unittest.mock import Mock

from banditsflow import suggestion as suggest


def test_suggest_categorical_is_called_with_parameters() -> None:
    suggestion: suggest.CategoricalSuggestion = {
        "name": "test",
        "type": "categorical",
        "choices": ["a", "b"],
    }
    suggester = suggest.Suggester([suggestion])
    mock_trial = Mock(spec=suggest.Trial)
    _ = suggester.suggest(mock_trial)

    mock_trial.suggest_categorical.assert_called_once_with(
        suggestion["name"], suggestion["choices"]
    )


def test_suggest_discrete_uniform_is_called_with_parameters() -> None:
    suggestion: suggest.DiscreteUniformSuggestion = {
        "name": "test",
        "type": "discrete_uniform",
        "low": 1.0,
        "high": 10.0,
        "q": 0.1,
    }
    suggester = suggest.Suggester([suggestion])
    mock_trial = Mock(spec=suggest.Trial)
    _ = suggester.suggest(mock_trial)

    mock_trial.suggest_discrete_uniform.assert_called_once_with(
        suggestion["name"], suggestion["low"], suggestion["high"], suggestion["q"]
    )


def test_suggest_float_is_called_with_parameters() -> None:
    suggestion: suggest.FloatSuggestion = {
        "name": "test",
        "type": "float",
        "low": 1.0,
        "high": 10.0,
        "step": 0.1,
        "log": True,
    }
    suggester = suggest.Suggester([suggestion])
    mock_trial = Mock(spec=suggest.Trial)
    _ = suggester.suggest(mock_trial)

    mock_trial.suggest_float.assert_called_once_with(
        suggestion["name"],
        suggestion["low"],
        suggestion["high"],
        step=suggestion["step"],
        log=suggestion["log"],
    )


def test_suggest_int_is_called_with_parameters() -> None:
    suggestion: suggest.IntSuggestion = {
        "name": "test",
        "type": "int",
        "low": 1,
        "high": 10,
        "step": 2,
        "log": True,
    }
    suggester = suggest.Suggester([suggestion])
    mock_trial = Mock(spec=suggest.Trial)
    _ = suggester.suggest(mock_trial)

    mock_trial.suggest_int.assert_called_once_with(
        suggestion["name"],
        suggestion["low"],
        suggestion["high"],
        step=suggestion["step"],
        log=suggestion["log"],
    )


def test_suggest_loguniform_is_called_with_parameters() -> None:
    suggestion: suggest.LogUniformSuggestion = {
        "name": "test",
        "type": "loguniform",
        "low": 1.0,
        "high": 10.0,
    }
    suggester = suggest.Suggester([suggestion])
    mock_trial = Mock(spec=suggest.Trial)
    _ = suggester.suggest(mock_trial)

    mock_trial.suggest_loguniform.assert_called_once_with(
        suggestion["name"],
        suggestion["low"],
        suggestion["high"],
    )


def test_suggest_uniform_is_called_with_parameters() -> None:
    suggestion: suggest.LogUniformSuggestion = {
        "name": "test",
        "type": "uniform",
        "low": 1.0,
        "high": 10.0,
    }
    suggester = suggest.Suggester([suggestion])
    mock_trial = Mock(spec=suggest.Trial)
    _ = suggester.suggest(mock_trial)

    mock_trial.suggest_uniform.assert_called_once_with(
        suggestion["name"],
        suggestion["low"],
        suggestion["high"],
    )


def test_suggests_are_not_called() -> None:
    suggester = suggest.Suggester([])
    mock_trial = Mock(spec=suggest.Trial)
    params = suggester.suggest(mock_trial)

    mock_trial.suggest_categorical.assert_not_called()
    mock_trial.suggest_discrete_uniform.assert_not_called()
    mock_trial.suggest_float.assert_not_called()
    mock_trial.suggest_int.assert_not_called()
    mock_trial.suggest_loguniform.assert_not_called()
    mock_trial.suggest_uniform.assert_not_called()

    assert len(params) == 0
