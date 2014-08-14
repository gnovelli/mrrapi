import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['requests']

setup(
    name='mrrapi',
    version='0.3',
    url='https://github.com/jcwoltz/mrrapi',
    description='MinigRigRentals.com python API integration',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Office/Business :: Financial"
    ],
    author='jcwoltz',
    author_email='jwoltz@gmail.com',
    keywords='mrr miningrigrentals api bitcoin',
    packages=['mrrapi'],
    install_requires=['requests'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="mrrapi",
)
