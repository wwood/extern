#!/usr/bin/env python

import unittest
import os.path
import sys

sys.path += [os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')]
from extern import ExternCalledProcessError
import extern

unittest.util._MAX_LENGTH=1000

class Tests(unittest.TestCase):

    def test_hello_world(self):
        self.assertEqual("commandeering\n", extern.run("echo commandeering"))

    def test_process_substitution(self):
        self.assertEqual("1\n2\n3\n", extern.run("cat <(seq 3)"))

    def test_pipe(self):
        self.assertEqual("2\n3\n", extern.run("cat <(seq 2 3)"))

    def test_bad_command(self):
        with self.assertRaises(ExternCalledProcessError) as ex:
            extern.run("cat /not_a_file_coz_I_SED_SO")
        expected = 'Command cat /not_a_file_coz_I_SED_SO returned non-zero exit status 1.\nSTDERR was: b\'cat: /not_a_file_coz_I_SED_SO: No such file or directory\\n\'STDOUT was: b\'\''
        self.assertEqual(expected, str(ex.exception))

    def test_stdin(self):
        self.assertEqual("dog", extern.run("cat", stdin=b"dog"))

    def test_which(self):
        self.assertNotEqual(None, extern.which('cat'))
        self.assertEqual(None, extern.which('notacat'))

    def test_multi_hello_world(self):
        self.assertEqual(['1\n2\n'], extern.run_many(['seq 2'], num_threads=1))

    def test_multi_with_many_threads(self):
        commands = ['seq 2','seq 3 4']*50
        answers = ['1\n2\n','3\n4\n']*50
        self.assertEqual(answers, extern.run_many(commands, num_threads=10))

    def test_multi_with_exception(self):
        with self.assertRaises(ExternCalledProcessError) as ex:
            extern.run_many(['seq 2','cat /notafile'])
        self.assertEqual('Command cat /notafile returned non-zero exit status 1.\nSTDERR was: b\'cat: /notafile: No such file or directory\\n\'STDOUT was: b\'\'',
                         str(ex.exception))

    # def test_multi_iterrupt(self):
    #     '''ctrl-C from tester required, hense usually commented out'''
    #     extern.run_many(['sleep 5'])

    def test_multi_stdin(self):
        self.assertEqual(
            sorted(['no','yes']),
            sorted(extern.run_many(
                ['cat','cat'],
                num_threads=1,
                stdin=(b'yes',b'no'))))

    def test_stdin_with_str(self):
        self.assertEqual('yes', extern.run("cat",stdin='yes'))

    def test_unequal_stdin_and_commands(self):
        with self.assertRaises(Exception) as ex:
            extern.run_many(
                ['seq 2','seq 3'],
                stdin=[b'1'])

    def test_stream_fail(self):
        with self.assertRaises(ExternCalledProcessError) as ex:
            extern.run("cat /notafile |tac")


# Doesn't seem to work with py.test, meh. Works in real life, easy enough to see
# def test_output_stream(capsys):
#     extern.runMany(['seq 4','seq 2'], 1, sys.stderr)
#     _, err = capsys.readouterr()
#     assert 'some' == err

if __name__ == "__main__":
    unittest.main()
