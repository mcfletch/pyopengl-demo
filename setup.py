#! /usr/bin/env python
"""OpenGL-ctypes setup script (setuptools-based)
"""
import sys, os
sys.path.insert(0, '.' )
from distutils.core import setup

packages = []
def is_package( path ):
    return os.path.isfile( os.path.join( path, '__init__.py' ))
def find_packages( root ):
    """Find all packages under this directory"""
    for path, directories, files in os.walk( root ):
        if is_package( path ):
            packages.append( path.replace( '/','.' ) )
requirements = ['PyOpenGL']

if __name__ == "__main__":
    setup(
        name = "PyOpenGL-Demo",
        packages = packages,
        version = '3.0.2',
        description = 'Demonstration scripts for the PyOpenGL library',
        include_package_data = True,
        zip_safe = False,
        options = {
            'sdist': {
                'formats': ['gztar','zip'],
            },
        },
        install_requires = requirements,
        maintainer = 'Mike C. Fletcher',
        maintainer_email = 'mcfletch@vrplumber.com',
        url = 'http://pyopengl.sourceforge.net/',
        license = 'BSD',
        use_2to3 = True,
        download_url = "https://sourceforge.net/project/showfiles.php?group_id=5988&package_id=221827",
    )
