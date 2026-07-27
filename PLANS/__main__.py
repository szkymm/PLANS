# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================

MODULE               : PLANS.__main__

TYPE                 : Python Script

DESCRIPTION          :
    CLI entry point for the PLANS local-first project management system.
    Provides subcommands for initializing the SQLite database schema and
    performing full CRUD operations on Strack, Plan, Issue, Action, and
    Note entities through a command-line argument parser with nested
    subcommand routing.

AUTHOR               : Suzuki Yumemi

CONTACT              : szkymm@gmail.com

MAINTAINER           :
    Suzuki Yumemi (szkymm@gmail.com)
    Matt Belfast Brown (thedayofthedo@gmail.com)


PROJECT CREATE DATE  : 2026-07-15

PROJECT VERSION DATE : 2026-07-15

PROJECT VERSION      : 0.1.1


FILE CREATE DATE     : 2026-07-15

FILE VERSION DATE    : 2026-07-15

FILE VERSION         : 1.0.0


STATUS               : Stable

PYTHON               : >=3.9

LICENSE              : GPL-3.0-only

SPDX ID              : GPL-3.0-only


USAGE                :
    PLANS --db /path/to/plans.db init
    PLANS --db /path/to/plans.db strack create ID TITLE [--description DESC] [--priority N]
    PLANS --db /path/to/plans.db strack list [--status STATUS]
    PLANS strack show ID
    PLANS strack update ID [--status STATUS] [--title TITLE] [--description DESC] [--priority N]
    PLANS strack delete ID
    PLANS plan create STRACK_ID PLAN_ID TITLE [--description DESC] [--priority N]
    PLANS plan list [STRACK_ID] [--status STATUS]
    PLANS plan show PLAN_ID
    PLANS plan update PLAN_ID --status STATUS
    PLANS plan delete PLAN_ID
    PLANS issue create STRACK_ID ISSUE_ID TITLE [--description DESC] [--severity SEV]
    PLANS issue list [STRACK_ID] [--status STATUS] [--severity SEV]
    PLANS issue show ISSUE_ID
    PLANS issue update ISSUE_ID --status STATUS
    PLANS issue delete ISSUE_ID
    PLANS action create STRACK_ID ACTION_ID TITLE [--description DESC]
    PLANS action list [STRACK_ID] [--status STATUS]
    PLANS action show ACTION_ID
    PLANS action update ACTION_ID --status STATUS
    PLANS action delete ACTION_ID
    PLANS note create STRACK_ID NOTE_ID TITLE [--content CONTENT]
    PLANS note list [STRACK_ID]
    PLANS note show NOTE_ID
    PLANS note update NOTE_ID [--title TITLE] [--content CONTENT]
    PLANS note delete NOTE_ID

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

# Import the argparse module for command-line argument parsing.
import argparse
# Import the json module for serializing output data structures.
import json
# Import the os module for environment variable and path operations.
import os
# Import the sys module for exit codes and stdout configuration.
import sys
# Import Optional for type hints on optional parameters.
from typing import Optional
# Import Sequence for type hints on argument sequences.
from typing import Sequence

# Import the package version string from the top-level init module.
from . import __version__
# Import the DatabaseManager for schema initialization and connection.
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

# Define the file version to match PROJECT VERSION in docstring.
__version__ = "0.1.1"

# Define the default database file path when no project or env var is set.
default_filepath = "plans.db"
# Define the environment variable name pointing to the database storage directory.
environment_keyname = "COMMON_PLANS_DB"
# Define the set of known top-level commands for project-name detection.
known_commands = {"init", "strack", "plan", "issue", "action", "note"}


