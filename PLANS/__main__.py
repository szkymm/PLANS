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
    plans --db /path/to/plans.db init
    plans --db /path/to/plans.db strack create ID TITLE [--description DESC] [--priority N]
    plans --db /path/to/plans.db strack list [--status STATUS]
    plans strack show ID
    plans strack delete ID
    plans plan create STRACK_ID PLAN_ID TITLE [--description DESC] [--priority N]
    plans plan list [STRACK_ID] [--status STATUS]
    plans plan show PLAN_ID
    plans plan update PLAN_ID --status STATUS
    plans plan delete PLAN_ID
    plans issue create STRACK_ID ISSUE_ID TITLE [--description DESC] [--severity SEV]
    plans issue list [STRACK_ID] [--status STATUS] [--severity SEV]
    plans issue show ISSUE_ID
    plans issue update ISSUE_ID --status STATUS
    plans issue delete ISSUE_ID
    plans action create STRACK_ID ACTION_ID TITLE [--description DESC]
    plans action list [STRACK_ID] [--status STATUS]
    plans action show ACTION_ID
    plans action update ACTION_ID --status STATUS
    plans action delete ACTION_ID
    plans note create STRACK_ID NOTE_ID TITLE [--content CONTENT]
    plans note list [STRACK_ID]
    plans note show NOTE_ID
    plans note update NOTE_ID [--title TITLE] [--content CONTENT]
    plans note delete NOTE_ID

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
__version__ = "0.1.0"

# Define the default database file path for the local SQLite database.
default_database_path = "plans.db"
# Define the environment variable name for custom database path override.
environment_database_path = "COMMON_PLANS_DB"


def _init_build_parser_function_():
    """
    Construct and return the complete argument parser for the PLANS CLI.

    Builds a nested argparse structure with top-level subcommands for each
    entity type (init, strack, plan, issue, action, note) and second-level
    subcommands for CRUD actions (create, list, show, update, delete).

    :return: The fully configured top-level ArgumentParser instance.
    :rtype: argparse.ArgumentParser
    """
    # Create the top-level argument parser with the program description.
    argument_parser = argparse.ArgumentParser(
        prog="plans",
        description="PLANS -- Priority Logs Actions Notes Stracks: "
        + "Local-first project management stack system.",
    )
    # Add a global option to specify the database file path for all subcommands.
    argument_parser.add_argument(
        "--db",
        dest="database_path",
        default=None,
        help="Path to the SQLite database file (default: ./plans.db or $COMMON_PLANS_DB).",
    )
    # Display the package version when the version flag is used.
    argument_parser.add_argument(
        "--version",
        action="version",
        version=f"PLANS {__version__}",
    )
    # Create the subparsers container for entity-level commands.
    argument_subparsers = argument_parser.add_subparsers(
        title="commands",
        dest="selected_command",
    )
    # --- init subcommand ---
    # Create the parser for the init database initialization command.
    init_subparser = argument_subparsers.add_parser(
        "init",
        help="Initialize the PLANS database schema.",
    )
    # --- strack entity subcommands ---
    _init_build_parser_function_strack_(argument_subparsers)
    # --- plan entity subcommands ---
    _init_build_parser_function_plan_(argument_subparsers)
    # --- issue entity subcommands ---
    _init_build_parser_function_issue_(argument_subparsers)
    # --- action entity subcommands ---
    _init_build_parser_function_action_(argument_subparsers)
    # --- note entity subcommands ---
    _init_build_parser_function_note_(argument_subparsers)
    # Return the fully constructed argument parser for dispatch in main.
    return argument_parser


