#! /usr/bin/env python
"""OpenGL-ctypes setup script (setuptools-based)
"""
from setuptools import setup, find_packages
import sys, os
sys.path.insert(0, '.' )

requirements = ['PyOpenGL']
packages = find_packages(  )


if __name__ == "__main__":
	setup(
		name = "PyOpenGL-Demo",
		version = '3.0.0b6',
		packages = packages,
		
		description = 'Demonstration scripts for the PyOpenGL library',
		include_package_data = True,
		zip_safe = False,
		
		install_requires = requirements,
		maintainer = 'Mike C. Fletcher',
		maintainer_email = 'mcfletch@vrplumber.com',
		url = 'http://pyopengl.sourceforge.net/',
		license = 'BSD',
		download_url = "http://sourceforge.net/project/showfiles.php?group_id=5988",

	)
