#!/usr/bin/env python

#=======================================================================
# Authors: Ben Woodcroft
#
# Unit tests.
#
# Copyright
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License.
# If not, see <http://www.gnu.org/licenses/>.
#=======================================================================

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
