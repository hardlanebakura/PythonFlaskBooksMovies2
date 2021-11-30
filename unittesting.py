import unittest

from books import *
from movies import *

class TestModule(unittest.TestCase):

    def testTypeInputs(self):
        '''function should fail on input that are of different type'''
        self.assertRaisesRegex(TypeError, "Expected string input", booksForOneGenre, 1)
        self.assertRaisesRegex(TypeError, "Expected string input", booksForOneGenre, ["1", "1"])
        self.assertRaisesRegex(TypeError, "Expected list input", findUniqueBooks, "1")
        self.assertRaisesRegex(TypeError, "Expected list of books", findUniqueBooks, ["THE LINCOLN HIGHWAY"])
        self.assertRaisesRegex(TypeError, "Expected list input", getMoviesGenres, 1)
        self.assertRaisesRegex(TypeError, "Expected int input", getMoviesGenres, ["1", 1])
        self.assertRaisesRegex(TypeError, "Expected string input", getTopMoviesByGenre, 1)

if (__name__ == "__main__"):
    unittest.main()