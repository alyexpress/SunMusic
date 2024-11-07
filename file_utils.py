from shutil import rmtree
from os import mkdir

def read(filename):
    with open(filename, 'rb') as file:
        return file.read()

def create(filename, data):
    with open(filename, 'wb') as file:
        file.write(data)

def clear(path):
    rmtree(path)
    mkdir(path)