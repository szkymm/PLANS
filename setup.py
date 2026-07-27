# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================
MODULE               : PLANS.setup

TYPE                 : Python Script (setuptools configuration)

DESCRIPTION          :
    Package metadata and build configuration for PLANS.
    Defines the project name, version, author, dependencies,
    entry points, classifiers, and packaging directives for
    distribution via PyPI and pip.

AUTHOR               : Matt Belfast Brown

CONTACT              : szkymm@gmail.com

MAINTAINER           :
    Matt Belfast Brown (thedayofthedo@gmail.com)


PROJECT CREATE DATE  : 2026-07-15

PROJECT VERSION DATE : 2026-07-15

PROJECT VERSION      : 0.1.2


FILE CREATE DATE     : 2026-07-15

FILE VERSION DATE    : 2026-07-15

FILE VERSION         : 1.0.0


STATUS               : Stable

PYTHON               : >=3.9

LICENSE              : GPL-3.0-only

SPDX ID              : GPL-3.0-only


USAGE                :
    pip install .

====================
THIS PROGRAM IS LICENSED UNDER GPL-3.0-only LICENSE.
YOU SHOULD HAVE RECEIVED A COPY OF GPL-3.0-only LICENSE.

Copyright (C) 2026 Matt Belfast Brown.

Sort License:

    PLANS is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    PLANS is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty
    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PLANS.  If not, see <https://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages

# Invoke setuptools with the project metadata and packaging configuration.
setup(
    # Declare the package name used for PyPI registration and pip install.
    name="pyplans",
    # Declare the semantic version following major.minor.patch convention.
    version="0.1.2",
    # Provide a brief description of the tool for PyPI and help text.
    description="Priority Logs Actions Notes Stracks -- Local-first project management stack system.",
    # Identify the primary author of the package.
    author="Suzuki Yumemi",
    # Supply the contact email address for the package author.
    author_email="szkymm@gmail.com",
    # List search keywords for package discovery on PyPI.
    keywords=[
        # Include PLANS as the primary keyword.
        "plans",
        # Include todo tracking keyword.
        "todo",
        # Include issue tracking keyword.
        "issue-tracker",
        # Include project management keyword.
        "project-management",
        # Include local-first architecture keyword.
        "local-first",
        # Include CLI keyword.
        "cli",
        # Include SQLite keyword.
        "sqlite",
    ],
    # Automatically discover all packages in the current directory tree.
    packages=find_packages(),
    # Restrict installation to Python interpreters version 3.9 and above.
    python_requires=">=3.9",
    # Define the console script entry point for the plans command.
    entry_points={
        # Map the console script group to the list of command definitions.
        "console_scripts": [
            # Register the PLANS command to invoke the main function.
            "PLANS=PLANS.__main__:main",
        ],
    },
    # Include non-Python files listed in MANIFEST.in in the distribution.
    include_package_data=True,
    # Declare the package as requiring directory extraction.
    zip_safe=False,
    # Provide trove classifiers for PyPI categorization and filtering.
    classifiers=[
        # Indicate the development maturity level as alpha stage.
        "Development Status :: 3 - Alpha",
        # Target developers as the primary intended audience.
        "Intended Audience :: Developers",
        # Declare the open-source license identifier for PyPI display.
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # Mark the package as independent of any specific operating system.
        "Operating System :: OS Independent",
        # Declare support for Python 3 as the language major version.
        "Programming Language :: Python :: 3",
        # Declare explicit compatibility with Python version 3.9.
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.9",
        # Declare explicit compatibility with Python version 3.10.
        "Programming Language :: Python :: 3.10",
        # Declare explicit compatibility with Python version 3.11.
        "Programming Language :: Python :: 3.11",
        # Declare explicit compatibility with Python version 3.12.
        "Programming Language :: Python :: 3.12",
        # Declare explicit compatibility with Python version 3.13.
        "Programming Language :: Python :: 3.13",
        # Declare explicit compatibility with Python version 3.14.
        "Programming Language :: Python :: 3.14",
        # Additionally categorize as a reusable Python library module.
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # Declare platform independence for universal distribution.
    platforms="any",
)
