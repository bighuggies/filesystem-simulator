#!/usr/bin/env python

import sys


class FileSystem(object):
    def __init__(self):
        self.filesystem = {
            '/': {}
        }

        self.pwd = self.home()

    def home(self):
        return self.filesystem['/']

    def get_file(self, path):
        parts = path.split('/')

        file = self.pwd
        for p in parts:
            file = file[p]

        return file

    def get_parent(self, path):
        if '/' in path:
            return self.get_file('/'.join(path.split('/')[:-1]))
        else:
            return self.pwd

    def get_absolute_path(self, file):
        if file == self.home():
            return '/'
        else:
            return '/' + self.bfs(self.filesystem, file).strip('/') + '/'

    def bfs(self, parent, file):
        for key, value in parent.items():
            if value == file:
                return key
            else:
                return key + '/' + self.bfs(value, file)

    def get_filename(self, path):
        return path.split('/')[-1]

    def enter(self, path):
        self.pwd = self.get_file(path)

    def create(self, path, file):
        print('Creating ' + path + ' with value ' + str(file))
        parent = self.get_parent(path)
        parent[self.get_filename(path)] = file

    def delete(self, path):
        print('Deleting ' + path)
        parent = self.get_parent(path)
        del parent[self.get_filename(path)]

    def append(self, text, path):
        print('Appending "' + text + '" to ' + str(path))
        file = self.get_file(path)
        file['text'] = file['text'] + text

    def show(self, path):
        print(self.get_file(path)['text'])

    def list(self):
        print('=== ' + str(self.get_absolute_path(self.pwd)) + ' ===')
        for filename, file in self.pwd.iteritems():
            sys.stdout.write(filename)
            for i in xrange(20 - len(filename)):
                sys.stdout.write(' ')

            if 'text' in file:
                sys.stdout.write('  ')
                size = str(len(file['text']))
            else:
                sys.stdout.write('d ')
                filenames = [key for key in file.keys()]
                size = str(len(':'.join(filenames)))
    
            for i in xrange(11 - len(size)):
                sys.stdout.write(' ')
            sys.stdout.write(size)

            sys.stdout.write('\n')

        sys.stdout.write('\n\n') 

    def move(self, source, dest):
        sourcefile = self.get_file(source)
        print('Moving ' + str(sourcefile) + ' to ' + dest)
        self.create(dest, file=sourcefile)
        self.delete(source)


if __name__ == '__main__':
    fs = FileSystem()

    commands = {
        'home': fs.home,
        'enter': fs.enter,
        'cd': fs.enter,
        'create': lambda path: fs.create(path, file={'text': ''}),
        'touch': lambda path: fs.create(path, file={'text': ''}),
        'mkdir': lambda path: fs.create(path, file={}),
        'append': fs.append,
        'show': fs.show,
        'listfiles': fs.list,
        'ls': fs.list,
        'move': fs.move,
        'mv': fs.move,
        # 'link': '10',
        'delete': fs.delete,
        'rm': fs.delete,
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

        # try:
        commands[command](*args)
        # except KeyError:
        #     pass
