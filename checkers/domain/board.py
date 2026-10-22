from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple
from .piece import Piece
from .enums import Color, PieceKind
from .move import Coord

BOARD_SIZE = 8


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def is_dark_square(r: int, c: int) -> bool:
    return (r + c) % 2 == 1


@dataclass
class Board:
    """
    SPEC:
    - 8x8 board; pieces only occupy dark squares.
    - None means empty.
    - Board supports querying, moving pieces, and cloning.
    """
    grid: List[List[Optional[Piece]]]

    @staticmethod
    def initial() -> "Board":
        """
        SPEC:
        - Creates standard initial checkers layout:
          BLACK on rows 0..2 on dark squares
          RED   on rows 5..7 on dark squares
        """
        grid: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        for r in range(3):
            for c in range(8):
                if is_dark_square(r, c):
                    grid[r][c] = Piece(Color.BLACK, PieceKind.MAN)
        for r in range(5, 8):
            for c in range(8):
                if is_dark_square(r, c):
                    grid[r][c] = Piece(Color.RED, PieceKind.MAN)
        return Board(grid)

    def clone(self) -> "Board":
        return Board([row[:] for row in self.grid])

    def get(self, pos: Coord) -> Optional[Piece]:
        r, c = pos
        return self.grid[r][c]

    def set(self, pos: Coord, piece: Optional[Piece]) -> None:
        r, c = pos
        self.grid[r][c] = piece

    def pieces_of(self, color: Color) -> List[Tuple[Coord, Piece]]:
        out: List[Tuple[Coord, Piece]] = []
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None and p.color == color:
                    out.append(((r, c), p))
        return out

    def count(self, color: Color) -> int:
        return sum(1 for _, p in self.pieces_of(color))

    def maybe_promote(self, pos: Coord) -> None:
        """
        SPEC:
        - If a MAN reaches the back rank, it becomes a KING.
          RED promotes on row 0, BLACK promotes on row 7.
        """
        p = self.get(pos)
        if p is None or p.is_king:
            return
        r, _ = pos
        if (p.color == Color.RED and r == 0) or (p.color == Color.BLACK and r == 7):
            self.set(pos, p.make_king())
