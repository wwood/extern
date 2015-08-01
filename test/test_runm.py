#!/usr/bin/env python

import unittest
import os.path
import sys

sys.path = [os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','runm')]+sys.path
from runm import RunMCalledProcessError
import runm

class Tests(unittest.TestCase):

    def test_hello_world(self):
        self.assertEqual("commandeering\n", runm.run("echo commandeering"))
        
    def test_process_substitution(self):
        self.assertEqual("1\n2\n3\n", runm.run("cat <(seq 3)"))
        
    def test_pipe(self):
        self.assertEqual("2\n3\n", runm.run("cat <(seq 2 3)"))
        
    def test_bad_command(self):
        with self.assertRaises(RunMCalledProcessError) as ex:
            runm.run("cat /not_a_file_coz_I_SED_SO")
        self.assertEqual('Command cat /not_a_file_coz_I_SED_SO returned non-zero exit status 1.\nSTDERR was: cat: /not_a_file_coz_I_SED_SO: No such file or directory\nSTDOUT was: ',
                         str(ex.exception))
        
if __name__ == "__main__":
    unittest.main()
