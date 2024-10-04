import unittest
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from FSA import *

class TestFSA(unittest.TestCase):
    def setUp(self):
        pass
    
    def testsRejects(self):
        fsa = compileRE('a(b|c*)')
        self.assertFalse(fsa.accepts("abbb"))

    def testDeterminization(self):
        states = [0, 1, 2, 3]
        alphabet = ['a']
        transitions = [(0, 1, 'a'),
                       (0, 2, 'a'),
                       (1, 0, 'b'),
                       (1, 3, 'a'),
                       (2, 0, 'a'),
                       (2, 2, 'b'),
                       (2, 3, 'a')]
        initialState = 0
        finalStates = [3]
        fsa = FSA(states, alphabet, transitions, initialState, finalStates)
        self.assertTrue(fsa.accepts('aba'))
        dfa = fsa.determinized()
        self.assertTrue(dfa.accepts('aba'))

    def testMinimization(self):
        fsa = concatenation(singleton("a"),minimize(closure(singleton("b"))))
        self.assertFalse(fsa.accepts("b"))
        fsa = concatenation(singleton("a"),closure(singleton("b")))
        self.assertFalse(fsa.accepts("b"))

class TestParseRE(unittest.TestCase):
    def testBasic(self):
        from reCompiler import compileRE

        odd_len = compileRE(".(..)*")
        self.assertFalse(odd_len.isEmpty())
        self.assertTrue(odd_len.accepts("aaa"))
        self.assertFalse(odd_len.accepts("aaaa"))

        self.assertTrue(compileRE('[0-5]').accepts('3'))
        self.assertFalse(compileRE('[0-5]').accepts('7'))

        self.assertTrue(compileRE(r'.').accepts('a'))
        self.assertFalse(compileRE(r'\.').accepts('a'))


    def testCustomNumberOfOccurrences(self):
        from reCompiler import compileRE

        self.assertTrue(compileRE('a{1,3}').accepts('aa'))
        self.assertFalse(compileRE('a{1,3}').accepts(''))
        self.assertTrue(compileRE('a{1,3}').accepts('a'))
        self.assertFalse(compileRE('a{1,3}').accepts('aaaa'))
        self.assertTrue(compileRE('a{1,3}').accepts('aaa'))

        self.assertTrue(compileRE('a{0,2}').accepts('aa'))
        self.assertTrue(compileRE('a{0,2}').accepts(''))
        self.assertTrue(compileRE('a{0,2}').accepts('a'))
        self.assertFalse(compileRE('a{0,2}').accepts('aaa'))

        self.assertFalse(compileRE('a{3}').accepts('aa'))
        self.assertFalse(compileRE('a{3}').accepts('aaaa'))
        self.assertTrue(compileRE('a{3}').accepts('aaa'))

    def testMetacharactersInSet(self):
        from reCompiler import compileRE

        self.assertTrue(compileRE(r'\w+').accepts('aa'))
        self.assertTrue(compileRE(r'[\w]+').accepts('aa'))
        self.assertFalse(compileRE(r'[\w]+').accepts('a a'))

        self.assertTrue(compileRE(r'\t').accepts('\t'))
        self.assertTrue(compileRE(r'[\t]').accepts('\t'))
        self.assertFalse(compileRE(r'[\t]').accepts('\v'))

if __name__ == '__main__':
    unittest.main()
