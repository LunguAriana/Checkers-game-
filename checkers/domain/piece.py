from __future__ import annotations
from dataclasses import dataclass
from .enums import Color, PieceKind


@dataclass(frozen=True)
class Piece:
    """
    SPEC:
    - A piece belongs to a color and is either MAN or KING.
    - Movement direction for MAN depends on color; KING moves both ways.
    """
    color: Color
    kind: PieceKind = PieceKind.MAN

    @property
    def is_king(self) -> bool:
        return self.kind == PieceKind.KING

    def make_king(self) -> "Piece":
        return Piece(self.color, PieceKind.KING)
