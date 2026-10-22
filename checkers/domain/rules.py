from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
from .board import Board, in_bounds, is_dark_square
from .enums import Color
from .move import Move, Coord


@dataclass(frozen=True)
class Rules:
    """
    SPEC (American checkers style):
    - Men move diagonally forward one step (RED forward = decreasing row; BLACK forward = increasing row).
    - Kings move diagonally both directions.
    - Captures are mandatory: if any capture exists for the player, ONLY capture moves are legal.
    - Multi-jump captures are allowed/required when possible: a capture move may include multiple jumps.
    - Winning:
      - Opponent has 0 pieces OR
      - Opponent has no legal moves on their turn.
    """

    @staticmethod
    def legal_moves(board: Board, player: Color) -> List[Move]:
        captures = Rules._all_capture_moves(board, player)
        if captures:
            return captures
        return Rules._all_simple_moves(board, player)

    @staticmethod
    def apply_move(board: Board, move: Move) -> None:
        """
        SPEC:
        - Moves piece along move.path, removes captured pieces, promotes if needed.
        - Assumes move is legal for the current state.
        """
        start = move.start
        piece = board.get(start)
        if piece is None:
            raise ValueError("No piece at move start.")

        board.set(start, None)
        for cap in move.captured:
            board.set(cap, None)

        board.set(move.end, piece)
        board.maybe_promote(move.end)

    @staticmethod
    def is_terminal(board: Board, next_player: Color) -> bool:
        """
        SPEC:
        - Terminal if next_player has no pieces or no legal moves.
        """
        if board.count(next_player) == 0:
            return True
        if not Rules.legal_moves(board, next_player):
            return True
        return False


    @staticmethod
    def _dirs_for_piece(piece_color: Color, is_king: bool) -> List[Tuple[int, int]]:
        if is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        # MEN: RED goes up (row -1), BLACK goes down (row +1)
        dr = -1 if piece_color == Color.RED else 1
        return [(dr, -1), (dr, 1)]

    @staticmethod
    def _all_simple_moves(board: Board, player: Color) -> List[Move]:
        moves: List[Move] = []
        for (r, c), piece in board.pieces_of(player):
            for dr, dc in Rules._dirs_for_piece(piece.color, piece.is_king):
                nr, nc = r + dr, c + dc
                if in_bounds(nr, nc) and is_dark_square(nr, nc) and board.get((nr, nc)) is None:
                    moves.append(Move(path=((r, c), (nr, nc))))
        return moves

    @staticmethod
    def _all_capture_moves(board: Board, player: Color) -> List[Move]:
        moves: List[Move] = []
        for (r, c), piece in board.pieces_of(player):
            moves.extend(Rules._capture_sequences_from(board, (r, c)))
        return moves

    @staticmethod
    def _capture_sequences_from(board: Board, start: Coord) -> List[Move]:
        piece = board.get(start)
        if piece is None:
            return []

        sequences: List[Move] = []

        def dfs(current_board: Board, path: List[Coord], captured: List[Coord]) -> None:
            cur = path[-1]
            p = current_board.get(cur)
            if p is None:
                return

            found_extension = False
            for dr, dc in Rules._dirs_for_piece(p.color, p.is_king):
                mid = (cur[0] + dr, cur[1] + dc)
                land = (cur[0] + 2 * dr, cur[1] + 2 * dc)
                if not (in_bounds(*mid) and in_bounds(*land)):
                    continue
                if not is_dark_square(*land):
                    continue

                mid_piece = current_board.get(mid)
                if mid_piece is None or mid_piece.color == p.color:
                    continue
                if current_board.get(land) is not None:
                    continue


                nb = current_board.clone()
                nb.set(cur, None)
                nb.set(mid, None)
                nb.set(land, p)
                nb.maybe_promote(land)

                found_extension = True
                dfs(nb, path + [land], captured + [mid])

            if not found_extension and captured:
                sequences.append(Move(path=tuple(path), captured=tuple(captured)))

        dfs(board.clone(), [start], [])
        return sequences