def _init_build_parser_function_():
    """
    Construct and return the complete argument parser for the PLANS CLI.

    Builds a nested argparse structure with top-level subcommands for each
    entity type (init, strack, plan, issue, action, note) and second-level
    subcommands for CRUD actions (create, list, show, update, delete).

    :return: The fully configured top-level ArgumentParser instance.
    :rtype: argparse.ArgumentParser
    """
    # Build the CLI description text string.
    description_text = "PLANS \u2014 Priority Logs Actions Notes Stracks\n"
    # Append the system description line.
    description_text += "Local-first project management stack system.\n\n"
    # Append the usage instruction line.
    description_text += "Usage: PLANS [--db PATH] <project> <command> [<args>...]\n\n"
    # Append the project name resolution explanation.
    description_text += "The project name resolves to {COMMON_PLANS_DB}/<project>.db\n"
    # Append the database override explanation.
    description_text += "automatically. Use --db for an explicit file path.\n\n"
    # Append the available commands header.
    description_text += "Available commands:\n"
    # Append the init command help line.
    description_text += "  init              Initialize the PLANS database schema\n"
    # Append the strack create command help line.
    description_text += "  strack create     Create a new Strack container\n"
    # Append the strack list command help line.
    description_text += "  strack list       List all Stracks\n"
    # Append the strack show command help line.
    description_text += "  strack show       Show details of a Strack\n"
    # Append the strack update command help line.
    description_text += "  strack update     Update fields of a Strack\n"
    # Append the strack delete command help line.
    description_text += "  strack delete     Delete a Strack\n"
    # Append the plan create command help line.
    description_text += "  plan create       Create a new Plan (todo) under a Strack\n"
    # Append the plan list command help line.
    description_text += "  plan list         List Plans, optionally filtered by Strack\n"
    # Append the plan show command help line.
    description_text += "  plan show         Show details of a Plan\n"
    # Append the plan update command help line.
    description_text += "  plan update       Update the status of a Plan\n"
    # Append the plan delete command help line.
    description_text += "  plan delete       Delete a Plan\n"
    # Append the issue create command help line.
    description_text += "  issue create      Create a new Issue under a Strack\n"
    # Append the issue list command help line.
    description_text += "  issue list        List Issues, optionally filtered by Strack\n"
    # Append the issue show command help line.
    description_text += "  issue show        Show details of an Issue\n"
    # Append the issue update command help line.
    description_text += "  issue update      Update the status of an Issue\n"
    # Append the issue delete command help line.
    description_text += "  issue delete      Delete an Issue\n"
    # Append the action create command help line.
    description_text += "  action create     Create a new Action under a Strack\n"
    # Append the action list command help line.
    description_text += "  action list       List Actions, optionally filtered by Strack\n"
    # Append the action show command help line.
    description_text += "  action show       Show details of an Action\n"
    # Append the action update command help line.
    description_text += "  action update     Update the status of an Action\n"
    # Append the action delete command help line.
    description_text += "  action delete     Delete an Action\n"
    # Append the note create command help line.
    description_text += "  note create       Create a new Note under a Strack\n"
    # Append the note list command help line.
    description_text += "  note list         List Notes, optionally filtered by Strack\n"
    # Append the note show command help line.
    description_text += "  note show         Show details of a Note\n"
    # Append the note update command help line.
    description_text += "  note update       Update the title or content of a Note\n"
    # Append the note delete command help line.
    description_text += "  note delete       Delete a Note"
    # Build the CLI epilog text string.
    epilog_text = "Full command forms:\n"
    # Append the init command form line.
    epilog_text += "  PLANS <project> init\n"
    # Append the strack create command form with required arguments.
    epilog_text += "  PLANS <project> strack create <id> <title> "
    # Append the optional argument descriptions for the strack create command.
    epilog_text += "[--description DESC] [--priority N]\n"
    # Append the strack list command form line.
    epilog_text += "  PLANS <project> strack list [--status active|archived]\n"
    # Append the strack show command form line.
    epilog_text += "  PLANS <project> strack show <id>\n"
    # Append the strack update command form line.
    epilog_text += "  PLANS <project> strack update <id> [--status STATUS] [--title TITLE] "
    # Append the remaining strack update options.
    epilog_text += "[--description DESC] [--priority N]\n"
    # Append the strack delete command form line.
    epilog_text += "  PLANS <project> strack delete <id>\n"
    # Append the plan create command form line.
    epilog_text += "  PLANS <project> plan create <strack_id> <plan_id> <title> "
    # Append the plan create optional arguments.
    epilog_text += "[--description DESC] [--priority N]\n"
    # Append the plan list command form with filter descriptions.
    epilog_text += "  PLANS <project> plan list [strack_id] "
    # Append the status filter options for the plan list command.
    epilog_text += "[--status pending|in_progress|done|blocked]\n"
    # Append the plan show command form line.
    epilog_text += "  PLANS <project> plan show <plan_id>\n"
    # Append the plan update command form line.
    epilog_text += "  PLANS <project> plan update <plan_id> --status STATUS\n"
    # Append the plan delete command form line.
    epilog_text += "  PLANS <project> plan delete <plan_id>\n"
    # Append the issue create command form line.
    epilog_text += "  PLANS <project> issue create <strack_id> <issue_id> <title> "
    # Append the issue create optional arguments.
    epilog_text += "[--description DESC] [--severity SEV]\n"
    # Append the issue list command form line.
    epilog_text += "  PLANS <project> issue list [strack_id] "
    # Append the issue list filter options.
    epilog_text += "[--status open|in_progress|resolved|closed] [--severity SEV]\n"
    # Append the issue show command form line.
    epilog_text += "  PLANS <project> issue show <issue_id>\n"
    # Append the issue update command form line.
    epilog_text += "  PLANS <project> issue update <issue_id> --status STATUS\n"
    # Append the issue delete command form line.
    epilog_text += "  PLANS <project> issue delete <issue_id>\n"
    # Append the action create command form with required arguments.
    epilog_text += "  PLANS <project> action create <strack_id> <action_id> <title> "
    # Append the optional description flag for the action create command.
    epilog_text += "[--description DESC]\n"
    # Append the action list command form line.
    epilog_text += "  PLANS <project> action list [strack_id] "
    # Append the action list status filter options.
    epilog_text += "[--status pending|in_progress|done|cancelled]\n"
    # Append the action show command form line.
    epilog_text += "  PLANS <project> action show <action_id>\n"
    # Append the action update command form line.
    epilog_text += "  PLANS <project> action update <action_id> --status STATUS\n"
    # Append the action delete command form line.
    epilog_text += "  PLANS <project> action delete <action_id>\n"
    # Append the note create command form with required arguments.
    epilog_text += "  PLANS <project> note create <strack_id> <note_id> <title> "
    # Append the optional content flag for the note create command.
    epilog_text += "[--content CONTENT]\n"
    # Append the note list command form line.
    epilog_text += "  PLANS <project> note list [strack_id]\n"
    # Append the note show command form line.
    epilog_text += "  PLANS <project> note show <note_id>\n"
    # Append the note update command form line.
    epilog_text += "  PLANS <project> note update <note_id> [--title TITLE] [--content CONTENT]\n"
    # Append the note delete command form line.
    epilog_text += "  PLANS <project> note delete <note_id>\n"
    # Create the top-level argument parser with the program description.
    argument_parser = argparse.ArgumentParser(
        # Set the program name for the argument parser.
        prog="PLANS",
        # Configure the help text formatting style.
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Pass the assembled description text to the argument parser.
        description=description_text,
        # Pass the assembled epilog text to the argument parser.
        epilog=epilog_text,
    )
    # Add a global option to specify the database file path for all subcommands.
    argument_parser.add_argument(
    # Execute the following code statement.
        "--db",
        # Specify the namespace attribute for storing the argument value.
        dest="database_path",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Path to the SQLite database file (default: ./plans.db or $COMMON_PLANS_DB).",
    )
    # Display the package version when the version flag is used.
    argument_parser.add_argument(
    # Execute the following code statement.
        "--version",
        # Set the argparse action triggered by this argument.
        action="version",
        # Supply the version string displayed by the flag.
        version=f"PLANS {__version__}",
    )
    # Create subparsers container and build its description text.
    description_subparsers = (
        # Text string describing the project name positional argument behavior.
        "For convenience, the first positional argument is treated as a project\n"
    )
    # Append the automatic resolution explanation.
    description_subparsers += "name and automatic-resolved to {COMMON_PLANS_DB}/<name>.db.\n"
    # Append the database override explanation.
    description_subparsers += "Use --db to override with an explicit file path instead."
    # Create the subparsers group with assembled description text.
    argument_subparsers = argument_parser.add_subparsers(
        # Label the subparser group in help text.
        title="available commands",
        # Specify the namespace attribute for storing the argument value.
        dest="selected_command",
        # Pass the assembled description text to the subparsers factory.
        description=description_subparsers,
    )
    # Create the parser for the init database initialization command.
    initialize_subparser = argument_subparsers.add_parser(
    # Execute the following code statement.
        "init",
        # Provide the help description string for this argument.
        help="Initialize the PLANS database schema.",
    )
    # Build the Strack entity subcommand parser group.
    _init_build_strack_parser_(argument_subparsers)
    # Build the Plan entity subcommand parser group.
    _init_build_plan_parser_(argument_subparsers)
    # Build the Issue entity subcommand parser group.
    _init_build_issue_parser_(argument_subparsers)
    # Build the Action entity subcommand parser group.
    _init_build_action_parser_(argument_subparsers)
    # Build the Note entity subcommand parser group.
    _init_build_note_parser_(argument_subparsers)
    # Return the fully constructed argument parser for dispatch in main.
    return argument_parser


