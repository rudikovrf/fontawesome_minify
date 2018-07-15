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


class TestHTMLHandler(unittest.TestCase):
    """Class tests HTMLHandler class."""

    @classmethod
    def setUpClass(cls):
        """Create dirs and files for tests."""
        create_directories()
        shutil.copyfile('test_data/f1.html', 'test_dir/1/f1.html')
        shutil.copyfile('test_data/f2.html', 'test_dir/2/f2.html')
        shutil.copyfile('test_data/f3.js', 'test_dir/2/f3.js')

    @classmethod
    def tearDownClass(cls):
        """Remove dirs and files for tests."""
        remove_directories()

    def test_get_html_files(self):
        """Test _get_html_files."""
        instance = HTMLHandler(['test_dir/2', 'test_dir/1'])
        instance._get_html_files()
        self.assertListEqual(
            instance.html_files,
            ['test_dir/2/f2.html', 'test_dir/1/f1.html']
        )

    def test_glue_together(self):
        """Test _glue_together."""
        instance = HTMLHandler([])
        instance.html_files = ['test_dir/2/f2.html', 'test_dir/1/f1.html']
        instance._glue_together()
        with open('test_dir/2/f3.js') as f_reader:
            html = f_reader.read()
        self.assertEqual(
            re.sub(r'\s', '', instance.html),
            re.sub(r'\s', '', html)
        )

    def test_get_icons(self):
        """Test _get_icons."""
        with open('test_data/_get_icons.html') as file_reader:
            data = file_reader.read()
        instance = HTMLHandler([])
        instance.html = data
        instance._get_icons()

        answer = {
            'moon',
            'play',
            'sun',
            'star',
            'stroopwafel'
        }
        for i in range(1, 25):
            answer.add('stroopwafel{}'.format(i))

        self.assertSetEqual(instance.icons, answer)

    def test_get_result(self):
        """Test get_result."""
        instance = HTMLHandler(['test_dir/2', 'test_dir/1'])
        self.assertSetEqual(
            instance.get_result(),
            {'times', 'pencil-alt', 'trash-alt', 'check'}
        )


if __name__ == '__main__':
    unittest.main()
