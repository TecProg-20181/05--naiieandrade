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


class TestDiskspace(unittest.TestCase):

    def setUp(self):
        self.file_tree = {'/home/teste': {'print_size': '2.00Kb',
                                          'children': [], 'size': 4}}
        self.file_tree_node = {'print_size': '2.00Kb',
                               'children': [], 'size': 4}
        self.path = '/home/teste'
        self.largest_size = 6
        self.total_size = 4
        self.percentage = int(self.file_tree_node['size'] /
                              float(self.total_size) * 100)

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
        percentage = int(self.file_tree_node['size'] /
                         float(self.total_size) * 100)
        self.assertTrue(percentage == 100)

    def test_percent_less_than_args(self):
        args = 99
        result = print_tree(self.file_tree, self.file_tree_node, self.path,
                            self.largest_size, self.total_size)
        self.assertTrue(result < args)

    def test_sysout_mock(self):
        cap = StringIO.StringIO()
        sys.stdout = cap
        print_tree(self.file_tree, self.file_tree_node, self.path,
                   self.largest_size, self.total_size)
        result = '{:>{}s} {:>4d}%  {}\n'.format(self.file_tree_node['print_size'],
                                                self.largest_size,
                                                self.percentage,
                                                self.path)
        sys.stdout = sys.__stdout__
        print("Result: " + result)
        print("Get Value: " + cap.getvalue())
        self.assertEqual(result, cap.getvalue())

    def test_args_tree_view(self):
        depth = 0
        path = self.path.split("/")[-1]
        result = '{}{}'.format('   '*depth, os.path.basename(self.path))
        self.assertEqual(result, path)


if __name__ == '__main__':
    unittest.main()