def _init_build_parser_function_strack_(argument_subparsers):
    """
    Add the Strack entity subcommand group to the argument subparsers.

    Registers create, list, show, and delete subcommands for the Strack
    entity type under the top-level 'strack' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Strack entity operations.
    entity_subparser = argument_subparsers.add_parser(
        "strack",
        help="Manage Strack entities (create, list, show, delete).",
    )
    # Create the sub-subparsers container for Strack action commands.
    action_subparsers = entity_subparser.add_subparsers(
        title="strack_actions",
        dest="selected_action",
    )
    # --- strack create ---
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
        "create",
        help="Create a new Strack.",
    )
    # Add the positional argument for the Strack identifier.
    create_parser.add_argument(
        "strack_id",
        help="Unique identifier for the Strack.",
    )
    # Add the positional argument for the Strack title.
    create_parser.add_argument(
        "entity_title",
        help="Title of the Strack.",
    )
    # Add the optional description flag for the Strack.
    create_parser.add_argument(
        "--description",
        dest="entity_description",
        default=None,
        help="Optional description of the Strack.",
    )
    # Add the optional priority flag for the Strack.
    create_parser.add_argument(
        "--priority",
        dest="task_priority",
        type=int,
        default=None,
        help="Optional priority level (integer).",
    )
    # --- strack list ---
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
        "list",
        help="List all Stracks.",
    )
    # Add the optional status filter flag for listing.
    list_parser.add_argument(
        "--status",
        dest="entity_status",
        default=None,
        help="Filter Stracks by status.",
    )
    # --- strack show ---
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
        "show",
        help="Show details of a Strack.",
    )
    # Add the positional argument for the Strack identifier to display.
    show_parser.add_argument(
        "strack_id",
        help="Identifier of the Strack to display.",
    )
    # --- strack delete ---
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
        "delete",
        help="Delete a Strack.",
    )
    # Add the positional argument for the Strack identifier to delete.
    delete_parser.add_argument(
        "strack_id",
        help="Identifier of the Strack to delete.",
    )


def _init_build_parser_function_plan_(argument_subparsers):
    """
    Add the Plan entity subcommand group to the argument subparsers.

    Registers create, list, show, update, and delete subcommands for the
    Plan entity type under the top-level 'plan' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Plan entity operations.
    entity_subparser = argument_subparsers.add_parser(
        "plan",
        help="Manage Plan entities (create, list, show, update, delete).",
    )
    # Create the sub-subparsers container for Plan action commands.
    action_subparsers = entity_subparser.add_subparsers(
        title="plan_actions",
        dest="selected_action",
    )
    # --- plan create ---
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
        "create",
        help="Create a new Plan under a Strack.",
    )
    # Add the positional argument for the parent Strack identifier.
    create_parser.add_argument(
        "strack_id",
        help="Identifier of the parent Strack.",
    )
    # Add the positional argument for the Plan identifier.
    create_parser.add_argument(
        "plan_id",
        help="Unique identifier for the Plan.",
    )
    # Add the positional argument for the Plan title.
    create_parser.add_argument(
        "entity_title",
        help="Title of the Plan.",
    )
    # Add the optional description flag for the Plan.
    create_parser.add_argument(
        "--description",
        dest="entity_description",
        default=None,
        help="Optional description of the Plan.",
    )
    # Add the optional priority flag for the Plan.
    create_parser.add_argument(
        "--priority",
        dest="task_priority",
        type=int,
        default=None,
        help="Optional priority level (integer).",
    )
    # --- plan list ---
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
        "list",
        help="List Plans, optionally filtered by Strack.",
    )
    # Add the optional positional argument for filtering by parent Strack.
    list_parser.add_argument(
        "strack_id",
        nargs="?",
        default=None,
        help="Optional parent Strack identifier to filter by.",
    )
    # Add the optional status filter flag for listing.
    list_parser.add_argument(
        "--status",
        dest="entity_status",
        default=None,
        help="Filter Plans by status.",
    )
    # --- plan show ---
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
        "show",
        help="Show details of a Plan.",
    )
    # Add the positional argument for the Plan identifier to display.
    show_parser.add_argument(
        "plan_id",
        help="Identifier of the Plan to display.",
    )
    # --- plan update ---
    # Create the subparser for the update action.
    update_parser = action_subparsers.add_parser(
        "update",
        help="Update the status of a Plan.",
    )
    # Add the positional argument for the Plan identifier to update.
    update_parser.add_argument(
        "plan_id",
        help="Identifier of the Plan to update.",
    )
    # Add the required status flag to set the new Plan status.
    update_parser.add_argument(
        "--status",
        dest="entity_status",
        required=True,
        help="New status value for the Plan.",
    )
    # --- plan delete ---
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
        "delete",
        help="Delete a Plan.",
    )
    # Add the positional argument for the Plan identifier to delete.
    delete_parser.add_argument(
        "plan_id",
        help="Identifier of the Plan to delete.",
    )


