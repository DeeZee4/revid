import threading
from ais.template import turn
from game.board import Board
from settings import Settings as s
import importlib

class AI():
    def get_turn(self, board:Board, me):
        mod = importlib.import_module(f"ais.{s.ais[me.id]}")
        turn = getattr(mod, "turn")
        return turn(board, me.id)