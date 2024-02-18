from models import (
    QPolyminoe,
    JPolyminoe,
    SPolyminoe,
    LPolyminoe,
    IPolyminoe,
    ZPolyminoe,
    TPolyminoe,
    AbstractPolyominoe,
)


class PolyominoeFactory:
    def __init__(self):
        self.polyominoe_classes = {
            "Q": QPolyminoe,
            "I": IPolyminoe,
            "Z": ZPolyminoe,
            "T": TPolyminoe,
            "S": SPolyminoe,
            "L": LPolyminoe,
            "J": JPolyminoe,
        }

    def create(self, polyomino_type: str) -> AbstractPolyominoe:
        polyomino_class = self.polyominoe_classes.get(polyomino_type)
        if polyomino_class:
            return polyomino_class()
        else:
            raise Exception(f"{polyomino_type} is not implemented in the factory yet!")
