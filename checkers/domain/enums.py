from __future__ import annotations
from enum import Enum, auto


class Color(Enum):
    """Player colors."""
    RED = auto()
    BLACK = auto()

    def opponent(self) -> "Color":
        return Color.BLACK if self is Color.RED else Color.RED


class PieceKind(Enum):
    """Piece types."""
    MAN = auto()
    KING = auto()
