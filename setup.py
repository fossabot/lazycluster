#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created based on: https://github.com/kennethreitz/setup.py/blob/master/setup.py
# Alternative: https://github.com/seanfisk/python-project-template/blob/master/setup.py.tpl
import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = "lazycluster"
MAIN_PACKAGE = NAME  # Change if main package != NAME
DESCRIPTION = "Distributed machine learning made simple."
URL = "https://github.com/ml-tooling/lazycluster.git"
EMAIL = "jan.kalkan@mailbox.org"
AUTHOR = "Jan Kalkan"
REQUIRES_PYTHON = ">=3.6"
VERSION = (
    None  # Only set version if you like to overwrite the version in __version__.py
)

# Please define the requirements within the requirements.txt

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

# Check if version is right
if sys.version_info[:1] == 3 and sys.version_info[:2] < (
    3,
    5,
):  # sys.version_info[:2] < (2, 7) or
    raise Exception("This package needs Python 3.6 or later.")  # 2.7,

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!

#

try:
    # convert markdown to rst format
    import pypandoc

    long_description = pypandoc.convert(here, "README.md", "rst")
    long_description = long_description.replace("\r", "")
except:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()

# Read the requirements.txt and use it as the setup.py requirements
with io.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = [line.rstrip() for line in f.readlines()]

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, MAIN_PACKAGE, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class DeployCommand(Command):
    """Support setup.py upload."""

    # Note: To use the 'deploy' functionality of this file, you must:
    #   $ pip install twine

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPi via Twine…")
        os.system("twine upload dist/*")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="%s\n\nRequirements:\n%s" % (long_description, requirements),
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    license="Apache License 2.0",
    packages=find_packages(exclude=("tests",)),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        lazycluster=lazycluster.scripts.cli_handler:cli
    """,
    include_package_data=True,
    classifiers=[
        # TODO: update this list to match your application: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        # Not python 2 compatible right now
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # $ setup.py publish support.
    cmdclass={"deploy": DeployCommand},
)
