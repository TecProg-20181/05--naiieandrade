import unittest
# import unittest.mock
import mock
# from unittest.mock import MagicMock
import io
import sys
import os
import subprocess
import StringIO
from diskspace import bytes_to_readable
from diskspace import subprocess_check_output, print_tree
from diskspace import calculate_percentage, du_command, percentage_args


class TestDiskspace(unittest.TestCase):

    def setUp(self):
        self.file_tree = {'/home/teste': {'print_size': '2.00Kb',
                                          'children': [], 'size': 4}}
        self.file_tree_node = {'print_size': '2.00Kb',
                               'children': [], 'size': 4}
        self.path = '/home/teste'
        self.largest_size = 6
        self.total_size = 4

    def test_bytes_to_readable(self):
        blocks = 224
        result = "112.00Kb"
        self.assertEqual(bytes_to_readable(blocks), result)

    def test_subprocess_check_output(self):
        command = 'du'
        du_result = subprocess.check_output(command)
        result = subprocess_check_output(command)
        self.assertEqual(du_result, result)

    def test_calculate_percentage(self):
        percentage = calculate_percentage(self.file_tree_node, self.total_size)
        self.assertTrue(percentage == 100)

    def test_print_tree(self):
        cap = StringIO.StringIO()
        sys.stdout = cap

        print_tree(self.file_tree, self.file_tree_node, self.path,
                   self.largest_size, self.total_size)
        result = "2.00Kb  100%  /home/teste\n"
        sys.stdout = sys.__stdout__
        # print("Get Value: " + cap.getvalue())
        self.assertEqual(result, cap.getvalue())

    def test_du_command_default(self):
        abs_directory = self.path
        cmd = du_command(-1, abs_directory)
        result = "du " + self.path
        self.assertEqual(result, cmd)

    def test_du_command(self):
        abs_directory = self.path
        depth = 1
        cmd = du_command(depth, abs_directory)
        result = "du -d {} {}".format(depth, self.path)
        self.assertEqual(result, cmd)

    def test_args_tree_view(self):
        depth = 0
        path = self.path.split("/")[-1]
        result = '{}{}'.format('   '*depth, os.path.basename(self.path))
        self.assertEqual(result, path)


if __name__ == '__main__':
    unittest.main()
