from distutils.core import setup, Extension

module1 = Extension('_example', sources=['example.c', 'example_warp.c'])

setup(name='example', version='1.0', description='This is a swig example', \
        ext_modules[module1])
