# Encord Tetris programming challenge

## Install dependencies
The solution uses the following dependencies:
- pytest
- numpy

**Activate virtual environment**

Windows 🪟

`env/scripts/activate.ps1`

Mac 🍎 / Linux 🐧

`source env/bin/activate`

**Install from requirements.txt**

`pip install -r requirements.txt`

## Run solver

`python tetris.py 'Q0,Q2'`

## Run tests 🧪

**Solver:**

`pytest tests/tetris_solver_tests.py`

**Polyminoe factory:**

`pytest tests/factory_test.py`