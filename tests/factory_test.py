import sys
import os

# Add the path to the root directory to sys.path so we can import the from our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from factory import PolyominoeFactory
from models import (
    QPolyminoe,
    JPolyminoe,
    SPolyminoe,
    LPolyminoe,
    IPolyminoe,
    ZPolyminoe,
    TPolyminoe,
    InterfacePolyominoe,
)
import pytest


@pytest.fixture
def polyominoe_factory():
    return PolyominoeFactory()


def test_create_Q_polyominoe(polyominoe_factory: PolyominoeFactory):
    result = polyominoe_factory.create("Q")
    assert isinstance(result, QPolyminoe)


def test_create_I_polyominoe(polyominoe_factory: PolyominoeFactory):
    result = polyominoe_factory.create("I")
    assert isinstance(result, IPolyminoe)


def test_create_Z_polyominoe(polyominoe_factory: PolyominoeFactory):
    result = polyominoe_factory.create("Z")
    assert isinstance(result, ZPolyminoe)


def test_create_T_polyominoe(polyominoe_factory: PolyominoeFactory):
    result = polyominoe_factory.create("T")
    assert isinstance(result, TPolyminoe)


def test_create_S_polyominoe(polyominoe_factory: PolyominoeFactory):
    result = polyominoe_factory.create("S")
    assert isinstance(result, SPolyminoe)


def test_create_L_polyominoe(polyominoe_factory: PolyominoeFactory):
    result = polyominoe_factory.create("L")
    assert isinstance(result, LPolyminoe)


def test_create_J_polyominoe(polyominoe_factory: PolyominoeFactory):
    result = polyominoe_factory.create("J")
    assert isinstance(result, JPolyminoe)


def test_create_unknown_polyominoe(polyominoe_factory: PolyominoeFactory):
    polyominoe_type = "Unknown"
    with pytest.raises(
        Exception, match=f"{polyominoe_type} is not implemented in the factory yet!"
    ):
        polyominoe_factory.create(polyominoe_type)