def _init_build_parser_function_issue_(argument_subparsers):
    """
    Add the Issue entity subcommand group to the argument subparsers.

    Registers create, list, show, update, and delete subcommands for the
    Issue entity type under the top-level 'issue' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Issue entity operations.
    entity_subparser = argument_subparsers.add_parser(
        "issue",
        help="Manage Issue entities (create, list, show, update, delete).",
    )
    # Create the sub-subparsers container for Issue action commands.
    action_subparsers = entity_subparser.add_subparsers(
        title="issue_actions",
        dest="selected_action",
    )
    # --- issue create ---
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
        "create",
        help="Create a new Issue under a Strack.",
    )
    # Add the positional argument for the parent Strack identifier.
    create_parser.add_argument(
        "strack_id",
        help="Identifier of the parent Strack.",
    )
    # Add the positional argument for the Issue identifier.
    create_parser.add_argument(
        "issue_id",
        help="Unique identifier for the Issue.",
    )
    # Add the positional argument for the Issue title.
    create_parser.add_argument(
        "entity_title",
        help="Title of the Issue.",
    )
    # Add the optional description flag for the Issue.
    create_parser.add_argument(
        "--description",
        dest="entity_description",
        default=None,
        help="Optional description of the Issue.",
    )
    # Add the optional severity flag for the Issue.
    create_parser.add_argument(
        "--severity",
        dest="issue_severity",
        default=None,
        help="Optional severity level (e.g., low, medium, high, critical).",
    )
    # --- issue list ---
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
        "list",
        help="List Issues, optionally filtered by Strack.",
    )
    # Add the optional positional argument for filtering by parent Strack.
    list_parser.add_argument(
        "strack_id",
        nargs="?",
        default=None,
        help="Optional parent Strack identifier to filter by.",
    )
    # Add the optional status filter flag for listing.
    list_parser.add_argument(
        "--status",
        dest="entity_status",
        default=None,
        help="Filter Issues by status.",
    )
    # Add the optional severity filter flag for listing.
    list_parser.add_argument(
        "--severity",
        dest="issue_severity",
        default=None,
        help="Filter Issues by severity.",
    )
    # --- issue show ---
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
        "show",
        help="Show details of an Issue.",
    )
    # Add the positional argument for the Issue identifier to display.
    show_parser.add_argument(
        "issue_id",
        help="Identifier of the Issue to display.",
    )
    # --- issue update ---
    # Create the subparser for the update action.
    update_parser = action_subparsers.add_parser(
        "update",
        help="Update the status of an Issue.",
    )
    # Add the positional argument for the Issue identifier to update.
    update_parser.add_argument(
        "issue_id",
        help="Identifier of the Issue to update.",
    )
    # Add the required status flag to set the new Issue status.
    update_parser.add_argument(
        "--status",
        dest="entity_status",
        required=True,
        help="New status value for the Issue.",
    )
    # --- issue delete ---
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
        "delete",
        help="Delete an Issue.",
    )
    # Add the positional argument for the Issue identifier to delete.
    delete_parser.add_argument(
        "issue_id",
        help="Identifier of the Issue to delete.",
    )


def _init_build_parser_function_action_(argument_subparsers):
    """
    Add the Action entity subcommand group to the argument subparsers.

    Registers create, list, show, update, and delete subcommands for the
    Action entity type under the top-level 'action' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Action entity operations.
    entity_subparser = argument_subparsers.add_parser(
        "action",
        help="Manage Action entities (create, list, show, update, delete).",
    )
    # Create the sub-subparsers container for Action action commands.
    action_subparsers = entity_subparser.add_subparsers(
        title="action_actions",
        dest="selected_action",
    )
    # --- action create ---
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
        "create",
        help="Create a new Action under a Strack.",
    )
    # Add the positional argument for the parent Strack identifier.
    create_parser.add_argument(
        "strack_id",
        help="Identifier of the parent Strack.",
    )
    # Add the positional argument for the Action identifier.
    create_parser.add_argument(
        "action_id",
        help="Unique identifier for the Action.",
    )
    # Add the positional argument for the Action title.
    create_parser.add_argument(
        "entity_title",
        help="Title of the Action.",
    )
    # Add the optional description flag for the Action.
    create_parser.add_argument(
        "--description",
        dest="entity_description",
        default=None,
        help="Optional description of the Action.",
    )
    # --- action list ---
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
        "list",
        help="List Actions, optionally filtered by Strack.",
    )
    # Add the optional positional argument for filtering by parent Strack.
    list_parser.add_argument(
        "strack_id",
        nargs="?",
        default=None,
        help="Optional parent Strack identifier to filter by.",
    )
    # Add the optional status filter flag for listing.
    list_parser.add_argument(
        "--status",
        dest="entity_status",
        default=None,
        help="Filter Actions by status.",
    )
    # --- action show ---
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
        "show",
        help="Show details of an Action.",
    )
    # Add the positional argument for the Action identifier to display.
    show_parser.add_argument(
        "action_id",
        help="Identifier of the Action to display.",
    )
    # --- action update ---
    # Create the subparser for the update action.
    update_parser = action_subparsers.add_parser(
        "update",
        help="Update the status of an Action.",
    )
    # Add the positional argument for the Action identifier to update.
    update_parser.add_argument(
        "action_id",
        help="Identifier of the Action to update.",
    )
    # Add the required status flag to set the new Action status.
    update_parser.add_argument(
        "--status",
        dest="entity_status",
        required=True,
        help="New status value for the Action.",
    )
    # --- action delete ---
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
        "delete",
        help="Delete an Action.",
    )
    # Add the positional argument for the Action identifier to delete.
    delete_parser.add_argument(
        "action_id",
        help="Identifier of the Action to delete.",
    )


