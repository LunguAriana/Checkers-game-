from __future__ import annotations

from typing import Tuple, List
from checkers.domain.move import Move, Coord
from checkers.domain.enums import Color
from checkers.services.game_service import GameService


class Colors:
    RED = "\033[31m"
    RESET = "\033[0m"
    BOLD = "\033[1m"



class ConsoleUI:
    """
    SPEC:
    - Console-only I/O.
    - Protects against invalid input:
      - malformed coordinates
      - illegal moves
      - out-of-turn actions
    - Input format:
      - Enter a move path like: b6-a5   (simple)
      - Or multi-jump like: b6-d4-f2
      Columns: a..h, Rows: 1..8
      Row 1 is bottom (human-friendly). Internally row 0 is top.
    """

    def __init__(self):
        self.game = GameService(human=Color.RED)

    def run(self) -> None:
        print("Checkers: You are RED. Enter moves like b6-a5 or b6-d4-f2. Type 'q' to quit.\n")
        while True:
            self._print_board()
            if self.game.state.winner is not None:
                print(f"\nWinner: {self.game.state.winner.name}")
                return

            if self.game.state.turn == self.game.human:
                print(f"\nYour turn ({self.game.human.name}).")
                legal = self.game.get_legal_moves()
                self._print_hint(legal)

                raw = input("Move> ").strip().lower()
                if raw in ("q", "quit", "exit"):
                    return

                try:
                    mv = self._parse_move(raw)
                    self.game.submit_human_move(mv)
                except Exception as e:
                    print(f"Invalid move: {e}")
            else:
                print(f"\nComputer's turn ({self.game.ai.name})...")
                try:
                    mv = self.game.play_ai_turn()
                    print(f"Computer played: {self._format_path(mv.path)}")
                except Exception as e:
                    print(f"AI error: {e}")

    def _print_hint(self, legal: List[Move]) -> None:
        if not legal:
            print("No legal moves.")
            return
        if any(m.is_capture for m in legal):
            print("Capture is mandatory.")

        examples = ", ".join(self._format_path(m.path) for m in legal[:8])
        if len(legal) > 8:
            examples += ", ..."
        print(f"Legal moves (examples): {examples}")

    def _parse_move(self, s: str) -> Move:
        parts = s.split("-")
        if len(parts) < 2:
            raise ValueError("Move must have at least start-end, e.g. b6-a5")

        path: List[Coord] = [self._parse_square(p) for p in parts]

        legal = self.game.get_legal_moves()
        for mv in legal:
            if list(mv.path) == path:
                return mv
        raise ValueError("That path is not a legal move in the current position.")

    def _parse_square(self, sq: str) -> Coord:
        sq = sq.strip()
        if len(sq) != 2:
            raise ValueError(f"Bad square '{sq}'. Use format like b6.")
        col_ch, row_ch = sq[0], sq[1]
        if col_ch < "a" or col_ch > "h":
            raise ValueError(f"Column must be a..h, got '{col_ch}'.")
        if row_ch < "1" or row_ch > "8":
            raise ValueError(f"Row must be 1..8, got '{row_ch}'.")
        c = ord(col_ch) - ord("a")

        r = 8 - int(row_ch)
        return (r, c)

    def _format_path(self, path: Tuple[Coord, ...]) -> str:
        def fmt(rc: Coord) -> str:
            r, c = rc
            col = chr(ord("a") + c)
            row = str(8 - r)
            return f"{col}{row}"
        return "-".join(fmt(p) for p in path)

    def _print_board(self):
        b = self.game.state.board

        print("\n    a b c d e f g h")
        for r in range(8):
            row_str = []
            for c in range(8):
                p = b.grid[r][c]

                if p is None:
                    ch = "."
                else:
                    if p.color == Color.RED:
                        ch = f"{Colors.RED}{'R' if p.is_king else 'r'}{Colors.RESET}"
                    else:
                        ch = f"{Colors.BOLD}{'B' if p.is_king else 'b'}{Colors.RESET}"

                row_str.append(ch)

            print(f"{8 - r:2}  " + " ".join(row_str) + f"  {8 - r:2}")

        print("    a b c d e f g h")