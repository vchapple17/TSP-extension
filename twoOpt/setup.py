from distutils.core import setup, Extension
import numpy

ext_twoOpt = Extension("_twoOpt", ["_twoOpt.c", "twoOpt.c"]);

setup(
    ext_modules=[ext_twoOpt],
    include_dirs=[numpy.get_include()]
)
