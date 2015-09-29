import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

sources = ["src/pypoisson.pyx"]
path = "src/PoissonRecon_v6_13/src/"
files = [os.path.join(path,x) for x in os.listdir(path) if x.endswith(".cpp")]
sources += files


exts = [Extension("pypoisson", sources,
        language="c++",
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
