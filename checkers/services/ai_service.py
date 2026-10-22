from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from checkers.domain.board import Board
from checkers.domain.enums import Color
from checkers.domain.move import Move
from checkers.domain.rules import Rules


@dataclass
class AIService:
    """
    SPEC (strategy, not optimal):
    1) If any AI move wins immediately, play it.
    2) Otherwise, avoid moves that allow the human to win immediately next turn (block 1-move victory).
    3) Otherwise, prefer:
       - captures (already enforced by rules if any exist)
       - promotions
       - more captures in a sequence
       - central squares (rough heuristic)
    """
    ai_color: Color

    def choose_move(self, board: Board, legal_moves: List[Move]) -> Move:

        for mv in legal_moves:
            b2 = board.clone()
            Rules.apply_move(b2, mv)
            if Rules.is_terminal(b2, self.ai_color.opponent()):
                return mv


        safe_moves: List[Move] = []
        min_opponent_winning_replies = 10**9

        for mv in legal_moves:
            b2 = board.clone()
            Rules.apply_move(b2, mv)

            opp = self.ai_color.opponent()
            opp_moves = Rules.legal_moves(b2, opp)

            winning_replies = 0
            for omv in opp_moves:
                b3 = b2.clone()
                Rules.apply_move(b3, omv)
                if Rules.is_terminal(b3, self.ai_color):
                    winning_replies += 1

            if winning_replies < min_opponent_winning_replies:
                min_opponent_winning_replies = winning_replies
                safe_moves = [mv]
            elif winning_replies == min_opponent_winning_replies:
                safe_moves.append(mv)

        candidates = safe_moves if safe_moves else legal_moves


        scored: List[Tuple[int, Move]] = [(self._score_move(board, mv), mv) for mv in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    def _score_move(self, board: Board, mv: Move) -> int:
        b2 = board.clone()
        before_piece = b2.get(mv.start)
        Rules.apply_move(b2, mv)
        after_piece = b2.get(mv.end)

        score = 0
        if mv.is_capture:
            score += 50 + 10 * len(mv.captured)


        if before_piece is not None and after_piece is not None:
            if (not before_piece.is_king) and after_piece.is_king:
                score += 40


        r, c = mv.end
        score += 7 - (abs(3.5 - r) + abs(3.5 - c))  # higher near center

        return int(score)
