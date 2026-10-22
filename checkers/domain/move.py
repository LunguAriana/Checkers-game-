from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, List, Optional

Coord = Tuple[int, int]  # (row, col), 0..7


@dataclass(frozen=True)
class Move:
    """
    SPEC:
    - A move is a path of squares, length >= 2.
    - Simple move: path length == 2, no captures.
    - Jump move: path length >= 2, each step is a jump of 2 diagonals and captures one piece.
    - captured holds the coordinates of captured enemy pieces in order.
    """
    path: Tuple[Coord, ...]
    captured: Tuple[Coord, ...] = ()

    @property
    def start(self) -> Coord:
        return self.path[0]

    @property
    def end(self) -> Coord:
        return self.path[-1]

    @property
    def is_capture(self) -> bool:
        return len(self.captured) > 0

    def __str__(self) -> str:

        return f"Move(path={self.path}, captured={self.captured})"
