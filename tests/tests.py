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

        self.assertFalse(compileRE(r'[^a]').accepts('a'))
        self.assertTrue(compileRE(r'[^a]').accepts('b'))


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
        self.assertTrue(compileRE(r'[\w ]+').accepts('a a'))
        self.assertFalse(compileRE(r'[\w]+').accepts('a a'))

        self.assertTrue(compileRE(r'\t').accepts('\t'))
        self.assertTrue(compileRE(r'[\t]').accepts('\t'))
        self.assertFalse(compileRE(r'[\t]').accepts('\v'))
        self.assertTrue(compileRE(r'[^\t]').accepts('\v'))
        
    def testComplex(self):
        from reCompiler import compileRE

        # IP validation regex generated by https://www.npmjs.com/package/joi
        VALIDATOR = r"(?:(?:(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])|(?:(?:[\dA-Fa-f]{1,4}:){6}(?:[\dA-Fa-f]{1,4}:[\dA-Fa-f]{1,4}|(?:(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|::(?:[\dA-Fa-f]{1,4}:){5}(?:[\dA-Fa-f]{1,4}:[\dA-Fa-f]{1,4}|(?:(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(?:[\dA-Fa-f]{1,4})?::(?:[\dA-Fa-f]{1,4}:){4}(?:[\dA-Fa-f]{1,4}:[\dA-Fa-f]{1,4}|(?:(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(?:(?:[\dA-Fa-f]{1,4}:){0,1}[\dA-Fa-f]{1,4})?::(?:[\dA-Fa-f]{1,4}:){3}(?:[\dA-Fa-f]{1,4}:[\dA-Fa-f]{1,4}|(?:(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(?:(?:[\dA-Fa-f]{1,4}:){0,2}[\dA-Fa-f]{1,4})?::(?:[\dA-Fa-f]{1,4}:){2}(?:[\dA-Fa-f]{1,4}:[\dA-Fa-f]{1,4}|(?:(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(?:(?:[\dA-Fa-f]{1,4}:){0,3}[\dA-Fa-f]{1,4})?::[\dA-Fa-f]{1,4}:(?:[\dA-Fa-f]{1,4}:[\dA-Fa-f]{1,4}|(?:(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(?:(?:[\dA-Fa-f]{1,4}:){0,4}[\dA-Fa-f]{1,4})?::(?:[\dA-Fa-f]{1,4}:[\dA-Fa-f]{1,4}|(?:(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(?:0{0,2}\d|0?[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|(?:(?:[\dA-Fa-f]{1,4}:){0,5}[\dA-Fa-f]{1,4})?::[\dA-Fa-f]{1,4}|(?:(?:[\dA-Fa-f]{1,4}:){0,6}[\dA-Fa-f]{1,4})?::)|v[\dA-Fa-f]+\.[\w-\.~!\$&'\(\)\*\+,;=:]+)"

        ip = compileRE(VALIDATOR.replace('(?:', '('))

        self.assertFalse(ip.isEmpty())

        self.assertFalse(ip.accepts("; cat secret.txt;"))
        self.assertTrue(ip.accepts("1.1.1.1"))
        self.assertTrue(ip.accepts("192.168.1.20"))

        self.assertTrue(ip.accepts("252.73.5.000"))
        self.assertTrue(ip.accepts("::120.08.8.141"))
        self.assertTrue(ip.accepts("B697::d:b34e:A281:9Ff:019.173.068.245"))
        self.assertTrue(ip.accepts("30.134.148.251"))
        self.assertTrue(ip.accepts("::05a8:8:c:c8:Afc:Ce8"))
        self.assertTrue(ip.accepts("::e7:Cf6:cf:A:E7e3:f55:4"))
        self.assertTrue(ip.accepts("vdc75Bf6.$Wt:.OP(1,UE5Y!WQ(NA!2LC"))
        self.assertTrue(ip.accepts("::Daae:3:87:2a:F96F:0ac:EfA"))
        self.assertTrue(ip.accepts("249.230.170.08"))

        self.assertTrue(ip.accepts("::"))
        self.assertTrue(ip.accepts("::a"))
        self.assertTrue(ip.accepts("vB.!"))
        self.assertFalse(ip.accepts(":::"))

        self.assertTrue(ip.accepts("vB.;cat$IFS$9secret.txt;"))

if __name__ == '__main__':
    unittest.main()
