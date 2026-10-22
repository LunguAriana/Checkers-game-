from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from checkers.domain.board import Board
from checkers.domain.enums import Color
from checkers.domain.move import Move
from checkers.domain.rules import Rules
from .ai_service import AIService


@dataclass
class GameState:
    board: Board
    turn: Color
    winner: Optional[Color] = None


class GameService:
    """
    SPEC:
    - Owns the game state.
    - Exposes:
      - get_legal_moves()
      - submit_human_move(move): validates & applies; updates winner/turn
      - play_ai_turn(): asks AI for move; applies; updates winner/turn
    - No console I/O here.
    """

    def __init__(self, human: Color = Color.RED):
        self.human = human
        self.ai = human.opponent()
        self.state = GameState(board=Board.initial(), turn=Color.RED)
        self.ai_service = AIService(ai_color=self.ai)

    def get_legal_moves(self) -> List[Move]:
        if self.state.winner is not None:
            return []
        return Rules.legal_moves(self.state.board, self.state.turn)

    def submit_human_move(self, move: Move) -> None:
        if self.state.winner is not None:
            raise ValueError("Game is over.")
        if self.state.turn != self.human:
            raise ValueError("Not human's turn.")

        legal = self.get_legal_moves()
        if move not in legal:
            raise ValueError("Illegal move.")

        Rules.apply_move(self.state.board, move)
        self._advance_turn()

    def play_ai_turn(self) -> Move:
        if self.state.winner is not None:
            raise ValueError("Game is over.")
        if self.state.turn != self.ai:
            raise ValueError("Not AI's turn.")

        legal = self.get_legal_moves()
        if not legal:

            self.state.winner = self.human
            raise ValueError("AI has no legal moves.")

        chosen = self.ai_service.choose_move(self.state.board, legal)
        Rules.apply_move(self.state.board, chosen)
        self._advance_turn()
        return chosen

    def _advance_turn(self) -> None:
        self.state.turn = self.state.turn.opponent()
        "it checks if the opponent is dead"
        if Rules.is_terminal(self.state.board, self.state.turn):
            self.state.winner = self.state.turn.opponent()
