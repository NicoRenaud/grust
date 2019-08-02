#!/usr/bin/env python

import os

from setuptools import (find_packages, setup)

here = os.path.abspath(os.path.dirname(__file__))

# To update the package version number, edit pyCHAMP/__version__.py
version = {}
with open(os.path.join(here, 'grust', '__version__.py')) as f:
    exec(f.read(), version)

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='grust',
    version=version['__version__'],
    description="Graph Clustering for 1D signal",
    long_description=readme + '\n\n',
    long_description_content_type='text/markdown',
    author=["Nicolas Renaud"],
    author_email='n.renaud@esciencecenter.nl',
    url='https://github.com/NicoRenaud/grust',
    packages=find_packages(),
    package_dir={'grust': 'grust'},
    include_package_data=True,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='grust',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'intended audience :: science/research',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: data clustering'
    ],
    test_suite='tests',
    install_requires=['matplotlib', 'numpy', 'h5py', 'scipy', 'tqdm'],
    extras_require={
        'dev': ['prospector[with_pyroma]', 'yapf', 'isort'],
        'doc': ['recommonmark', 'sphinx', 'sphinx_rtd_theme'],
        'test': ['coverage', 'pycodestyle', 'pytest', 'pytest-cov', 'pytest-runner'],
    }
)
