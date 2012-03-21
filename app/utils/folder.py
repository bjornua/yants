# -*- coding: utf-8 -*-
import os
from os.path import join, isfile, isdir
def get_nodes(path):
    """Recursively return nodes paths in a directory"""
    nodes = []
    for entry in os.listdir(join(*path)):
        entry = path + [entry]
        entrystring = join(*entry)
        if isfile(entrystring):
            nodes += [entry]
        elif isdir(entrystring):
            nodes += get_nodes(entry)
    nodes += [path]
    return nodes

def get_files(directory):
    """Recursively return file paths in a directory"""
    dir = os.listdir(directory)
    dir = [os.path.join(directory, entry) for entry in dir]
    files = filter(os.path.isfile, dir)
    directories = filter(os.path.isdir, dir)
    for dir in directories:
        files += get_files(dir)
    return files
