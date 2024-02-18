from dataclasses import dataclass
import sys
import os
from typing import List

# Add the path to the root directory to sys.path so we can import the from our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from factory import PolyominoeFactory
# rom models import QPolyminoe,JPolyminoe,SPolyminoe,LPolyminoe, IPolyminoe, ZPolyminoe, TPolyminoe, InterfacePolyominoe
from tetris_solver import TetrisSolver
import pytest


@dataclass
class TestCase:
    __test__ = False
    sequence: str
    expected_height: int


@pytest.fixture
def tetris_solver():
    return TetrisSolver()


def test_solver(tetris_solver: TetrisSolver):
    test_cases = [
        TestCase("Q0", 2),
        TestCase("Q0,Q1", 4),
        TestCase("Q0,Q2,Q4,Q6,Q8", 0),
        TestCase("Q0,Q2,Q4,Q6,Q8,Q1", 2),
        TestCase("Q0,Q2,Q4,Q6,Q8,Q1,Q1", 4),
        TestCase("I0,I4,Q8", 1),
        TestCase("I0,I4,Q8,I0,I4", 0),
        TestCase("L0,J2,L4,J6,Q8", 2),
        TestCase("L0,Z1,Z3,Z5,Z7", 2),
        TestCase("T0,T3", 2),
        TestCase("T0,T3,I6,I6", 1),
        TestCase("I0,I6,S4", 1),
        TestCase("T1,Z3,I4", 4),
        TestCase("L0,J3,L5,J8,T1", 3),
        TestCase("L0,J3,L5,J8,T1,T6", 1),
        TestCase("L0,J3,L5,J8,T1,T6,J2,L6,T0,T7", 2),
        TestCase("L0,J3,L5,J8,T1,T6,J2,L6,T0,T7,Q4", 1),
        TestCase("S0,S2,S4,S6", 8),
        TestCase("S0,S2,S4,S5,Q8,Q8,Q8,Q8,T1,Q1,I0,Q4", 8),
        TestCase("L0,J3,L5,J8,T1,T6,S2,Z5,T0,T7", 0),
        # TestCase('Q0,I2,I6,I0,I6,I6,Q2,Q4',2)
    ]

    for test_case in test_cases:
        sequence: str = test_case.sequence
        expected_height: int = test_case.expected_height
        computed_height = tetris_solver.solve(sequence)

        assert computed_height == expected_height
        tetris_solver.reset()
