#!/usr/bin/env python

import sys
import logging


class FileSystem(object):
    def __init__(self):
        self.filesystem = {
            '/': {}
        }

        self.home()

    def home(self):
        self.pwd = self.filesystem['/']

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
        if file == self.filesystem['/']:
            return '/'
        else:
            return '/' + self.bfs(self.filesystem, file).strip('/') + '/'

    def bfs(self, parent, file):
        for key, value in parent.items():
            logging.info('Key: ' + key + ' Value: ' + str(value))
            if 'text' in value:
                continue
            else:
                if value == file:
                    return key
                else:
                    return key + '/' + self.bfs(value, file)

    def get_filename(self, path):
        return path.split('/')[-1]

    def enter(self, path):
        logging.info('Entering ' + path)
        self.pwd = self.get_file(path)

    def create(self, path, file):
        logging.info('Creating ' + path + ' with value ' + str(file))
        parent = self.get_parent(path)
        parent[self.get_filename(path)] = file

    def delete(self, path):
        logging.info('Deleting ' + path)
        parent = self.get_parent(path)
        del parent[self.get_filename(path)]

    def append(self, *args):
        text = ' '.join(args[:-1]).strip('"')
        path = args[-1]

        logging.info('Appending "' + text + '" to ' + path)
        
        file = self.get_file(path)
        file['text'] = file['text'] + text

    def show(self, path):
        logging.info('Showing ' + path)
        print(self.get_file(path)['text'])

    def list(self):
        logging.info("Listing " + str(self.pwd))

        print('=== ' + str(self.get_absolute_path(self.pwd)) + ' ===')
        for filename, file in sorted(self.pwd.iteritems()):
            sys.stdout.write(filename)
            for i in xrange(21 - len(filename)):
                sys.stdout.write(' ')

            if 'text' in file:
                sys.stdout.write('  ')
                size = str(len(file['text']))
            else:
                sys.stdout.write('d ')
                filenames = [key for key in file.keys()]
                size = str(len(''.join(filenames)) + len(filenames))

            for i in xrange(1, 11 - len(size)):
                sys.stdout.write(' ')
            sys.stdout.write(size)

            sys.stdout.write('\n')

        sys.stdout.write('\n')

    def move(self, source, dest):
        sourcefile = self.get_file(source)
        logging.info('Moving ' + str(sourcefile) + ' to ' + dest)
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
        'link': '10',
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

        logging.info('Command: ' + command + ' args: ' + str(args))

        try:
            commands[command](*args)
        except KeyError:
            pass