def _init_build_parser_function_note_(argument_subparsers):
    """
    Add the Note entity subcommand group to the argument subparsers.

    Registers create, list, show, update, and delete subcommands for the
    Note entity type under the top-level 'note' command.

    :param argument_subparsers: The top-level subparser action object.
    :type argument_subparsers: argparse._SubParsersAction
    """
    # Create the subparser for all Note entity operations.
    entity_subparser = argument_subparsers.add_parser(
        "note",
        help="Manage Note entities (create, list, show, update, delete).",
    )
    # Create the sub-subparsers container for Note action commands.
    action_subparsers = entity_subparser.add_subparsers(
        title="note_actions",
        dest="selected_action",
    )
    # --- note create ---
    # Create the subparser for the create action.
    create_parser = action_subparsers.add_parser(
        "create",
        help="Create a new Note under a Strack.",
    )
    # Add the positional argument for the parent Strack identifier.
    create_parser.add_argument(
        "strack_id",
        help="Identifier of the parent Strack.",
    )
    # Add the positional argument for the Note identifier.
    create_parser.add_argument(
        "note_id",
        help="Unique identifier for the Note.",
    )
    # Add the positional argument for the Note title.
    create_parser.add_argument(
        "entity_title",
        help="Title of the Note.",
    )
    # Add the optional content flag for the Note body text.
    create_parser.add_argument(
        "--content",
        dest="note_content",
        default=None,
        help="Optional content body of the Note.",
    )
    # --- note list ---
    # Create the subparser for the list action.
    list_parser = action_subparsers.add_parser(
        "list",
        help="List Notes, optionally filtered by Strack.",
    )
    # Add the optional positional argument for filtering by parent Strack.
    list_parser.add_argument(
        "strack_id",
        nargs="?",
        default=None,
        help="Optional parent Strack identifier to filter by.",
    )
    # --- note show ---
    # Create the subparser for the show action.
    show_parser = action_subparsers.add_parser(
        "show",
        help="Show details of a Note.",
    )
    # Add the positional argument for the Note identifier to display.
    show_parser.add_argument(
        "note_id",
        help="Identifier of the Note to display.",
    )
    # --- note update ---
    # Create the subparser for the update action.
    update_parser = action_subparsers.add_parser(
        "update",
        help="Update the title or content of a Note.",
    )
    # Add the positional argument for the Note identifier to update.
    update_parser.add_argument(
        "note_id",
        help="Identifier of the Note to update.",
    )
    # Add the optional title flag to update the Note title.
    update_parser.add_argument(
        "--title",
        dest="entity_title",
        default=None,
        help="New title for the Note.",
    )
    # Add the optional content flag to update the Note body text.
    update_parser.add_argument(
        "--content",
        dest="note_content",
        default=None,
        help="New content body for the Note.",
    )
    # --- note delete ---
    # Create the subparser for the delete action.
    delete_parser = action_subparsers.add_parser(
        "delete",
        help="Delete a Note.",
    )
    # Add the positional argument for the Note identifier to delete.
    delete_parser.add_argument(
        "note_id",
        help="Identifier of the Note to delete.",
    )


