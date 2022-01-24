import pathlib
import tempfile
from typing import List

import pytest
from banditsflow import scaffold


def test_build() -> None:
    name = "sample_bandit"
    src_dir = "banditsflow/templates"

    expect_paths: List[str] = [
        "scenario/__init__.py",
        "scenario/loader.py",
        "suggestion/__init__.py",
        "suggestion/loader.py",
        "suggestion/epsilon_greedy.yml",
        "actor/__init__.py",
        "actor/loader.py",
        "reporter/__init__.py",
        "reporter/loader.py",
        "__main__.py",
    ]
    class_name_paths = ["scenario/loader.py", "reporter/loader.py"]

    with tempfile.TemporaryDirectory() as dest_dir:
        scaffold.Builder().build(name, src_dir, dest_dir)

        dest_paths = list(pathlib.Path(dest_dir).glob("**/*.*"))
        assert len(dest_paths) == len(expect_paths)

        relative_pathnames = [
            str(dest_path.relative_to(dest_dir)) for dest_path in dest_paths
        ]
        for expect_path in expect_paths:
            assert expect_path in relative_pathnames

        for relative_pathname, dest_path in zip(relative_pathnames, dest_paths):
            if relative_pathname in class_name_paths:
                with dest_path.open(mode="r") as f:
                    match_lines = [
                        line for line in f.readlines() if "SampleBandit" in line
                    ]
                    assert len(match_lines) > 0


@pytest.mark.parametrize(
    ("snake", "title"),
    [
        ("sample", "Sample"),
        ("sample_bandit", "SampleBandit"),
    ],
)
def test_title_case(snake: str, title: str) -> None:
    assert scaffold.Builder.to_title_case(snake) == title
