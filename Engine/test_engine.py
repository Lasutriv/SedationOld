# A unit test for the engine module.
# Tanner Fry
# tefnq2@mst.edu
import engine
import unittest


class TestEngine(unittest.TestCase):

    def test_main(self):
        self.assertEqual(engine.main(), 0)


if __name__ == '__main__':
    unittest.main()
