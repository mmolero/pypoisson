import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

sources = ["pypoisson.pyx"]
path = "PoissonRecon_v6_13/src/"
files = [os.path.join(path,x) for x in os.listdir(path) if x.endswith(".cpp")]
sources += files

print sources


exts = [Extension("pypoisson", sources,
        language="c++",
        extra_compile_args = ["-w","-fopenmp"],
        extra_link_args=["-fopenmp"]
        )]
setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = exts, include_dirs = [numpy.get_include()]
)



"""
python setup_pypoisson.py build_ext --inplace --compiler=mingw32 -DMS_WIN64
"""