def _init_build_strack_parser_(argument_subparsers):
    """
    Add the Strack entity subcommand group to the argument subparsers.

    Registers create, list, show, update, and delete subcommands for the Strack
    entity type under the top-level 'strack' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Strack entity operations.
    entity_subparser = argument_subparsers.add_parser(
    # Execute the following code statement.
        "strack",
        # Provide the help description string for this argument.
        help="Manage Strack entities (create, list, show, update, delete).",
    )
    # Create the sub-subparsers container for Strack action commands.
    action_subparsers = entity_subparser.add_subparsers(
        # Label the subparser group in help text.
        title="strack_actions",
        # Specify the namespace attribute for storing the argument value.
        dest="selected_action",
    )
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "create",
        # Provide the help description string for this argument.
        help="Create a new Strack.",
    )
    # Add the positional argument for the Strack identifier.
    create_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Provide the help description string for this argument.
        help="Unique identifier for the Strack.",
    )
    # Add the positional argument for the Strack title.
    create_parser.add_argument(
    # Execute the following code statement.
        "entity_title",
        # Provide the help description string for this argument.
        help="Title of the Strack.",
    )
    # Add the optional description flag for the Strack.
    create_parser.add_argument(
    # Execute the following code statement.
        "--description",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_description",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional description of the Strack.",
    )
    # Add the optional priority flag for the Strack.
    create_parser.add_argument(
    # Execute the following code statement.
        "--priority",
        # Specify the namespace attribute for storing the argument value.
        dest="task_priority",
        # Define the type conversion for the argument value.
        type=int,
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional priority level (integer).",
    )
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "list",
        # Provide the help description string for this argument.
        help="List all Stracks.",
    )
    # Add the optional status filter flag for listing.
    list_parser.add_argument(
    # Execute the following code statement.
        "--status",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_status",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Filter Stracks by status.",
    )
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "show",
        # Provide the help description string for this argument.
        help="Show details of a Strack.",
    )
    # Add the positional argument for the Strack identifier to display.
    show_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Provide the help description string for this argument.
        help="Identifier of the Strack to display.",
    )
    # Create the subparser for the update action.
    update_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "update",
        # Provide the help description string for this argument.
        help="Update fields of a Strack.",
    )
    # Add the positional argument for the Strack identifier to update.
    update_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Provide the help description string for this argument.
        help="Identifier of the Strack to update.",
    )
    # Add the optional status flag for updating the Strack status.
    update_parser.add_argument(
    # Execute the following code statement.
        "--status",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_status",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="New status value for the Strack.",
    )
    # Add the optional title flag for updating the Strack title.
    update_parser.add_argument(
    # Execute the following code statement.
        "--title",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_title",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="New title for the Strack.",
    )
    # Add the optional description flag for updating the Strack description.
    update_parser.add_argument(
    # Execute the following code statement.
        "--description",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_description",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="New description for the Strack.",
    )
    # Add the optional priority flag for updating the Strack priority.
    update_parser.add_argument(
    # Execute the following code statement.
        "--priority",
        # Specify the namespace attribute for storing the argument value.
        dest="task_priority",
        # Define the type conversion for the argument value.
        type=int,
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="New priority level (integer) for the Strack.",
    )
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "delete",
        # Provide the help description string for this argument.
        help="Delete a Strack.",
    )
    # Add the positional argument for the Strack identifier to delete.
    delete_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Provide the help description string for this argument.
        help="Identifier of the Strack to delete.",
    )


def _init_build_plan_parser_(argument_subparsers):
    """
    Add the Plan entity subcommand group to the argument subparsers.

    Registers create, list, show, update, and delete subcommands for the
    Plan entity type under the top-level 'plan' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Plan entity operations.
    entity_subparser = argument_subparsers.add_parser(
    # Execute the following code statement.
        "plan",
        # Provide the help description string for this argument.
        help="Manage Plan entities (create, list, show, update, delete).",
    )
    # Create the sub-subparsers container for Plan action commands.
    action_subparsers = entity_subparser.add_subparsers(
        # Label the subparser group in help text.
        title="plan_actions",
        # Specify the namespace attribute for storing the argument value.
        dest="selected_action",
    )
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "create",
        # Provide the help description string for this argument.
        help="Create a new Plan under a Strack.",
    )
    # Add the positional argument for the parent Strack identifier.
    create_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Provide the help description string for this argument.
        help="Identifier of the parent Strack.",
    )
    # Add the positional argument for the Plan identifier.
    create_parser.add_argument(
    # Execute the following code statement.
        "plan_id",
        # Provide the help description string for this argument.
        help="Unique identifier for the Plan.",
    )
    # Add the positional argument for the Plan title.
    create_parser.add_argument(
    # Execute the following code statement.
        "entity_title",
        # Provide the help description string for this argument.
        help="Title of the Plan.",
    )
    # Add the optional description flag for the Plan.
    create_parser.add_argument(
    # Execute the following code statement.
        "--description",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_description",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional description of the Plan.",
    )
    # Add the optional priority flag for the Plan.
    create_parser.add_argument(
    # Execute the following code statement.
        "--priority",
        # Specify the namespace attribute for storing the argument value.
        dest="task_priority",
        # Define the type conversion for the argument value.
        type=int,
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional priority level (integer).",
    )
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "list",
        # Provide the help description string for this argument.
        help="List Plans, optionally filtered by Strack.",
    )
    # Add the optional positional argument for filtering by parent Strack.
    list_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Specify how many values the argument consumes.
        nargs="?",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional parent Strack identifier to filter by.",
    )
    # Add the optional status filter flag for listing.
    list_parser.add_argument(
    # Execute the following code statement.
        "--status",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_status",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Filter Plans by status.",
    )
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "show",
        # Provide the help description string for this argument.
        help="Show details of a Plan.",
    )
    # Add the positional argument for the Plan identifier to display.
    show_parser.add_argument(
    # Execute the following code statement.
        "plan_id",
        # Provide the help description string for this argument.
        help="Identifier of the Plan to display.",
    )
    # Create the subparser for the update action.
    update_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "update",
        # Provide the help description string for this argument.
        help="Update the status of a Plan.",
    )
    # Add the positional argument for the Plan identifier to update.
    update_parser.add_argument(
    # Execute the following code statement.
        "plan_id",
        # Provide the help description string for this argument.
        help="Identifier of the Plan to update.",
    )
    # Add the required status flag to set the new Plan status.
    update_parser.add_argument(
    # Execute the following code statement.
        "--status",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_status",
        # Indicate whether the argument is mandatory.
        required=True,
        # Provide the help description string for this argument.
        help="New status value for the Plan.",
    )
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "delete",
        # Provide the help description string for this argument.
        help="Delete a Plan.",
    )
    # Add the positional argument for the Plan identifier to delete.
    delete_parser.add_argument(
    # Execute the following code statement.
        "plan_id",
        # Provide the help description string for this argument.
        help="Identifier of the Plan to delete.",
    )


