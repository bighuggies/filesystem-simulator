#!/usr/bin/env python

import sys
import os

HOME = os.getcwd()
CWD = '/'


class FileSystem(object):
    def __init__(self):
        self.root = Directory('', None)
        self.pwd = self.root

    def get_file(self, path):
        if not path:
            return self.pwd
        if path == '/':
            return self.root
        elif path[0] == '/':
            root = self.root
            path = path[1:]
        else:
            root = self.pwd

        file_names = path.split('/')
        f = root

        for name in file_names:
            f = f.files[name]

        return f

    def get_path(self, filen):
        if filen == self.root:
            return '/'

        path = filen.name + '/'

        while filen.parent is not None:
            path = filen.parent.name + '/' + path
            filen = filen.parent

        return path

    def change_directory(self, path):
        self.pwd = self.get_file(path)

    def create_file(self, path, type):
        filename = path.split('/')[-1]
        path = '/'.join(path.split('/')[:-1])

        if path:
            directory = self.get_file(path)
        else:
            directory = self.pwd

        if type == 'text':
            directory.add_file(TextFile(filename, directory))
        elif type == 'dir':
            directory.add_file(Directory(filename, directory))

    def link(self, link, path):
        #todo
        pass

    def list_files(self):
        print('=== ' + self.get_path(self.pwd) + ' ===')
        for f in sorted(self.pwd.files.values()):

            sys.stdout.write(f.name)
            for i in xrange(21 - len(f.name)):
                sys.stdout.write(' ')

            if (type(f) == Directory):
                sys.stdout.write('d ')
            else:
                sys.stdout.write('  ')

            if (type(f) == TextFile):
                size = str(len(f.text))
                size_len = len(size)
            elif (type(f) == Directory):
                # Gets the sum of the length of all the filenames in a directory
                # + 1 for each directory
                size = str(len(':'.join([fi.name for fi in f.files.values()])) + 1)
                size_len = len(size)

            for i in xrange(11 - size_len):
                sys.stdout.write(' ')
            sys.stdout.write(size)
            sys.stdout.write('\n')

    def append(self, *args):
        path = args[-1]
        text = ' '.join(args[:-1]).strip('"')

        self.get_file(path).append(text)

    def show(self, path):
        print(self.get_file(path).text)

    def move(self, source, dest):
        sourcefile = self.get_file(source)

        destparent = self.get_file('/'.join(dest.split('/')[0:-1]))
        destname = dest.split('/')[-1]

        if (type(sourcefile) == Directory):
            destfile = Directory(destname, destparent)
            destfile.files = sourcefile.files
        elif (type(sourcefile) == TextFile):
            destfile = TextFile(destname, destparent)
            destfile.text = sourcefile.text

        del(sourcefile.parent.files[sourcefile.name])
        destparent.add_file(destfile)


class File(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent


class Directory(File):
    def __init__(self, name, parent):
        File.__init__(self, name, parent)
        self.files = {}

    def add_file(self, filen):
        self.files[filen.name] = filen


class TextFile(File):
    def __init__(self, name, parent):
        File.__init__(self, name, parent)
        self.text = ''

    def append(self, text):
        self.text = self.text + text


class Link(File):
    def __init__(self, name, parent, file=None):
        File.__init__(self, name, parent)
        self.link = file


if __name__ == '__main__':
    fs = FileSystem()

    commands = {
        'home': lambda: fs.change_directory('/'),
        'enter': fs.change_directory,
        'create': lambda x: fs.create_file(x, 'text'),
        'mkdir': lambda x: fs.create_file(x, 'dir'),
        'append': fs.append,
        'show': fs.show,
        'listfiles': fs.list_files,
        'move': fs.move,
        'link': '10',
        'delete': lambda x: os.system('rm {}'.format(x)),
        'deleteall': '14',
        'quit': lambda: sys.exit(1),
    }

    while True:
        sys.stdout.write('> ')

        parts = sys.stdin.readline().split(' ')
        command = parts[0].strip()
        
        args = []
        if len(parts) > 1:
            args = [arg.strip() for arg in parts[1:]]
        
        # print('Command: ' + command + ' args: ' + str(args))

        try:
            commands[command](*args)
        except KeyError:
            pass
