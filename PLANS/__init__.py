# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================
MODULE               : PLANS.__init__

TYPE                 : Python Script

DESCRIPTION          :
    Package entry point and public API surface for PLANS.
    Exposes the database manager and all five entity managers
    (Strack, Plan, Issue, Action, Note) as the primary public
    interface for programmatic use of the local-first project
    management stack system.

AUTHOR               : Matt Belfast Brown

CONTACT              : thedayofthedo@gmail.com

MAINTAINER           :
    Matt Belfast Brown (thedayofthedo@gmail.com)


PROJECT CREATE DATE  : 2026-07-15

PROJECT VERSION DATE : 2026-07-15

PROJECT VERSION      : 0.1.0


FILE CREATE DATE     : 2026-07-15

FILE VERSION DATE    : 2026-07-15

FILE VERSION         : 1.0.0


STATUS               : Stable

PYTHON               : >=3.9

LICENSE              : GPL-3.0-only

SPDX ID              : GPL-3.0-only


USAGE                :
    from PLANS import DatabaseManager, StrackManager

    database = DatabaseManager("plans.db")
    database.initialize_schema()
    strack_manager = StrackManager(database)
    strack_manager.create_strack("my-project", "My First Project")

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

# Define the package version string to match PROJECT VERSION in docstring.
__version__ = "0.1.0"
# Export the database manager and entity managers as the public API surface.
__all__ = [
    "DatabaseManager",
    "StrackManager",
    "PlanManager",
    "IssueManager",
    "ActionManager",
    "NoteManager",
]

# Import the DatabaseManager for programmatic database control.
from .database import DatabaseManager
# Import the StrackManager for Strack entity CRUD operations.
from .strack import StrackManager
# Import the PlanManager for Plan entity CRUD operations.
from .plan import PlanManager
# Import the IssueManager for Issue entity CRUD operations.
from .issue import IssueManager
# Import the ActionManager for Action entity CRUD operations.
from .action import ActionManager
# Import the NoteManager for Note entity CRUD operations.
from .note import NoteManager
