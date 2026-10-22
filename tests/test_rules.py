import unittest
from checkers.domain.board import Board
from checkers.domain.piece import Piece
from checkers.domain.enums import Color, PieceKind
from checkers.domain.rules import Rules


class TestRules(unittest.TestCase):
    def test_mandatory_capture(self):
        b = Board.initial()

        for r in range(8):
            for c in range(8):
                b.set((r, c), None)


        b.set((5, 2), Piece(Color.RED, PieceKind.MAN))
        b.set((4, 3), Piece(Color.BLACK, PieceKind.MAN))

        b.set((3, 4), None)

        moves = Rules.legal_moves(b, Color.RED)
        self.assertTrue(all(m.is_capture for m in moves))
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0].path, ((5, 2), (3, 4)))
        self.assertEqual(moves[0].captured, ((4, 3),))

    def test_multi_jump_generation(self):
        b = Board.initial()
        for r in range(8):
            for c in range(8):
                b.set((r, c), None)

        b.set((5, 2), Piece(Color.RED, PieceKind.MAN))
        b.set((4, 3), Piece(Color.BLACK, PieceKind.MAN))
        b.set((2, 5), Piece(Color.BLACK, PieceKind.MAN))
        # Ensure landings empty
        b.set((3, 4), None)
        b.set((1, 6), None)

        moves = Rules.legal_moves(b, Color.RED)
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0].path, ((5, 2), (3, 4), (1, 6)))
        self.assertEqual(moves[0].captured, ((4, 3), (2, 5)))

    def test_terminal_no_moves(self):
        b = Board.initial()
        for r in range(8):
            for c in range(8):
                b.set((r, c), None)

        b.set((7, 0), Piece(Color.BLACK, PieceKind.MAN))
        self.assertTrue(Rules.is_terminal(b, Color.BLACK))
