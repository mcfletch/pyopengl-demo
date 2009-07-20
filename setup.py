#! /usr/bin/env python
"""OpenGL-ctypes setup script (setuptools-based)
"""

import sys, os
sys.path.insert(0, '.' )

# if setuptools isn't installed... we just use these packages manually.
from distutils.core import setup
packages = ['PyOpenGL-Demo', 'PyOpenGL-Demo.tom', 'PyOpenGL-Demo.GLE', 'PyOpenGL-Demo.dek', 'PyOpenGL-Demo.redbook', 'PyOpenGL-Demo.NeHe', 'PyOpenGL-Demo.da', 'PyOpenGL-Demo.GLUT', 'PyOpenGL-Demo.dek.OglSurface', 'PyOpenGL-Demo.NeHe.lesson43', 'PyOpenGL-Demo.NeHe.lesson44', 'PyOpenGL-Demo.NeHe.lesson48', 'PyOpenGL-Demo.GLUT.tom']


requirements = ['PyOpenGL']



if __name__ == "__main__":
	setup(
		name = "PyOpenGL-Demo",
		version = '3.0.1a1',
		packages = packages,
		
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
		download_url = "https://sourceforge.net/project/showfiles.php?group_id=5988&package_id=221827",

	)
