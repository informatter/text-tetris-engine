# Encord Tetris programming challenge

I created my own test suite during development to ensure my solution was getting the expected outputs. I used the sequences provided in the `input.txt` file.

Built against python 3.11.7

## Run using executable

### Install pyinstaller
1. Create virtual environment
2. Activate virtual environment
3. `pip install pyinstaller`

### Create executable

**Install dependencies**

`pip install -r requirements.txt`

**Run the following command:**

`pyinstaller tetris.py`

**This will create two new folders in the root directory:**

`build` and `dist` The exe will be under `dist/tetris`

### Run executable

Windows 🪟

`dist/tetris/tetris.exe 'Q0,Q1'`

Mac 🍎 / Linux 🐧

`dist/tetris/tetris 'Q0,Q1'`

Use `--help for more options`


## Run using python

### Install dependencies
The solution uses the following dependencies:
- pytest
- numpy
- pyinstaller

### Create virtual environment

`python -m venv env`

### Activate virtual environment

Windows 🪟

`env/scripts/activate.ps1`

Mac 🍎 / Linux 🐧

`source env/bin/activate`

### Install dependencies

`pip install -r requirements.txt`

### Run solver

`python tetris.py 'Q0,Q2'`

Use `--help for more options`

# Run tests 🧪

**Solver:**

`pytest tests/tetris_solver_tests.py`

**Polyminoe factory:**

`pytest tests/factory_test.py`