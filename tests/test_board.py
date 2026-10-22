import unittest
from checkers.domain.board import Board
from checkers.domain.enums import Color, PieceKind
from checkers.domain.piece import Piece


class TestBoard(unittest.TestCase):
    def test_initial_counts(self):
        b = Board.initial()
        self.assertEqual(b.count(Color.RED), 12)
        self.assertEqual(b.count(Color.BLACK), 12)

    def test_promotion(self):
        b = Board.initial()

        b.set((1, 2), Piece(Color.RED, PieceKind.MAN))
        b.set((0, 1), None)
        b.set((1, 2), None)
        b.set((0, 1), Piece(Color.RED, PieceKind.MAN))
        b.maybe_promote((0, 1))
        self.assertTrue(b.get((0, 1)).is_king)