def main(arguments_list=None):
    """
    Execute the PLANS command-line interface entry point.

    Parses command-line arguments, initializes the database for the init
    command, and dispatches entity CRUD operations to the appropriate
    manager classes. Prints results as formatted JSON output and returns
    exit code 0 on success or 1 on error.

    :param arguments_list: Optional pre-parsed argument list for testing.
    :type arguments_list: Optional[Sequence[str]]
    :return: Exit code 0 for success, 1 for failure.
    :rtype: int
    """
    # Reconfigure standard output to use UTF-8 encoding for cross-platform support.
    sys.stdout.reconfigure(encoding="utf-8")
    # Build the full argument parser structure via the private builder.
    argument_parser = _init_build_parser_function_()
    # Parse the command-line arguments into a namespace object.
    if arguments_list is None:
        # Use sys.argv[1:] when no explicit argument list is provided.
        parsed_arguments = argument_parser.parse_args()
    else:
        # Use the supplied argument list for programmatic invocation.
        parsed_arguments = argument_parser.parse_args(arguments_list)
    # Retrieve the selected top-level command from the parsed namespace.
    selected_command = getattr(parsed_arguments, "selected_command", None)
    # Resolve the database file path from arguments, env variable, or default.
    database_path = getattr(parsed_arguments, "database_path", None)
    # Fall back to the environment variable when no path was provided.
    if database_path is None:
        # Attempt to read the database path from the environment variable.
        database_path = os.environ.get(
            environment_database_path,
            default_database_path,
        )
    # Handle the case where no recognized command was provided.
    if selected_command is None:
        # Print the help text and exit cleanly when no command is given.
        argument_parser.print_help()
        # Return exit code 0 since displaying help is not an error.
        return 0
    # Dispatch to the init handler for database initialization.
    if selected_command == "init":
        # Delegate to the init handler with the resolved database path.
        return _init_main_handle_init_(database_path)
    # For all entity commands, ensure the database file exists first.
    if not os.path.isfile(database_path):
        # Prepare the Chinese error message for missing database file.
        message_error = "[X] 数据库文件不存在，请先运行 'plans init' 初始化数据库: "
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
            database_path,
            selected_action,
            parsed_arguments,
        )
    if selected_command == "plan":
        # Delegate to the Plan entity handler for the selected action.
        return _init_main_handle_plan_(
            database_path,
            selected_action,
            parsed_arguments,
        )
    if selected_command == "issue":
        # Delegate to the Issue entity handler for the selected action.
        return _init_main_handle_issue_(
            database_path,
            selected_action,
            parsed_arguments,
        )
    if selected_command == "action":
        # Delegate to the Action entity handler for the selected action.
        return _init_main_handle_action_(
            database_path,
            selected_action,
            parsed_arguments,
        )
    if selected_command == "note":
        # Delegate to the Note entity handler for the selected action.
        return _init_main_handle_note_(
            database_path,
            selected_action,
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
    except FileNotFoundError as filenotfound_error:
        # Build the Chinese error message for path-related failures.
        message_error = "[X] (FileNotFoundError) 数据库路径无效或无法访问: "
        message_error += str(filenotfound_error)
        # Print the error message for the user to diagnose.
        print(message_error)
        # Return exit code 1 to indicate initialization failure.
        return 1
    except PermissionError as permission_error:
        # Build the Chinese error message for permission-denied failures.
        message_error = "[X] (PermissionError) 无权限创建或写入数据库文件: "
        message_error += str(permission_error)
        # Print the error message for the user to diagnose.
        print(message_error)
        # Return exit code 1 to indicate initialization failure.
        return 1
    except Exception as exception_error:
        # Build the Chinese error message for any unanticipated failures.
        message_error = "[X] (OtherError) 数据库初始化时发生未知错误: "
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

    Routes create, list, show, and delete actions to their respective
    StrackManager method calls and formats the output.

    :param database_path: The resolved path to the database file.
    :type database_path: str
    :param selected_action: The action subcommand (create, list, show, delete).
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
            # Call the StrackManager create method with parsed arguments.
            entity_result = strack_manager.create_strack(
                parsed_arguments.strack_id,
                parsed_arguments.entity_title,
                description=parsed_arguments.entity_description or "",
                priority=parsed_arguments.task_priority or 3,
            )
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Strack 创建参数无效: "
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Strack 创建时发生未知错误: "
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
                status=parsed_arguments.entity_status,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Strack 列表查询时发生未知错误: "
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
            # Call the StrackManager show method with the Strack identifier.
            entity_result = strack_manager.get_strack(
                parsed_arguments.strack_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Strack 查询时发生未知错误: "
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Check if the Strack entity was found in the database.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Strack 未找到: "
            message_error += parsed_arguments.strack_id
            # Print the error message to standard output.
            print(message_error)
            # Return exit code 1 to indicate the entity was not found.
            return 1
        # Print the Strack details as formatted JSON output.
        print(json.dumps(entity_result, indent=4, ensure_ascii=False))
        # Return exit code 0 to indicate successful retrieval.
        return 0
    # Dispatch to the delete handler for the Strack delete action.
    if selected_action == "delete":
        # Attempt to delete the Strack by its identifier.
        try:
            # Call the StrackManager delete method with the Strack identifier.
            is_deleted = strack_manager.delete_strack(
                parsed_arguments.strack_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Strack 删除时发生未知错误: "
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
            # Call the PlanManager create method with parsed arguments.
            entity_result = plan_manager.create_plan(
                parsed_arguments.strack_id,
                parsed_arguments.plan_id,
                parsed_arguments.entity_title,
                plan_description=parsed_arguments.entity_description or "",
                priority_level=parsed_arguments.task_priority or 3,
            )
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Plan 创建参数无效: "
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 创建时发生未知错误: "
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
                strack_id=parsed_arguments.strack_id,
                status_value=parsed_arguments.entity_status,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 列表查询时发生未知错误: "
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
            # Call the PlanManager show method with the Plan identifier.
            entity_result = plan_manager.get_plan(
                parsed_arguments.plan_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 查询时发生未知错误: "
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Check if the Plan entity was found in the database.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Plan 未找到: "
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
            # Call the PlanManager update method with the new status.
            entity_result = plan_manager.update_plan(
                parsed_arguments.plan_id,
                Status=parsed_arguments.entity_status,
            )
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Plan 更新参数无效: "
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 更新时发生未知错误: "
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
            # Call the PlanManager delete method with the Plan identifier.
            is_deleted = plan_manager.delete_plan(
                parsed_arguments.plan_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Plan 删除时发生未知错误: "
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
            # Call the IssueManager create method with parsed arguments.
            entity_result = issue_manager.create_issue(
                parsed_arguments.strack_id,
                parsed_arguments.issue_id,
                parsed_arguments.entity_title,
                description=parsed_arguments.entity_description or "",
                severity=parsed_arguments.issue_severity or "medium",
            )
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Issue 创建参数无效: "
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 创建时发生未知错误: "
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
                strack_id=parsed_arguments.strack_id,
                status=parsed_arguments.entity_status,
                severity=parsed_arguments.issue_severity,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 列表查询时发生未知错误: "
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
            # Call the IssueManager show method with the Issue identifier.
            entity_result = issue_manager.get_issue(
                parsed_arguments.issue_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 查询时发生未知错误: "
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Check if the Issue entity was found in the database.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Issue 未找到: "
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
            # Call the IssueManager update method with the new status.
            entity_result = issue_manager.update_issue(
                parsed_arguments.issue_id,
                Status=parsed_arguments.entity_status,
            )
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Issue 更新参数无效: "
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 更新时发生未知错误: "
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
            # Call the IssueManager delete method with the Issue identifier.
            is_deleted = issue_manager.delete_issue(
                parsed_arguments.issue_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Issue 删除时发生未知错误: "
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
            # Call the ActionManager create method with parsed arguments.
            entity_result = action_manager.create_action(
                parsed_arguments.strack_id,
                parsed_arguments.action_id,
                parsed_arguments.entity_title,
                description=parsed_arguments.entity_description or "",
            )
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Action 创建参数无效: "
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 创建时发生未知错误: "
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
                strack_id=parsed_arguments.strack_id,
                status=parsed_arguments.entity_status,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 列表查询时发生未知错误: "
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
            # Call the ActionManager show method with the Action identifier.
            entity_result = action_manager.get_action(
                parsed_arguments.action_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 查询时发生未知错误: "
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Check if the Action entity was found in the database.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Action 未找到: "
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
            # Call the ActionManager update method with the new status.
            entity_result = action_manager.update_action(
                parsed_arguments.action_id,
                Status=parsed_arguments.entity_status,
            )
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Action 更新参数无效: "
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 更新时发生未知错误: "
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
            # Call the ActionManager delete method with the Action identifier.
            is_deleted = action_manager.delete_action(
                parsed_arguments.action_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Action 删除时发生未知错误: "
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
            # Call the NoteManager create method with parsed arguments.
            entity_result = note_manager.create_note(
                parsed_arguments.strack_id,
                parsed_arguments.note_id,
                parsed_arguments.entity_title,
                note_content=parsed_arguments.note_content or "",
            )
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Note 创建参数无效: "
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the create operation failed.
            return 1
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 创建时发生未知错误: "
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
                strack_id=parsed_arguments.strack_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 列表查询时发生未知错误: "
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
            # Call the NoteManager show method with the Note identifier.
            entity_result = note_manager.get_note(
                parsed_arguments.note_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 查询时发生未知错误: "
            message_error += str(exception_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the show operation failed.
            return 1
        # Check if the Note entity was found in the database.
        if entity_result is None:
            # Prepare the Chinese error message for entity not found.
            message_error = "[X] Note 未找到: "
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
            # Call the NoteManager update method with optional new values.
            entity_result = note_manager.update_note(
                parsed_arguments.note_id,
                Title=parsed_arguments.entity_title,
                Content=parsed_arguments.note_content,
            )
        except ValueError as value_error:
            # Build the Chinese error message for invalid parameter values.
            message_error = "[X] (ValueError) Note 更新参数无效: "
            message_error += str(value_error)
            # Print the error message for the user to diagnose.
            print(message_error)
            # Return exit code 1 to indicate the update operation failed.
            return 1
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 更新时发生未知错误: "
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
            # Call the NoteManager delete method with the Note identifier.
            is_deleted = note_manager.delete_note(
                parsed_arguments.note_id,
            )
        except Exception as exception_error:
            # Build the Chinese error message for unanticipated failures.
            message_error = "[X] (OtherError) Note 删除时发生未知错误: "
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
