import os
from setuptools import setup
from jupyter_packaging import create_cmdclass


NAME = 'nbclassic'

about = {}
here = os.path.abspath(os.path.dirname(__file__))
project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
with open(os.path.join(here, project_slug, '__version__.py')) as f:
    exec(f.read(), about)


with open("README.md", "r") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))

# Handle datafiles
cmdclass = create_cmdclass(
    data_files_spec=[(
        'etc/jupyter/jupyter_server_config.d',
        'jupyter_server_config.d',
        '*.json'
    )]
)

setup_args = dict(
    name             = NAME,
    description      = 'Jupyter Notebook as a Jupyter Server Extension.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    version          = about['__version__'],
    author           = 'Jupyter Development Team',
    author_email     = 'jupyter@googlegroups.com',
    url              = 'http://jupyter.org',
    license          = 'BSD',
    platforms        = "Linux, Mac OS X, Windows",
    keywords         = ['ipython', 'jupyter'],
    classifiers      = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass         = cmdclass,
    zip_safe=False,
    python_requires='>=3.5',
    include_package_data=True,
    install_requires = [
        'jupyter_server>=0.3',
        'notebook<7',
    ],
    entry_points = {
        'console_scripts': [
            'jupyter-nbclassic = nbclassic.notebookapp:main'
        ]
    },
    extras_require = {
        'test': [
            'pytest', 'pytest-tornasync', 'pytest-console-scripts'
        ],
    },
)

if __name__ == '__main__':
    setup(**setup_args)