def _init_build_issue_parser_(argument_subparsers):
    """
    Add the Issue entity subcommand group to the argument subparsers.

    Registers create, list, show, update, and delete subcommands for the
    Issue entity type under the top-level 'issue' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Issue entity operations.
    entity_subparser = argument_subparsers.add_parser(
    # Execute the following code statement.
        "issue",
        # Provide the help description string for this argument.
        help="Manage Issue entities (create, list, show, update, delete).",
    )
    # Create the sub-subparsers container for Issue action commands.
    action_subparsers = entity_subparser.add_subparsers(
        # Label the subparser group in help text.
        title="issue_actions",
        # Specify the namespace attribute for storing the argument value.
        dest="selected_action",
    )
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "create",
        # Provide the help description string for this argument.
        help="Create a new Issue under a Strack.",
    )
    # Add the positional argument for the parent Strack identifier.
    create_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Provide the help description string for this argument.
        help="Identifier of the parent Strack.",
    )
    # Add the positional argument for the Issue identifier.
    create_parser.add_argument(
    # Execute the following code statement.
        "issue_id",
        # Provide the help description string for this argument.
        help="Unique identifier for the Issue.",
    )
    # Add the positional argument for the Issue title.
    create_parser.add_argument(
    # Execute the following code statement.
        "entity_title",
        # Provide the help description string for this argument.
        help="Title of the Issue.",
    )
    # Add the optional description flag for the Issue.
    create_parser.add_argument(
    # Execute the following code statement.
        "--description",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_description",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional description of the Issue.",
    )
    # Add the optional severity flag for the Issue.
    create_parser.add_argument(
    # Execute the following code statement.
        "--severity",
        # Specify the namespace attribute for storing the argument value.
        dest="issue_severity",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional severity level (e.g., low, medium, high, critical).",
    )
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "list",
        # Provide the help description string for this argument.
        help="List Issues, optionally filtered by Strack.",
    )
    # Add the optional positional argument for filtering by parent Strack.
    list_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Specify how many values the argument consumes.
        nargs="?",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional parent Strack identifier to filter by.",
    )
    # Add the optional status filter flag for listing.
    list_parser.add_argument(
    # Execute the following code statement.
        "--status",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_status",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Filter Issues by status.",
    )
    # Add the optional severity filter flag for listing.
    list_parser.add_argument(
    # Execute the following code statement.
        "--severity",
        # Specify the namespace attribute for storing the argument value.
        dest="issue_severity",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Filter Issues by severity.",
    )
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "show",
        # Provide the help description string for this argument.
        help="Show details of an Issue.",
    )
    # Add the positional argument for the Issue identifier to display.
    show_parser.add_argument(
    # Execute the following code statement.
        "issue_id",
        # Provide the help description string for this argument.
        help="Identifier of the Issue to display.",
    )
    # Create the subparser for the update action.
    update_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "update",
        # Provide the help description string for this argument.
        help="Update the status of an Issue.",
    )
    # Add the positional argument for the Issue identifier to update.
    update_parser.add_argument(
    # Execute the following code statement.
        "issue_id",
        # Provide the help description string for this argument.
        help="Identifier of the Issue to update.",
    )
    # Add the required status flag to set the new Issue status.
    update_parser.add_argument(
    # Execute the following code statement.
        "--status",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_status",
        # Indicate whether the argument is mandatory.
        required=True,
        # Provide the help description string for this argument.
        help="New status value for the Issue.",
    )
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "delete",
        # Provide the help description string for this argument.
        help="Delete an Issue.",
    )
    # Add the positional argument for the Issue identifier to delete.
    delete_parser.add_argument(
    # Execute the following code statement.
        "issue_id",
        # Provide the help description string for this argument.
        help="Identifier of the Issue to delete.",
    )


def _init_build_action_parser_(argument_subparsers):
    """
    Add the Action entity subcommand group to the argument subparsers.

    Registers create, list, show, update, and delete subcommands for the
    Action entity type under the top-level 'action' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Action entity operations.
    entity_subparser = argument_subparsers.add_parser(
    # Execute the following code statement.
        "action",
        # Provide the help description string for this argument.
        help="Manage Action entities (create, list, show, update, delete).",
    )
    # Create the sub-subparsers container for Action action commands.
    action_subparsers = entity_subparser.add_subparsers(
        # Label the subparser group in help text.
        title="action_actions",
        # Specify the namespace attribute for storing the argument value.
        dest="selected_action",
    )
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "create",
        # Provide the help description string for this argument.
        help="Create a new Action under a Strack.",
    )
    # Add the positional argument for the parent Strack identifier.
    create_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Provide the help description string for this argument.
        help="Identifier of the parent Strack.",
    )
    # Add the positional argument for the Action identifier.
    create_parser.add_argument(
    # Execute the following code statement.
        "action_id",
        # Provide the help description string for this argument.
        help="Unique identifier for the Action.",
    )
    # Add the positional argument for the Action title.
    create_parser.add_argument(
    # Execute the following code statement.
        "entity_title",
        # Provide the help description string for this argument.
        help="Title of the Action.",
    )
    # Add the optional description flag for the Action.
    create_parser.add_argument(
    # Execute the following code statement.
        "--description",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_description",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional description of the Action.",
    )
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "list",
        # Provide the help description string for this argument.
        help="List Actions, optionally filtered by Strack.",
    )
    # Add the optional positional argument for filtering by parent Strack.
    list_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Specify how many values the argument consumes.
        nargs="?",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional parent Strack identifier to filter by.",
    )
    # Add the optional status filter flag for listing.
    list_parser.add_argument(
    # Execute the following code statement.
        "--status",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_status",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Filter Actions by status.",
    )
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "show",
        # Provide the help description string for this argument.
        help="Show details of an Action.",
    )
    # Add the positional argument for the Action identifier to display.
    show_parser.add_argument(
    # Execute the following code statement.
        "action_id",
        # Provide the help description string for this argument.
        help="Identifier of the Action to display.",
    )
    # Create the subparser for the update action.
    update_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "update",
        # Provide the help description string for this argument.
        help="Update the status of an Action.",
    )
    # Add the positional argument for the Action identifier to update.
    update_parser.add_argument(
    # Execute the following code statement.
        "action_id",
        # Provide the help description string for this argument.
        help="Identifier of the Action to update.",
    )
    # Add the required status flag to set the new Action status.
    update_parser.add_argument(
    # Execute the following code statement.
        "--status",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_status",
        # Indicate whether the argument is mandatory.
        required=True,
        # Provide the help description string for this argument.
        help="New status value for the Action.",
    )
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "delete",
        # Provide the help description string for this argument.
        help="Delete an Action.",
    )
    # Add the positional argument for the Action identifier to delete.
    delete_parser.add_argument(
    # Execute the following code statement.
        "action_id",
        # Provide the help description string for this argument.
        help="Identifier of the Action to delete.",
    )


