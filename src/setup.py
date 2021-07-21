import os
import sys
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy


sources = ["pypoisson.pyx"]
path = "PoissonRecon_v6_13/src/"
files = [os.path.join(path,x) for x in os.listdir(path) if x.endswith(".cpp")]
sources += files


if sys.platform.startswith('linux') or sys.platform == 'darwin':
    macros = [('__linux__', '1')]
else:
    macros = [('__linux__', '0')]


exts = [Extension("pypoisson", sources,
        language="c++",
        define_macros=macros,
        extra_compile_args = ["-w","-fopenmp"],
        extra_link_args=["-fopenmp"]
        )]
setup(
    name='pypoisson',
    version='0.10',
    description='Poisson Surface Reconstruction Python Binding',
    author='Miguel Molero-Armenta',
    author_email='miguel.molero@gmail.com',
    url='https://github.com/mmolero/pypoisson',
    cmdclass = {'build_ext': build_ext},
    ext_modules = exts, include_dirs = [numpy.get_include()]

)


"""
python setup.py build_ext --inplace --compiler=mingw32 -DMS_WIN64
"""