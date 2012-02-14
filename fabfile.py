from fabric.api import *

def upload():
    """
    Uploads the package to pypi.
    """
    local('python setup.py sdist upload')
    _clean()

def _clean():
    """
    Cleans generated files while uploading to pypi.
    """
    local('rm -rf dist xmldict.egg*')

def test():
    """
    Runs unit tests.
    """
    local('nosetests -v')
