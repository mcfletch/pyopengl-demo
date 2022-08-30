#! /usr/bin/env python
"""OpenGL-ctypes setup script (setuptools-based)
"""
import sys, os

sys.path.insert(0, ".")
from distutils.core import setup

# HERE = os.path.dirname(os.path.abspath(__file__))

# packages = []


# def is_package(path):
#     return os.path.isfile(os.path.join(path, "__init__.py"))


# def find_packages(root):
#     """Find all packages under this directory"""
#     packages = []
#     for path, directories, files in os.walk(root):
#         if is_package(path):
#             packages.append(path[len(root) + 1 :].replace("/", "."))
#     return packages


# packages += find_packages(HERE)

# requirements = ["PyOpenGL", "six"]

if __name__ == "__main__":
    setup(
        # name="PyOpenGL-Demo",
        # packages=packages,
        # version="3.1.1",
        # description="Demonstration scripts for the PyOpenGL library",
        # include_package_data=True,
        # zip_safe=False,
        # options={
        #     "sdist": {
        #         "formats": ["gztar"],
        #     },
        # },
        # install_requires=requirements,
        # maintainer="Mike C. Fletcher",
        # maintainer_email="mcfletch@vrplumber.com",
        # url="https://github.com/mcfletch/pyopengl-demo",
        # license="BSD",
        # use_2to3=False,
    )
