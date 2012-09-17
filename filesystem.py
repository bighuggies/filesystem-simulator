#!/usr/bin/env python

# Andrew Hughson | ahug048 | 1546814

import sys
import logging
import shlex


class FileSystem(object):
    """Maintains a file system in memory using a tree of dictionaries"""

    def __init__(self):
        """Initialise a file system as a single root directory called '/' and
        set it to the present working directory.

        """
        self.filesystem = {
            '/': {}
        }

        self.root = self.filesystem['/']
        self.pwd = self.root
        self.path = []

    def _get_file(self, path):
        """Get the file at a given path.

        Arguments:
        path -- The path of a file relative to the pwd.

        Returns:
        Dictionary representing a file.

        """
        parts = path.split('/')

        file = self.pwd

        # Decend down the file tree from the pwd
        for p in parts:
            file = file[p]

        return file

    def _get_parent(self, path):
        """Get the directory above a file at a given path.

        Arguments:
        path -- The path of a file whose parent is wanted relative to the pwd.

        Returns:
        Dictionary object representing the parent directory of a file at the
        given path.

        """
        if '/' in path:
            return self._get_file('/'.join(path.split('/')[:-1]))
        else:
            return self.pwd

    def _get_absolute_path(self, file):
        """Get the absolute path of a given file.

        Arguments:
        file -- Dictionary representing a file.

        Returns:
        Absolute path of a file as a string.

        """
        if self.pwd == self.root:
            return '/'
        else:
            return '/' + '/'.join(self.path) + '/'

    def _get_filename(self, path):
        """Get the name of a file specified by a path."""
        return path.split('/')[-1]

    def home(self):
        """Set the pwd to the root of the file system."""
        self.pwd = self.root
        self.path = []

    def enter(self, path):
        """Set the pwd to a directory below the current pwd.

        Arguments:
        path -- Path of a directory to enter relative to the pwd.

        """
        logging.info('ENTERING ' + path)
        self.pwd = self._get_file(path)
        self.path.append(path)

    def create(self, path, file):
        """Create a new file.

        Arguments:
        path -- The path where the new file will exist in the filesystem.
        file -- The file object to be placed at the path.

        """
        logging.info('CREATING ' + path + ' with value ' + str(file))
        parent = self._get_parent(path)
        parent[self._get_filename(path)] = file

    def delete(self, path):
        """Delete a file.

        Arguments:
        path: The path of the file to be deleted relative to the pwd.

        """
        logging.info('DELETING ' + path)
        parent = self._get_parent(path)
        del parent[self._get_filename(path)]

    def deleteall(self, path):
        """Delete all references to a file.

        Arguments:
        path -- The path of the file to remove all reference to.

        """
        logging.info('DELETING all references to ' + path)
        self._delete_links(self.filesystem, self._get_file(path))

    def _delete_links(self, parent, file):
        """Traverse the file system looking for references to a file and delete
        them.

        Arguments:
        parent -- Dictionary representing the directory to begin the search at.
        file -- The file to be found and removed.

        """
        for key, value in parent.items():
            # For each file that is a child to this one
            if key == 'text':
                # This file is a text file, ignore
                continue
            if value == file:
                # This is the file we are looking for, delete it
                del parent[key]
            else:
                # Look in this file
                self._delete_links(value, file)

    def append(self, text, path):
        """Add text to a file.

        Arguments:
        text -- The text to add to the file as a string.
        path -- The path of the file to add the text to relative to the pwd.

        """
        logging.info('APPENDING "' + text + '" to ' + path)
        file = self._get_file(path)
        file['text'] = file['text'] + text

    def show(self, path):
        """Print the contents of a text file."""
        logging.info('SHOWING ' + path)
        print(self._get_file(path)['text'])

    def list(self):
        """List the contents of a directory."""
        logging.info("LISTING " + str(self.pwd))

        # Print the absolute path of the pwd
        print('\n=== ' + str(self._get_absolute_path(self.pwd)) + ' ===')
        for filename, file in sorted(self.pwd.iteritems()):
            # Print each file name, followed by a 'd' if it is a directory,
            # followed by its size.
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

    def move(self, sourcepath, destpath):
        """Move a file from one location in the filesystem to another.

        Arguments:
        sourcepath -- The path of the file to be moved relative to the pwd.
        destpath -- The path where the file will be moved relative to the pwd.

        """
        logging.info('MOVING ' + sourcepath + ' to ' + destpath)
        source = self._get_file(sourcepath)
        self.create(destpath, file=source)
        self.delete(sourcepath)

    def link(self, linkpath, origpath):
        """Create a reference to a file at a new location in the filesystem.

        Arguments:
        linkpath -- The path at which the link should exist.
        origpath -- The path of the file which the link should point to.

        """
        logging.info('LINKING ' + linkpath + ' to ' + origpath)
        orig = self._get_file(origpath)
        # Put a reference to the file at the link location.
        self.create(linkpath, orig)


if __name__ == '__main__':
    logging.basicConfig(filename='output.log', level=logging.WARNING)
    logging.info('STARTING FILESYSTEM\n-----------------------------')

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
        'link': fs.link,
        'delete': fs.delete,
        'rm': fs.delete,
        'deleteall': fs.deleteall,
        'quit': lambda: sys.exit(1),
    }

    while True:
        sys.stdout.write('> ')

        parts = shlex.split(sys.stdin.readline())

        # If there was input, the first part is the command. Otherwise, skip the
        # rest of this iteration.
        if parts:
            command = parts[0].strip()
        else:
            continue

        # The first index of the list is the command, the rest are args
        args = [arg for arg in parts[1:]]

        logging.info('CMD: ' + command + ' ARGS: ' + str(args))

        # Attempt to execute the command. If the command does not exist, print
        # the given input (plus a leading space to match the sample output)
        try:
            commands[command](*args)
        except KeyError:
            print(' '.join(parts) + ' ')

        logging.info('--------------')