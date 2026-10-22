import unittest
from checkers.domain.board import Board
from checkers.domain.piece import Piece
from checkers.domain.enums import Color, PieceKind
from checkers.domain.rules import Rules
from checkers.services.ai_service import AIService


class TestAI(unittest.TestCase):
    def test_ai_takes_immediate_win(self):
        b = Board.initial()
        # Clear board and set up: AI (BLACK) can capture last red piece and win
        for r in range(8):
            for c in range(8):
                b.set((r, c), None)

        b.set((2, 1), Piece(Color.BLACK, PieceKind.MAN))
        b.set((3, 2), Piece(Color.RED, PieceKind.MAN))
        # landing
        b.set((4, 3), None)

        legal = Rules.legal_moves(b, Color.BLACK)
        ai = AIService(ai_color=Color.BLACK)
        mv = ai.choose_move(b, legal)

        # After applying, red has 0 pieces => terminal for red
        b2 = b.clone()
        Rules.apply_move(b2, mv)
        self.assertTrue(Rules.is_terminal(b2, Color.RED))

    def test_ai_blocks_opponent_immediate_win_when_possible(self):
        b = Board([[None for _ in range(8)] for _ in range(8)])
        b.set((2, 1), Piece(Color.BLACK, PieceKind.MAN))
        b.set((4, 3), Piece(Color.RED, PieceKind.MAN))
        legal = Rules.legal_moves(b, Color.BLACK)
        # (3, 2) exposes the last BLACK piece to a capture; (3, 0) is safe.
        self.assertEqual({move.end for move in legal}, {(3, 0), (3, 2)})
        unsafe = next(move for move in legal if move.end == (3, 2))
        bad_board = b.clone()
        Rules.apply_move(bad_board, unsafe)
        reply = next(move for move in Rules.legal_moves(bad_board, Color.RED) if move.is_capture)
        Rules.apply_move(bad_board, reply)
        self.assertTrue(Rules.is_terminal(bad_board, Color.BLACK))
        move = AIService(ai_color=Color.BLACK).choose_move(b, legal)
        self.assertEqual(move.end, (3, 0))
        Rules.apply_move(b, move)
        for reply in Rules.legal_moves(b, Color.RED):
            after = b.clone()
            Rules.apply_move(after, reply)
            self.assertFalse(Rules.is_terminal(after, Color.BLACK))