def _init_build_note_parser_(argument_subparsers):
    """
    Add the Note entity subcommand group to the argument subparsers.

    Registers create, list, show, update, and delete subcommands for the
    Note entity type under the top-level 'note' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Note entity operations.
    entity_subparser = argument_subparsers.add_parser(
    # Execute the following code statement.
        "note",
        # Provide the help description string for this argument.
        help="Manage Note entities (create, list, show, update, delete).",
    )
    # Create the sub-subparsers container for Note action commands.
    action_subparsers = entity_subparser.add_subparsers(
        # Label the subparser group in help text.
        title="note_actions",
        # Specify the namespace attribute for storing the argument value.
        dest="selected_action",
    )
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "create",
        # Provide the help description string for this argument.
        help="Create a new Note under a Strack.",
    )
    # Add the positional argument for the parent Strack identifier.
    create_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Provide the help description string for this argument.
        help="Identifier of the parent Strack.",
    )
    # Add the positional argument for the Note identifier.
    create_parser.add_argument(
    # Execute the following code statement.
        "note_id",
        # Provide the help description string for this argument.
        help="Unique identifier for the Note.",
    )
    # Add the positional argument for the Note title.
    create_parser.add_argument(
    # Execute the following code statement.
        "entity_title",
        # Provide the help description string for this argument.
        help="Title of the Note.",
    )
    # Add the optional content flag for the Note body text.
    create_parser.add_argument(
    # Execute the following code statement.
        "--content",
        # Specify the namespace attribute for storing the argument value.
        dest="note_content",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional content body of the Note.",
    )
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "list",
        # Provide the help description string for this argument.
        help="List Notes, optionally filtered by Strack.",
    )
    # Add the optional positional argument for filtering by parent Strack.
    list_parser.add_argument(
    # Execute the following code statement.
        "strack_id",
        # Specify how many values the argument consumes.
        nargs="?",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="Optional parent Strack identifier to filter by.",
    )
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "show",
        # Provide the help description string for this argument.
        help="Show details of a Note.",
    )
    # Add the positional argument for the Note identifier to display.
    show_parser.add_argument(
    # Execute the following code statement.
        "note_id",
        # Provide the help description string for this argument.
        help="Identifier of the Note to display.",
    )
    # Create the subparser for the update action.
    update_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "update",
        # Provide the help description string for this argument.
        help="Update the title or content of a Note.",
    )
    # Add the positional argument for the Note identifier to update.
    update_parser.add_argument(
    # Execute the following code statement.
        "note_id",
        # Provide the help description string for this argument.
        help="Identifier of the Note to update.",
    )
    # Add the optional title flag to update the Note title.
    update_parser.add_argument(
    # Execute the following code statement.
        "--title",
        # Specify the namespace attribute for storing the argument value.
        dest="entity_title",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="New title for the Note.",
    )
    # Add the optional content flag to update the Note body text.
    update_parser.add_argument(
    # Execute the following code statement.
        "--content",
        # Specify the namespace attribute for storing the argument value.
        dest="note_content",
        # Set the fallback value when the argument is omitted.
        default=None,
        # Provide the help description string for this argument.
        help="New content body for the Note.",
    )
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
    # Execute the following code statement.
        "delete",
        # Provide the help description string for this argument.
        help="Delete a Note.",
    )
    # Add the positional argument for the Note identifier to delete.
    delete_parser.add_argument(
    # Execute the following code statement.
        "note_id",
        # Provide the help description string for this argument.
        help="Identifier of the Note to delete.",
    )


def main(arguments_list=None):
    """
    Execute the PLANS command-line interface entry point.

    Supports project-first syntax: when the first positional argument is
    not a recognized command, it is treated as a project name and the
    database path is automatic-resolved from COMMON_PLANS_DB or current directory.
    This enables `plans myproject strack create ...` without explicit --db.

    The parameters are as follows:

    :param arguments_list: Optional pre-parsed argument list for testing.
    :type arguments_list: Optional[Sequence[str]]
    :return: Exit code 0 for success, 1 for failure.
    :rtype: int
    """
    # Reconfigure standard output to use UTF-8 encoding for cross-platform support.
    sys.stdout.reconfigure(encoding="utf-8")
    # Determine the argument list to process, defaulting to sys.argv.
    if arguments_list is not None:
        # Use the explicitly provided argument list for programmatic invocations.
        list_arguments = list(arguments_list)
    # Execute the following code statement.
    else:
        # Copy system arguments excluding the program name itself.
        list_arguments = list(sys.argv[1:])
    # Detect and extract a project name as the first positional argument.
    project_name = None
    # Validate that the first argument is a project name, not a command flag.
    if (
        # Access the first positional argument for validation.
        list_arguments
        # Exclude arguments that match known CLI command identifiers.
        and list_arguments[0] not in known_commands
        # Exclude arguments that begin with a dash like option flags.
        and not list_arguments[0].startswith("-")
    # The body executes when the argument passes project-name validation.
    ):
        # Pop the first argument as the project name for path resolution.
        project_name = list_arguments.pop(0)
    # Resolve the database path from the project name when provided.
    if project_name is not None:
        # Determine the base directory from environment variable or current directory.
        string_base = os.environ.get(environment_keyname, ".")
        # Construct the full database file path from directory and project name.
        database_path = os.path.join(string_base, f"{project_name}.db")
        # Inject the resolved --db flag into the remaining argument list for the parser.
        list_arguments = ["--db", database_path] + list_arguments
    # Build the full argument parser structure via the private builder.
    argument_parser = _init_build_parser_function_()
    # Parse the processed command-line arguments into a namespace object.
    parsed_arguments = argument_parser.parse_args(list_arguments)
    # Retrieve the selected top-level command from the parsed namespace.
    selected_command = getattr(parsed_arguments, "selected_command", None)
    # Resolve the database file path from --db, env variable, or default fallback.
    database_path = getattr(parsed_arguments, "database_path", None)
    # Fall back to the environment variable when no explicit path was provided.
    if database_path is None:
        # Attempt to read the database path from the environment variable.
        database_path = os.environ.get(
    # Execute the following code statement.
            environment_keyname,
    # Execute the following code statement.
            default_filepath,
        )
    # Display project-oriented help when a project name is given without a command.
    if selected_command is None:
        # Print the command-line help text when no recognized command was given.
        argument_parser.print_help()
        # Show a hint about the detected project name for better user guidance.
        if project_name is not None:
            # Print a tip showing the resolved database path for the project.
            print(f"\n  Tip: project '{project_name}' resolves to '{database_path}'")
            # Suggest example commands to help the user get started.
            print(f"  Try: plans {project_name} strack list")
        # Return exit code 0 since displaying help is not an error.
        return 0
    # Dispatch to the init handler for database initialization.
    if selected_command == "init":
        # Delegate to the init handler with the resolved database path.
        return _init_main_handle_init_(database_path)
    # For all entity commands, ensure the database file exists first.
    if not os.path.isfile(database_path):
        # Prepare the Chinese error message for missing database file.
        message_error = "[X] 数据库文件不存在，请先运行 'PLANS <project> init' 初始化数据库: "
    # Assign a value to the variable for subsequent use.
        message_error += database_path
        # Print the error message since no logger is configured in CLI mode.
        print(message_error)
        # Return exit code 1 to indicate a fatal configuration error.
        return 1
    # Retrieve the selected entity action from the parsed namespace.
    selected_action = getattr(parsed_arguments, "selected_action", None)
    # Dispatch to the appropriate entity handler based on the top-level command.
    if selected_command == "strack":
        # Delegate to the Strack entity handler for the selected action.
        return _init_main_handle_strack_(
    # Execute the following code statement.
            database_path,
    # Execute the following code statement.
            selected_action,
    # Execute the following code statement.
            parsed_arguments,
        )
    # Evaluate the conditional expression for branching.
    if selected_command == "plan":
        # Delegate to the Plan entity handler for the selected action.
        return _init_main_handle_plan_(
    # Execute the following code statement.
            database_path,
    # Execute the following code statement.
            selected_action,
    # Execute the following code statement.
            parsed_arguments,
        )
    # Evaluate the conditional expression for branching.
    if selected_command == "issue":
        # Delegate to the Issue entity handler for the selected action.
        return _init_main_handle_issue_(
    # Execute the following code statement.
            database_path,
    # Execute the following code statement.
            selected_action,
    # Execute the following code statement.
            parsed_arguments,
        )
    # Evaluate the conditional expression for branching.
    if selected_command == "action":
        # Delegate to the Action entity handler for the selected action.
        return _init_main_handle_action_(
    # Execute the following code statement.
            database_path,
    # Execute the following code statement.
            selected_action,
    # Execute the following code statement.
            parsed_arguments,
        )
    # Evaluate the conditional expression for branching.
    if selected_command == "note":
        # Delegate to the Note entity handler for the selected action.
        return _init_main_handle_note_(
    # Execute the following code statement.
            database_path,
    # Execute the following code statement.
            selected_action,
    # Execute the following code statement.
            parsed_arguments,
        )
    # Print the unrecognized command error and return failure exit code.
    print(f"[X] 未知命令: {selected_command}")
    # Return exit code 1 for unrecognized top-level commands.
    return 1


def _init_main_handle_init_(database_path):
    """
    Handle the init subcommand to initialize the PLANS database.

    Creates a new DatabaseManager instance and calls initialize_schema
    to set up the SQLite database tables for all five entity types.

    :param database_path: The resolved path to the database file.
    :type database_path: str
    :return: Exit code 0 for success, 1 for failure.
    :rtype: int
    """
    # Attempt to initialize the database schema at the specified path.
    try:
        # Instantiate the DatabaseManager with the resolved database path.
        database_manager = DatabaseManager(database_path)
        # Execute the schema initialization to create all required tables.
        database_manager.initialize_schema()
    # Catch and process the named exception type.
    except FileNotFoundError as filenotfound_error:
        # Build the Chinese error message for path-related failures.
        message_error = "[X] (FileNotFoundError) 数据库路径无效或无法访问: "
    # Assign a value to the variable for subsequent use.
        message_error += str(filenotfound_error)
        # Print the error message for the user to diagnose.
        print(message_error)
        # Return exit code 1 to indicate initialization failure.
        return 1
    # Catch and process the named exception type.
    except PermissionError as permission_error:
        # Build the Chinese error message for permission-denied failures.
        message_error = "[X] (PermissionError) 无权限创建或写入数据库文件: "
    # Assign a value to the variable for subsequent use.
        message_error += str(permission_error)
        # Print the error message for the user to diagnose.
        print(message_error)
        # Return exit code 1 to indicate initialization failure.
        return 1
    # Catch and process the named exception type.
    except Exception as exception_error:
        # Build the Chinese error message for any unanticipated failures.
        message_error = "[X] (OtherError) 数据库初始化时发生未知错误: "
    # Assign a value to the variable for subsequent use.
        message_error += str(exception_error)
        # Print the error message for the user to diagnose.
        print(message_error)
        # Return exit code 1 to indicate initialization failure.
        return 1
    # Print the success confirmation message in Chinese.
    print(f"[OK] 数据库初始化成功: {database_path}")
    # Return exit code 0 to indicate successful initialization.
    return 0


def _init_main_handle_strack_(database_path, selected_action, parsed_arguments):
    """
    Dispatch the selected Strack action to the appropriate handler.

    Routes create, list, show, update, and delete actions to their respective
    StrackManager method calls and formats the output.

    :param database_path: The resolved path to the database file.
    :type database_path: str
    :param selected_action: The action subcommand (create, list, show, update, delete).
    :type selected_action: str
    :param parsed_arguments: The parsed command-line argument namespace.
    :type parsed_arguments: argparse.Namespace
    :return: Exit code 0 for success, 1 for failure.
    :rtype: int
    """
    # Instantiate the DatabaseManager for the resolved database path.
    database_manager = DatabaseManager(database_path)
    # Create the StrackManager instance bound to the database connection.
    strack_manager = StrackManager(database_manager)
    # Dispatch to the create handler for the Strack create action.
    if selected_action == "create":
        # Attempt to create a new Strack with the provided parameters.
        try:
            # Call the StrackManager insert method with parsed arguments.
            entity_result = strack_manager.insert_strack_record(
    # Execute the following code statement.
                parsed_arguments.strack_id,
    # Execute the following code statement.
                parsed_arguments.entity_title,
    # Assign a value to the variable for subsequent use.
                item_description=parsed_arguments.entity_description or "",
    # Assign a value to the variable for subsequent use.
                priority_level=parsed_arguments.task_priority or 3,
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Strack 创建参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Strack 创建时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        # Print the created Strack entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful creation.
        return 0
    # Dispatch to the list handler for the Strack list action.
    if selected_action == "list":
        # Attempt to retrieve the list of Strack entities.
        try:
            # Call the StrackManager list method with optional status filter.
            entity_result = strack_manager.list_stracks(
    # Assign a value to the variable for subsequent use.
                item_status=parsed_arguments.entity_status,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Strack 列表查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the list operation failed.
            return 1
        # Print the list of Strack entities as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful listing.
        return 0
    # Dispatch to the show handler for the Strack show action.
    if selected_action == "show":
        # Attempt to retrieve the single Strack by its identifier.
        try:
            # Call the StrackManager retrieve method with the Strack identifier.
            entity_result = strack_manager.retrieve_strack(
    # Execute the following code statement.
                parsed_arguments.strack_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Strack 查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Verify that the Strack entity exists in the database before proceeding.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Strack 未找到: "
    # Assign a value to the variable for subsequent use.
            message_error += parsed_arguments.strack_id
            # Print the error message to standard output.
            print(message_error)
            # Return exit code 1 to indicate the entity was not found.
            return 1
        # Print the Strack details as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful retrieval.
        return 0
    # Dispatch to the update handler for the Strack update action.
    if selected_action == "update":
        # Build the keyword arguments dictionary from non-None optional flags.
        keyword_arguments = {}
        # Conditionally add the status field when provided by the user.
        if parsed_arguments.entity_status is not None:
            # Set the Status PascalCase key in the update keyword dictionary.
            keyword_arguments["Status"] = parsed_arguments.entity_status
        # Conditionally add the title field when provided by the user.
        if parsed_arguments.entity_title is not None:
            # Set the Title PascalCase key in the update keyword dictionary.
            keyword_arguments["Title"] = parsed_arguments.entity_title
        # Conditionally add the description field when provided by the user.
        if parsed_arguments.entity_description is not None:
            # Set the Description PascalCase key in the update keyword dictionary.
            keyword_arguments["Description"] = parsed_arguments.entity_description
        # Conditionally add the priority field when provided by the user.
        if parsed_arguments.task_priority is not None:
            # Set the Priority PascalCase key in the update keyword dictionary.
            keyword_arguments["Priority"] = parsed_arguments.task_priority
        # Attempt to update the Strack with the provided keyword arguments.
        try:
            # Call the StrackManager modify method with the update keywords.
            entity_result = strack_manager.modify_strack_fields(
    # Execute the following code statement.
                parsed_arguments.strack_id,
    # Unpack the keyword arguments dictionary into the modify method call.
                **keyword_arguments,
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Strack 更新参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Strack 更新时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
        # Verify that the Strack entity was found for the update.
        if entity_result is None or not entity_result:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Strack 未找到: "
    # Assign a value to the variable for subsequent use.
            message_error += parsed_arguments.strack_id
            # Print the error message to standard output.
            print(message_error)
            # Return exit code 1 to indicate the entity was not found.
            return 1
        # Print the updated Strack entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful update.
        return 0
    # Dispatch to the delete handler for the Strack delete action.
    if selected_action == "delete":
        # Attempt to delete the Strack by its identifier.
        try:
            # Call the StrackManager erase method with the Strack identifier.
            is_deleted = strack_manager.erase_strack_record(
    # Execute the following code statement.
                parsed_arguments.strack_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Strack 删除时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the delete operation failed.
            return 1
        # Verify that the deletion was successful.
        if is_deleted:
            # Print the success confirmation message in Chinese.
            print(f"[OK] Strack 已删除: {parsed_arguments.strack_id}")
            # Return exit code 0 to indicate successful deletion.
            return 0
        # Prepare the Chinese error message for entity not found during deletion.
        message_error = "[X] Strack 未找到，无法删除: "
    # Assign a value to the variable for subsequent use.
        message_error += parsed_arguments.strack_id
        # Print the error message to standard output.
        print(message_error)
        # Return exit code 1 to indicate the entity was not found.
        return 1
    # Print the unrecognized action error and return failure exit code.
    print(f"[X] Strack 未知操作: {selected_action}")
    # Return exit code 1 for unrecognized Strack actions.
    return 1


def _init_main_handle_plan_(database_path, selected_action, parsed_arguments):
    """
    Dispatch the selected Plan action to the appropriate handler.

    Routes create, list, show, update, and delete actions to their
    respective PlanManager method calls and formats the output.

    :param database_path: The resolved path to the database file.
    :type database_path: str
    :param selected_action: The action subcommand (create, list, show, update, delete).
    :type selected_action: str
    :param parsed_arguments: The parsed command-line argument namespace.
    :type parsed_arguments: argparse.Namespace
    :return: Exit code 0 for success, 1 for failure.
    :rtype: int
    """
    # Instantiate the DatabaseManager for the resolved database path.
    database_manager = DatabaseManager(database_path)
    # Create the PlanManager instance bound to the database connection.
    plan_manager = PlanManager(database_manager)
    # Dispatch to the create handler for the Plan create action.
    if selected_action == "create":
        # Attempt to create a new Plan with the provided parameters.
        try:
            # Call the PlanManager insert method with parsed arguments.
            entity_result = plan_manager.insert_plan_record(
    # Execute the following code statement.
                parsed_arguments.strack_id,
    # Execute the following code statement.
                parsed_arguments.plan_id,
    # Execute the following code statement.
                parsed_arguments.entity_title,
    # Assign a value to the variable for subsequent use.
                plan_description=parsed_arguments.entity_description or "",
    # Assign a value to the variable for subsequent use.
                priority_level=parsed_arguments.task_priority or 3,
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Plan 创建参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 创建时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        # Print the created Plan entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful creation.
        return 0
    # Dispatch to the list handler for the Plan list action.
    if selected_action == "list":
        # Attempt to retrieve the list of Plan entities.
        try:
            # Call the PlanManager list method with optional filters.
            entity_result = plan_manager.list_plans(
    # Assign a value to the variable for subsequent use.
                strack_id=parsed_arguments.strack_id,
    # Assign a value to the variable for subsequent use.
                status_value=parsed_arguments.entity_status,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 列表查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the list operation failed.
            return 1
        # Print the list of Plan entities as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful listing.
        return 0
    # Dispatch to the show handler for the Plan show action.
    if selected_action == "show":
        # Attempt to retrieve the single Plan by its identifier.
        try:
            # Call the PlanManager retrieve method with the Plan identifier.
            entity_result = plan_manager.retrieve_plan(
    # Execute the following code statement.
                parsed_arguments.plan_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Verify that the Plan entity exists in the database before proceeding.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Plan 未找到: "
    # Assign a value to the variable for subsequent use.
            message_error += parsed_arguments.plan_id
            # Print the error message to standard output.
            print(message_error)
            # Return exit code 1 to indicate the entity was not found.
            return 1
        # Print the Plan details as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful retrieval.
        return 0
    # Dispatch to the update handler for the Plan update action.
    if selected_action == "update":
        # Attempt to update the Plan status with the provided value.
        try:
            # Call the PlanManager modify method with the new status.
            entity_result = plan_manager.modify_plan_fields(
    # Execute the following code statement.
                parsed_arguments.plan_id,
    # Assign a value to the variable for subsequent use.
                Status=parsed_arguments.entity_status,
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Plan 更新参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 更新时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
        # Print the updated Plan entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful update.
        return 0
    # Dispatch to the delete handler for the Plan delete action.
    if selected_action == "delete":
        # Attempt to delete the Plan by its identifier.
        try:
            # Call the PlanManager erase method with the Plan identifier.
            is_deleted = plan_manager.erase_plan_record(
    # Execute the following code statement.
                parsed_arguments.plan_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 删除时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the delete operation failed.
            return 1
        # Verify that the deletion was successful.
        if is_deleted:
            # Print the success confirmation message in Chinese.
            print(f"[OK] Plan 已删除: {parsed_arguments.plan_id}")
            # Return exit code 0 to indicate successful deletion.
            return 0
        # Prepare the Chinese error message for entity not found during deletion.
        message_error = "[X] Plan 未找到，无法删除: "
    # Assign a value to the variable for subsequent use.
        message_error += parsed_arguments.plan_id
        # Print the error message to standard output.
        print(message_error)
        # Return exit code 1 to indicate the entity was not found.
        return 1
    # Print the unrecognized action error and return failure exit code.
    print(f"[X] Plan 未知操作: {selected_action}")
    # Return exit code 1 for unrecognized Plan actions.
    return 1


def _init_main_handle_issue_(database_path, selected_action, parsed_arguments):
    """
    Dispatch the selected Issue action to the appropriate handler.

    Routes create, list, show, update, and delete actions to their
    respective IssueManager method calls and formats the output.

    :param database_path: The resolved path to the database file.
    :type database_path: str
    :param selected_action: The action subcommand (create, list, show, update, delete).
    :type selected_action: str
    :param parsed_arguments: The parsed command-line argument namespace.
    :type parsed_arguments: argparse.Namespace
    :return: Exit code 0 for success, 1 for failure.
    :rtype: int
    """
    # Instantiate the DatabaseManager for the resolved database path.
    database_manager = DatabaseManager(database_path)
    # Create the IssueManager instance bound to the database connection.
    issue_manager = IssueManager(database_manager)
    # Dispatch to the create handler for the Issue create action.
    if selected_action == "create":
        # Attempt to create a new Issue with the provided parameters.
        try:
            # Call the IssueManager insert method with parsed arguments.
            entity_result = issue_manager.insert_issue_record(
    # Execute the following code statement.
                parsed_arguments.strack_id,
    # Execute the following code statement.
                parsed_arguments.issue_id,
    # Execute the following code statement.
                parsed_arguments.entity_title,
    # Assign a value to the variable for subsequent use.
                item_description=parsed_arguments.entity_description or "",
    # Assign a value to the variable for subsequent use.
                severity_level=parsed_arguments.issue_severity or "medium",
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Issue 创建参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 创建时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        # Print the created Issue entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful creation.
        return 0
    # Dispatch to the list handler for the Issue list action.
    if selected_action == "list":
        # Attempt to retrieve the list of Issue entities.
        try:
            # Call the IssueManager list method with optional filters.
            entity_result = issue_manager.list_issues(
    # Assign a value to the variable for subsequent use.
                strack_id=parsed_arguments.strack_id,
    # Assign a value to the variable for subsequent use.
                item_status=parsed_arguments.entity_status,
    # Assign a value to the variable for subsequent use.
                severity_level=parsed_arguments.issue_severity,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 列表查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the list operation failed.
            return 1
        # Print the list of Issue entities as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful listing.
        return 0
    # Dispatch to the show handler for the Issue show action.
    if selected_action == "show":
        # Attempt to retrieve the single Issue by its identifier.
        try:
            # Call the IssueManager retrieve method with the Issue identifier.
            entity_result = issue_manager.retrieve_issue(
    # Execute the following code statement.
                parsed_arguments.issue_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Verify that the Issue entity exists in the database before proceeding.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Issue 未找到: "
    # Assign a value to the variable for subsequent use.
            message_error += parsed_arguments.issue_id
            # Print the error message to standard output.
            print(message_error)
            # Return exit code 1 to indicate the entity was not found.
            return 1
        # Print the Issue details as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful retrieval.
        return 0
    # Dispatch to the update handler for the Issue update action.
    if selected_action == "update":
        # Attempt to update the Issue status with the provided value.
        try:
            # Call the IssueManager modify method with the new status.
            entity_result = issue_manager.modify_issue_fields(
    # Execute the following code statement.
                parsed_arguments.issue_id,
    # Assign a value to the variable for subsequent use.
                Status=parsed_arguments.entity_status,
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Issue 更新参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 更新时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
        # Print the updated Issue entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful update.
        return 0
    # Dispatch to the delete handler for the Issue delete action.
    if selected_action == "delete":
        # Attempt to delete the Issue by its identifier.
        try:
            # Call the IssueManager erase method with the Issue identifier.
            is_deleted = issue_manager.erase_issue_record(
    # Execute the following code statement.
                parsed_arguments.issue_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 删除时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the delete operation failed.
            return 1
        # Verify that the deletion was successful.
        if is_deleted:
            # Print the success confirmation message in Chinese.
            print(f"[OK] Issue 已删除: {parsed_arguments.issue_id}")
            # Return exit code 0 to indicate successful deletion.
            return 0
        # Prepare the Chinese error message for entity not found during deletion.
        message_error = "[X] Issue 未找到，无法删除: "
    # Assign a value to the variable for subsequent use.
        message_error += parsed_arguments.issue_id
        # Print the error message to standard output.
        print(message_error)
        # Return exit code 1 to indicate the entity was not found.
        return 1
    # Print the unrecognized action error and return failure exit code.
    print(f"[X] Issue 未知操作: {selected_action}")
    # Return exit code 1 for unrecognized Issue actions.
    return 1


def _init_main_handle_action_(database_path, selected_action, parsed_arguments):
    """
    Dispatch the selected Action action to the appropriate handler.

    Routes create, list, show, update, and delete actions to their
    respective ActionManager method calls and formats the output.

    :param database_path: The resolved path to the database file.
    :type database_path: str
    :param selected_action: The action subcommand (create, list, show, update, delete).
    :type selected_action: str
    :param parsed_arguments: The parsed command-line argument namespace.
    :type parsed_arguments: argparse.Namespace
    :return: Exit code 0 for success, 1 for failure.
    :rtype: int
    """
    # Instantiate the DatabaseManager for the resolved database path.
    database_manager = DatabaseManager(database_path)
    # Create the ActionManager instance bound to the database connection.
    action_manager = ActionManager(database_manager)
    # Dispatch to the create handler for the Action create action.
    if selected_action == "create":
        # Attempt to create a new Action with the provided parameters.
        try:
            # Call the ActionManager insert method with parsed arguments.
            entity_result = action_manager.insert_action_record(
    # Execute the following code statement.
                parsed_arguments.strack_id,
    # Execute the following code statement.
                parsed_arguments.action_id,
    # Execute the following code statement.
                parsed_arguments.entity_title,
    # Assign a value to the variable for subsequent use.
                item_description=parsed_arguments.entity_description or "",
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Action 创建参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 创建时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        # Print the created Action entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful creation.
        return 0
    # Dispatch to the list handler for the Action list action.
    if selected_action == "list":
        # Attempt to retrieve the list of Action entities.
        try:
            # Call the ActionManager list method with optional filters.
            entity_result = action_manager.list_actions(
    # Assign a value to the variable for subsequent use.
                strack_id=parsed_arguments.strack_id,
    # Assign a value to the variable for subsequent use.
                item_status=parsed_arguments.entity_status,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 列表查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the list operation failed.
            return 1
        # Print the list of Action entities as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful listing.
        return 0
    # Dispatch to the show handler for the Action show action.
    if selected_action == "show":
        # Attempt to retrieve the single Action by its identifier.
        try:
            # Call the ActionManager retrieve method with the Action identifier.
            entity_result = action_manager.retrieve_action(
    # Execute the following code statement.
                parsed_arguments.action_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Verify that the Action entity exists in the database before proceeding.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Action 未找到: "
    # Assign a value to the variable for subsequent use.
            message_error += parsed_arguments.action_id
            # Print the error message to standard output.
            print(message_error)
            # Return exit code 1 to indicate the entity was not found.
            return 1
        # Print the Action details as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful retrieval.
        return 0
    # Dispatch to the update handler for the Action update action.
    if selected_action == "update":
        # Attempt to update the Action status with the provided value.
        try:
            # Call the ActionManager modify method with the new status.
            entity_result = action_manager.modify_action_fields(
    # Execute the following code statement.
                parsed_arguments.action_id,
    # Assign a value to the variable for subsequent use.
                Status=parsed_arguments.entity_status,
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Action 更新参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 更新时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
        # Print the updated Action entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful update.
        return 0
    # Dispatch to the delete handler for the Action delete action.
    if selected_action == "delete":
        # Attempt to delete the Action by its identifier.
        try:
            # Call the ActionManager erase method with the Action identifier.
            is_deleted = action_manager.erase_action_record(
    # Execute the following code statement.
                parsed_arguments.action_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 删除时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the delete operation failed.
            return 1
        # Verify that the deletion was successful.
        if is_deleted:
            # Print the success confirmation message in Chinese.
            print(f"[OK] Action 已删除: {parsed_arguments.action_id}")
            # Return exit code 0 to indicate successful deletion.
            return 0
        # Prepare the Chinese error message for entity not found during deletion.
        message_error = "[X] Action 未找到，无法删除: "
    # Assign a value to the variable for subsequent use.
        message_error += parsed_arguments.action_id
        # Print the error message to standard output.
        print(message_error)
        # Return exit code 1 to indicate the entity was not found.
        return 1
    # Print the unrecognized action error and return failure exit code.
    print(f"[X] Action 未知操作: {selected_action}")
    # Return exit code 1 for unrecognized Action actions.
    return 1


def _init_main_handle_note_(database_path, selected_action, parsed_arguments):
    """
    Dispatch the selected Note action to the appropriate handler.

    Routes create, list, show, update, and delete actions to their
    respective NoteManager method calls and formats the output.

    :param database_path: The resolved path to the database file.
    :type database_path: str
    :param selected_action: The action subcommand (create, list, show, update, delete).
    :type selected_action: str
    :param parsed_arguments: The parsed command-line argument namespace.
    :type parsed_arguments: argparse.Namespace
    :return: Exit code 0 for success, 1 for failure.
    :rtype: int
    """
    # Instantiate the DatabaseManager for the resolved database path.
    database_manager = DatabaseManager(database_path)
    # Create the NoteManager instance bound to the database connection.
    note_manager = NoteManager(database_manager)
    # Dispatch to the create handler for the Note create action.
    if selected_action == "create":
        # Attempt to create a new Note with the provided parameters.
        try:
            # Call the NoteManager insert method with parsed arguments.
            entity_result = note_manager.insert_note_record(
    # Execute the following code statement.
                parsed_arguments.strack_id,
    # Execute the following code statement.
                parsed_arguments.note_id,
    # Execute the following code statement.
                parsed_arguments.entity_title,
    # Assign a value to the variable for subsequent use.
                note_content=parsed_arguments.note_content or "",
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Note 创建参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 创建时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        # Print the created Note entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful creation.
        return 0
    # Dispatch to the list handler for the Note list action.
    if selected_action == "list":
        # Attempt to retrieve the list of Note entities.
        try:
            # Call the NoteManager list method with optional Strack filter.
            entity_result = note_manager.list_notes(
    # Assign a value to the variable for subsequent use.
                strack_id=parsed_arguments.strack_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 列表查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the list operation failed.
            return 1
        # Print the list of Note entities as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful listing.
        return 0
    # Dispatch to the show handler for the Note show action.
    if selected_action == "show":
        # Attempt to retrieve the single Note by its identifier.
        try:
            # Call the NoteManager retrieve method with the Note identifier.
            entity_result = note_manager.retrieve_note(
    # Execute the following code statement.
                parsed_arguments.note_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 查询时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Verify that the Note entity exists in the database before proceeding.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Note 未找到: "
    # Assign a value to the variable for subsequent use.
            message_error += parsed_arguments.note_id
            # Print the error message to standard output.
            print(message_error)
            # Return exit code 1 to indicate the entity was not found.
            return 1
        # Print the Note details as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful retrieval.
        return 0
    # Dispatch to the update handler for the Note update action.
    if selected_action == "update":
        # Attempt to update the Note with the provided title or content.
        try:
            # Call the NoteManager modify method with optional new values.
            entity_result = note_manager.modify_note_fields(
    # Execute the following code statement.
                parsed_arguments.note_id,
    # Assign a value to the variable for subsequent use.
                Title=parsed_arguments.entity_title,
    # Assign a value to the variable for subsequent use.
                Content=parsed_arguments.note_content,
            )
    # Catch and process the named exception type.
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Note 更新参数无效: "
    # Assign a value to the variable for subsequent use.
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 更新时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
        # Print the updated Note entity as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful update.
        return 0
    # Dispatch to the delete handler for the Note delete action.
    if selected_action == "delete":
        # Attempt to delete the Note by its identifier.
        try:
            # Call the NoteManager erase method with the Note identifier.
            is_deleted = note_manager.erase_note_record(
    # Execute the following code statement.
                parsed_arguments.note_id,
            )
    # Catch and process the named exception type.
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 删除时发生未知错误: "
    # Assign a value to the variable for subsequent use.
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the delete operation failed.
            return 1
        # Verify that the deletion was successful.
        if is_deleted:
            # Print the success confirmation message in Chinese.
            print(f"[OK] Note 已删除: {parsed_arguments.note_id}")
            # Return exit code 0 to indicate successful deletion.
            return 0
        # Prepare the Chinese error message for entity not found during deletion.
        message_error = "[X] Note 未找到，无法删除: "
    # Assign a value to the variable for subsequent use.
        message_error += parsed_arguments.note_id
        # Print the error message to standard output.
        print(message_error)
        # Return exit code 1 to indicate the entity was not found.
        return 1
    # Print the unrecognized action error and return failure exit code.
    print(f"[X] Note 未知操作: {selected_action}")
    # Return exit code 1 for unrecognized Note actions.
    return 1


# Guard the main function execution for direct script invocation.
if __name__ == "__main__":
    # Invoke main and propagate the returned exit code to the operating system.
    sys.exit(main())
