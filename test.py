"""Test FontAwesome minify."""

import unittest
import os
import re

import shutil

from minify import FAHandler, HTMLHandler, get_undirectories


def create_directories():
    """Create dirs for tests."""
    if not os.path.exists('test_dir'):
        os.mkdir('test_dir')
    if not os.path.exists('test_dir/1'):
        os.mkdir('test_dir/1')
    if not os.path.exists('test_dir/2'):
        os.mkdir('test_dir/2')


def remove_directories():
    """Remove dirs for tests."""
    shutil.rmtree('test_dir', ignore_errors=True)


class TestGetUndirecrories(unittest.TestCase):
    """Class tests get_undirectories function."""

    @classmethod
    def setUpClass(cls):
        """Create dirs for tests."""
        create_directories()

    @classmethod
    def tearDownClass(cls):
        """Remove dirs for tests."""
        remove_directories()

    def test_undirectories(self):
        """Test with undirectories."""
        input_dirs = [
            'test1',
            'test2'
        ]
        output_dirs = [
            'test1',
            'test2'
        ]
        self.assertListEqual(get_undirectories(input_dirs), output_dirs)

    def test_directories(self):
        """Test with directories."""
        input_dirs = [
            'test_dir/1',
            'test_dir/2'
        ]
        output_dirs = []
        self.assertListEqual(get_undirectories(input_dirs), output_dirs)

    def test_mix(self):
        """Test with directories and undirectories."""
        input_dirs = [
            'test_dir/1',
            'test_dir2'
        ]
        output_dirs = ['test_dir2']
        self.assertListEqual(get_undirectories(input_dirs), output_dirs)


if __name__ == '__main__':
    unittest.main()
