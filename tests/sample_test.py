"""
An automated test suite will be run against your submission. To make sure that it will run well 
please
* Add installation instructions to make your `tetris` executable runnable into the README.md.
    If you are using Python you might also include the dependencies you are introducing
    with a `requirements.txt` file.
* Run these sample tests against the executable you have produced. Please note, if you're using
    Windows you will need to modify the `subprocess.run` command accordingly.
"""

import subprocess
from dataclasses import dataclass
from typing import Iterable
import platform
import os

ENTRY_POINT = "dist/tetris/tetris"
ENTRY_POINT_WINDOWS = "dist/tetris/tetris.exe"


@dataclass
class TestCase:
    name: str
    sample_input: str
    sample_output: Iterable[int]


def run_test(test_case: TestCase):
    completed_process = None
    if platform.system() in ["Linux", "Darwin"]:  # Linux or macOS
        completed_process = subprocess.run(
            ["/bin/bash", ENTRY_POINT],
            input=test_case.sample_input.encode("utf-8"),
            capture_output=True,
        )
    elif platform.system() == "Windows":
        exe_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), "..", "dist", "tetris", "tetris.exe"
            )
        )

        command = f"powershell -Command \"& '{exe_path}' {test_case.sample_input}\""
        completed_process = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    else:
        raise OSError("Unsupported operating system")

    output = [int(line) for line in completed_process.stdout.splitlines()]

    assert output == [
        test_case.sample_output
    ], f"The test with name `{test_case.name}` failed."


if __name__ == "__main__":
    test_cases = [
        TestCase("simple test", "Q0", 2),
        TestCase("Many blocks test", ",".join(["Q0"] * 5), 10),
    ]
    for test_case in test_cases:
        run_test(test_case)
