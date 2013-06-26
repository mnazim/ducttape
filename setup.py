from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "ducttape",
    version = "0.1.alpha",
    packages = find_packages(),
    zip_safe = True,
    scripts = [],

    install_requires = ['Django', 'watchdog'],

    entry_points = {
        'console_scripts': [
            'ducttape = ducttape:main',
        ],
    },

    package_data = {
        '': ['*.txt', '*.rst'],
    },

    # metadata for upload to PyPI
    author = "Mir Nazim",
    author_email = "me@mirnazim.org",
    description = "A prototyping/desing tool uhich uses Django templates",
    license = "MIT",
    keywords = "",
    url = "http://github.com/mnazim/ducttape",

)
