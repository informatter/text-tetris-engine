
from models import QPolyminoe, IPolyminoe, ZPolyminoe, TPolyminoe, InterfacePolyominoe

class PolyominoeFactory:
    def __init__(self):
        pass

    def create(self, polyminoe_type: str) -> InterfacePolyominoe:
        if polyminoe_type == "Q":
            return QPolyminoe()
        if polyminoe_type == "I":
            return IPolyminoe()
        if polyminoe_type == "Z":
            return ZPolyminoe()
        if polyminoe_type == "T":
            return TPolyminoe()
        else:
            raise Exception(f'{polyminoe_type} is not implemented in the factory yet!')