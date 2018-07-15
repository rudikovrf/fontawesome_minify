"""FontAwesome minify utilit."""

import argparse
import os.path
import re
import json

import glob2


class FAHandler:
    """Handle FontAwesome file for getting icons."""

    patern = re.compile(r"((?<=var f = )|(?<=var f=))\{(.+?)\};")

    def __init__(self, file, html_icons):
        """Initialize handler."""
        self.file = file
        self.minify_file = file[:-3] + '.min.js'
        self.data = ''
        self.handled_data = ''
        self.html_icons = html_icons
        self.icons = set()

    def get_size(self):
        """Return size of FontAwesome file."""
        return len(self.data)

    def get_minified_size(self):
        """Return size of FontAwesome minified file."""
        return len(self.handled_data)

    def _get_data(self):
        """Read file."""
        with open(self.file) as file_reader:
            self.data = file_reader.read()

    def _handle_icon_text(self, string):
        """Return string with only used icons."""
        string = re.sub(r'(\b[^\"]+):', r'"\1":', string)[:-1]
        json_data = json.loads(string)
        json_data = {
            key: json_data[key] for key in json_data
            if key in self.html_icons
        }
        string = json.dumps(json_data)
        return string + ';'

    def _parse(self):
        """Find icons and remove unused icons."""
        self.handled_data = self.data
        start = -1
        while True:
            search_result = self.patern.search(self.handled_data[start+1:])
            if search_result is None:
                break
            end = search_result.end() + start + 1
            start = search_result.start() + start + 1
            icon_text = self._handle_icon_text(self.handled_data[start:end])
            self.handled_data = (
                self.handled_data[:start] + icon_text + self.handled_data[end:]
            )

    def _write_result(self):
        """Write minify file."""
        with open(self.minify_file, 'w') as file_writer:
            file_writer.write(self.handled_data)

    def just_do_it(self):
        """Make minify file."""
        self._get_data()
        self._parse()
        self._write_result()


class HTMLHandler:
    """Handle html files for getting icons."""

    patern = re.compile(
        r"<i class=\"fa. +(?:fa-(?:(?:pulse)|(?:rotate-\d+)|(?:fa-flip-\
        horizontal)|(?:fa-flip-vertical)|(?:spin)|(?:border)|(?:pull-right)\
        |(?:pull-left)|(?:inverse)|(?:stack-\d+x)|(?:xs)|(?:fw)|(?:sm)|(?:lg)\
        |(?:\d+x)) )* *fa-(?P<name>.+?)(?: +.+?)*\"><\/i>"
    )

    def __init__(self, pathes):
        """Initialize handler."""
        self.pathes = pathes
        self.html_files = []
        self.html = ""
        self.icons = set()

    def _glue_together(self):
        """Glue html files together."""
        for file in self.html_files:
            with open(file) as file_reader:
                self.html += '\n' + file_reader.read()

    def _get_html_files(self):
        """Get html files from pathes."""
        for directory in self.pathes:
            if directory[-1] == '\\' or directory[-1] == '/':
                directory = directory[:-1]
            files = glob2.glob(directory + '/**/*.html', recursive=True)
            self.html_files.extend(files)

    def _get_icons(self):
        """Get FontAwesome icons from html files."""
        self.icons = set(self.patern.findall(self.html))

    def get_result(self):
        """Return list of using icons."""
        self._get_html_files()
        self._glue_together()
        self._get_icons()
        return self.icons


def get_undirectories(pathes):
    """Return undirectories."""
    def is_undirectory(path):
        """Return False if path is a directory, else return True."""
        return not os.path.isdir(path)

    return list(filter(is_undirectory, pathes))


def main():
    """Handle request."""
    parser = argparse.ArgumentParser(
        description='FontAwesome minify utilit. It works for FontAwesome 5.1 with \
        python3.5 or older.'
    )
    parser.add_argument('-t', nargs='+', help='Directories of the templates')
    parser.add_argument('-f', help='Path to FontAwesome.js')
    args = parser.parse_args()
    if args.f and args.t:
        correct = True
        if get_undirectories(args.t):
            print('-t contains undirectories.')
            correct = False
        if not os.path.isfile(args.f) and not args.f.endswith('.js'):
            print('-f does not contain js file')
            correct = False
        if correct:
            html_handler = HTMLHandler(args.t)
            icons_from_html = html_handler.get_result()
            print('HTML files are handled.')
            fa_handler = FAHandler(args.f, icons_from_html)
            fa_handler.just_do_it()
            print('FontAwesome file is handled.')
            print('File {} is created.'.format(fa_handler.minify_file))
            print('The file size is reduced by {:.2f} KB.'.format(
                (fa_handler.get_size() - fa_handler.get_minified_size())/1024
            ))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
