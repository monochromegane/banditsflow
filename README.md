# BanditsFlow: :slot_machine: A building workflow and tracking its information framework for bandits.

[![Lint and Test](https://github.com/monochromegane/banditsflow/actions/workflows/ci.yml/badge.svg)](https://github.com/monochromegane/banditsflow/actions/workflows/ci.yml)

BanditsFlow is a framework that supports the construction of a typical evaluation workflow for comparing bandit algorithms.
Your experimental modules on this framework are automatically executed in the [Metaflow](https://metaflow.org/) workflow.
In addition, the workflow incorporates experiment management with [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html) and hyperparameter optimization with [Optuna](https://optuna.org/).
Combined with code management using Git, you will be able to manage your experiments with high reproducibility.

## Usage

### 1. Generate scaffold and first run your experiment

```sh
$ YOUR_BANDIT_FLOW_NAME='sample'
$ python -m banditsflow scaffold $YOUR_BANDIT_FLOW_NAME
$ git add .
$ git commit -m 'Initial commit'
$ git tag first-experiment
$ make run
$ mlflow ui
```

And access to http://127.0.0.1:5000

### 2. Customize experiment

1. Implement our scenario.
1. Implement an actor who acts the scenario.
1. Implement a reporter who reports result of actions of the actor.
1. Prepare a parameter suggestion for each actor. (optional)

The scenario, actor and reporter must follow each protocol.
See each protocol ([scenario.Scenario](https://github.com/monochromegane/banditsflow/blob/main/banditsflow/scenario.py), [actor.Actor](https://github.com/monochromegane/banditsflow/blob/main/banditsflow/actor.py) and [reporter.Reporter](https://github.com/monochromegane/banditsflow/blob/main/banditsflow/reporter.py)).

Note that each module has a loader.Loader class which returns its instance by name.

```
├── actor
│   └── loader.py
├── reporter
│   └── loader.py
├── scenario
│   └── loader.py
└── suggestion
    ├── ACTOR_NAME.yml
    └── loader.py
```

### 3. Update experiment and run

```sh
$ git add .
$ git commit -m 'Customize modules'
$ git tag second-experiment
$ make run
$ mlflow ui
```

Repeat 2 and 3.

## Workflow

BanditsFlow provides the following workflow.
The workflow has optimize and evaluate and report steps.
The each step result are saved by Metaflow and MLflow Tracking.

```
                                   ┌─────────┐
                                   │  start  │
                                   └────┬────┘
                         ┌──────────────┼──────────────┐
                     (actor-1)      (actor-2)      (actor-3)
 {suggestion}       ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
 {scenario  } ─────►│optimize │    │optimize │    │optimize ├───► <best_params>
 {actor     }       └────┬────┘    └────┬────┘    └────┬────┘
                    best_params    best_params    best_params
                    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
 {scenario  } ─────►│evaluate │    │evaluate │    │evaluate ├─┬─► <result>
 {actor     }       └────┬────┘    └────┬────┘    └────┬────┘ │
                         │              │              │      ├─► [Parameter]
                      result         result         result    └─► [Metric]
                         └──────────────┼──────────────┘
                                   ┌────┴────┐
                                   │  join   │
                                   └────┬────┘
                                     results
                                   ┌────┴────┐
 {reporter  } ────────────────────►│ report  ├──────────────────► [Artifact]
                                   └────┬────┘
                                   ┌────┴────┐
                                   │   end   │
                                   └─────────┘

{}: Module
[]: MLflow Tracking
<>: Metaflow
```

## Cache

BanditsFlow stores metrics, results and reports for every run.
BanditsFlow assumes that the results are the same for the same experiment, and reduces the time needed to re-run the experiment by using previous results.
These caches are searched using the experiment name, scenario name, and actor name as keys.
You can re-run the experiment by specifying the `--revival_from_optimization_by` or `--revival_from_evaluation_by` option or changing the name of the experiment by setting another git tag).

## Optimization

BanditsFlow uses Optuna for optimization.
Your suggestion loader class returns parameter suggestions for its actor.
If you use the loader made by scaffold, each actor receives its suggestion which is prepared in suggestion module as YAML of its name.
The YAML has `suggestions` dictionary which has list of parameter suggestion dictionary.
Each parameter suggestion has name, type and parameter for each type.

An example of categorical parameter is the following:

```yml
suggestions:
  - name: epsilon
    type: discrete_uniform
    low: 0.1
    high: 1.0
    q: 0.1
```

See [Optuna document](https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html) for other type and parameter for each type.

## Installation

```sh
$ pip install git+https://github.com/monochromegane/banditsflow
```

## License

[MIT](https://github.com/monochromegane/banditsflow/blob/master/LICENSE)

## Author

[monochromegane](https://github.com/monochromegane)
