# A unit test for the engineLib module.
# Tanner Fry
# tefnq2@mst.edu
import engine
from engine import Game
from engineLib import EngineHandler

import unittest


class TestEngineLib(unittest.TestCase):

    def test_engine_handler(self):
        self.assertRaises(FileNotFoundError, EngineHandler.generate_level, EngineHandler, Game, 1, 1)


if __name__ == '__main__':
    unittest.main()
