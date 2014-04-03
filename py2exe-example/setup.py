from distutils.core import setup
import py2exe
import glob, os
import OpenGL
data_files = [
    (
        os.path.join('OpenGL','DLLS'),
        glob.glob( os.path.join( os.path.dirname( OpenGL.__file__ ), 'DLLS', '*.*' ))
    ),
]

if __name__ == "__main__":
    setup(
        windows=['shader_test.py'],
        options={
            "py2exe": {
                "includes": [
                    "ctypes", "logging",
                    'OpenGL.platform.win32',
                ] + [
                    'OpenGL.arrays.%s'%x for x in [
                        'ctypesarrays','ctypesparameters','ctypespointers',
                        'lists','nones','numbers','numpymodule','strings','vbo'
                    ]
                ],
                'skip_archive': True,
            },
        },
        data_files = data_files,
    )
