#!/usr/bin/env python
"""Setup script for Jupyter NbClassic"""

#-----------------------------------------------------------------------------
#  Copyright (c) 2015-, Jupyter Development Team.
#  Copyright (c) 2008-2015, IPython Development Team.
#
#  Distributed under the terms of the Modified BSD License.
#
#  The full license is in the file LICENSE, distributed with this software.
#-----------------------------------------------------------------------------

import os
import sys

if sys.version_info < (3, 6):
    pip_message = 'This may be due to an out of date pip. Make sure you have pip >= 9.0.1.'
    try:
        import pip
        pip_version = tuple(int(x) for x in pip.__version__.split('.')[:3])
        if pip_version < (9, 0, 1) :
            pip_message = 'Your pip version is out of date, please install pip >= 9.0.1. '\
            'pip {} detected.'.format(pip.__version__)
        else:
            # pip is new enough - it must be something else
            pip_message = ''
    except Exception:
        pass


    error = """
NbClassic 1+ supports Python 3.7 and above.

Python {py} detected.
{pip}
""".format(py=sys.version_info, pip=pip_message )

    print(error, file=sys.stderr)
    sys.exit(1)

# At least we're on the python version we need, move on.

# BEFORE importing distutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

from setuptools import setup

# Needed to support building with `setuptools.build_meta`
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from setupbase import (
    version,
    find_packages,
    find_package_data,
    check_package_data_first,
    CompileCSS,
    CompileJS,
    CompileBackendTranslation,
    Bower,
    JavascriptVersion,
    css_js_prerelease,
)


setup_args = dict(
    packages        = find_packages(),
    package_data    = find_package_data(),
)

# Custom distutils/setuptools commands ----------
from distutils.command.build_py import build_py
from distutils.command.sdist import sdist
from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.develop import develop

class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg

    Prevents setup.py install from performing setuptools' default easy_install,
    which it should never ever do.
    """
    def run(self):
        sys.exit("Aborting implicit building of eggs. Use `pip install .` to install from source.")

setup_args['cmdclass'] = {
    'build_py': css_js_prerelease(
            check_package_data_first(build_py)),
    'sdist' : css_js_prerelease(sdist, strict=True),
    'develop': css_js_prerelease(develop),
    'css' : CompileCSS,
    'backendtranslations': CompileBackendTranslation,
    'js' : CompileJS,
    'jsdeps' : Bower,
    'jsversion' : JavascriptVersion,
    'bdist_egg': bdist_egg if 'bdist_egg' in sys.argv else bdist_egg_disabled,
}

try:
    from wheel.bdist_wheel import bdist_wheel
except ImportError:
    pass
else:
    setup_args['cmdclass']['bdist_wheel'] = css_js_prerelease(bdist_wheel)

# Run setup --------------------
def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()
