# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================

MODULE               : PLANS.action

TYPE                 : Python Script

DESCRIPTION          :
    Action entity manager for the PLANS local-first project management
    system. Provides CRUD operations for Action items belonging to
    Strack containers, with status tracking through pending,
    in_progress, done, and cancelled states.

AUTHOR               : Suzuki Yumemi

CONTACT              : szkymm@gmail.com

MAINTAINER           :
    Suzuki Yumemi (szkymm@gmail.com)
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
    from PLANS import DatabaseManager, ActionManager

    database = DatabaseManager("plans.db")
    database.initialize_schema()
    action_manager = ActionManager(database)
    action = action_manager.insert_action_record(
        strack_id="project-alpha",
        action_id="task-001",
        item_title="Implement login screen",
        item_description="Build the React component for user login.",
    )
    action_manager.modify_action_fields("task-001", Status="in_progress")
    all_open = action_manager.list_actions(
        strack_id="project-alpha",
        status="pending",
    )

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

# Import the datetime module for UTC timestamp generation.
from datetime import datetime, timezone
# Import type hinting utilities for method signatures.
from typing import Optional, List, Dict, Any
# Import the DatabaseManager for SQLite database operations.
from .database import DatabaseManager

# Define the package version string to match PROJECT VERSION in docstring.
__version__ = "0.1.2"


class ActionManager:
    """
    ActionManager CLASS IS CORE PART OF PLANS ACTION.PY.

    PLANS.action.ActionManager:
        Manages Action entities within the PLANS project management
        system. An Action represents a single actionable task item
        belonging to a Strack container, with full lifecycle tracking
        through pending, in_progress, done, and cancelled statuses.

    ATTRIBUTES                         :
        database_manager (DatabaseManager): The injected database
            connection manager for SQLite persistence operations.

    PUBLIC METHODS                     :
        insert_action_record(strack_id, action_id, item_title, item_description) -> dict:
            Insert a new Action row into the database and return it.
        retrieve_action(action_id) -> Optional[dict]:
            Retrieve a single Action by its primary key identifier.
        list_actions(strack_id, item_status) -> list:
            Query Actions with optional Strack and status filters.
        modify_action_fields(action_id, **keyword_arguments) -> dict:
            Modify Title, Description, or Status fields of an Action.
        erase_action_record(action_id) -> bool:
            Erase an Action row from the database permanently.

    PRIVATE METHODS                    :
        _init_form_timestamp_function_() -> str:
            Produce a UTC ISO 8601 timestamp string for database fields.

    USAGE                             :
        manager = ActionManager(database)
        action = manager.insert_action_record("strack-1", "act-1", "Fix bug")
        manager.modify_action_fields("act-1", Status="done")
        results = manager.list_actions(status="pending")

    WARNING                           :
        Private methods should not be called from outside the class.
    """

    def __init__(self, database_manager: DatabaseManager) -> None:
        """
        Initialize the ActionManager with a database connection.

        Stores the injected DatabaseManager reference and ensures the
        Actions table schema exists for subsequent CRUD operations.

        The parameters are as follows:

        :param database_manager: The DatabaseManager instance providing
            SQLite connectivity and query execution.
        :type database_manager: DatabaseManager
        """
        # Store the database manager reference for all SQL operations.
        self.database_manager = database_manager
        # Define the CREATE TABLE statement for the Actions entity.
        string_sql = "CREATE TABLE IF NOT EXISTS Actions ("
        # Append the Id primary key column definition to the schema DDL.
        string_sql += "Id TEXT PRIMARY KEY, "
        # Append the StrackId foreign key column definition to the schema DDL.
        string_sql += "StrackId TEXT NOT NULL, "
        # Append the Title column definition with NOT NULL constraint.
        string_sql += "Title TEXT NOT NULL, "
        # Append the Description column definition with empty string default.
        string_sql += "Description TEXT DEFAULT '', "
        # Append the Status column definition with pending default.
        string_sql += "Status TEXT DEFAULT 'pending', "
        # Append the CreatedAt timestamp column definition.
        string_sql += "CreatedAt TEXT NOT NULL, "
        # Append the UpdatedAt timestamp column definition.
        string_sql += "UpdatedAt TEXT NOT NULL"
        # Close the CREATE TABLE DDL statement with a closing parenthesis.
        string_sql += ")"
        # Execute the schema creation statement against the database.
        self.database_manager.run_sql_statement(string_sql)

    def insert_action_record(
        # Declare the typed parameters for inserting a new Action record.
        self, strack_id: str, action_id: str, item_title: str, item_description: str = ""
        # Annotate the return type as a dictionary representing the new Action.
    ) -> dict:
        """
        Create a new Action record in the database.

        Generates UTC timestamps for both CreatedAt and UpdatedAt
        fields, sets the initial status to pending, and persists
        the Action row via the DatabaseManager.

        The parameters are as follows:

        :param strack_id: The identifier of the parent Strack container.
        :type strack_id: str
        :param action_id: The unique primary key for this Action.
        :type action_id: str
        :param item_title: The human-readable title of the Action.
        :type item_title: str
        :param item_description: Optional longer description of the Action.
        :type item_description: str
        :return: The newly created Action as a dictionary.
        :rtype: dict
        :raise Exception: If the database insertion operation fails.
        """
        # Generate the current UTC timestamp for CreatedAt and UpdatedAt.
        timestamp_utc = self._init_form_timestamp_function_()
        # Build the column portion of the INSERT SQL for the Actions table.
        string_sql = "INSERT INTO Actions (Id, StrackId, Title, Description, "
        # Append the remaining columns with the closing parenthesis.
        string_sql += "Status, CreatedAt, UpdatedAt) "
        # Append the VALUES clause with positional parameter placeholders.
        string_sql += "VALUES (?, ?, ?, ?, ?, ?, ?)"
        # Assemble the parameter tuple for the INSERT statement.
        tuple_parameters = (
            # Provide the action identifier as the primary key value.
            action_id,
            # Provide the Strack identifier as the foreign key value.
            strack_id,
            # Provide the title text for the Action record.
            item_title,
            # Provide the optional description text for the Action record.
            item_description,
            # Provide the initial status string literal for a new Action.
            "pending",
            # Provide the UTC timestamp for the CreatedAt column.
            timestamp_utc,
            # Provide the UTC timestamp for the UpdatedAt column.
            timestamp_utc,
        )
        # Attempt to persist the new Action row into the database.
        try:
            # Execute the INSERT statement with all parameter values.
            self.database_manager.run_sql_statement(string_sql, tuple_parameters)
            # Commit the transaction to persist the new Action record.
            self.database_manager.connection.commit()
        # Handle any database error that occurs during the INSERT operation.
        except Exception as exception_error:
            # Build the error message describing the insertion failure in Chinese.
            message_error = f"[X] (OtherError) 创建Action失败，Action ID: {action_id}: {exception_error}"
            # Output the error message to the console for user visibility.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Return the newly created Action as a dictionary from the database.
        return self.retrieve_action(action_id)

    def retrieve_action(self, action_id: str) -> Optional[dict]:
        """
        Retrieve a single Action by its unique identifier.

        Queries the Actions table using the primary key and returns
        the matching row as a dictionary, or None if no match exists.

        The parameters are as follows:

        :param action_id: The unique identifier of the Action to retrieve.
        :type action_id: str
        :return: The Action as a dictionary with PascalCase keys, or None.
        :rtype: Optional[dict]
        :raise Exception: If the database query operation fails.
        """
        # Build the SELECT SQL statement for fetching a single Action.
        string_sql = "SELECT Id, StrackId, Title, Description, Status, CreatedAt, UpdatedAt "
        # Append the WHERE clause to target the specific Action by primary key.
        string_sql += "FROM Actions WHERE Id = ?"
        # Attempt to query the database for the specified Action.
        try:
            # Execute the SELECT statement with the action_id parameter.
                cursor_result = self.database_manager.run_sql_statement(string_sql, (action_id,))
        # Handle any database error that occurs during the SELECT operation.
        except Exception as exception_error:
            # Build the error message describing the query failure in Chinese.
            message_error = f"[X] (OtherError) 查询Action失败，Action ID: {action_id}: {exception_error}"
            # Output the error message to the console for user visibility.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Fetch the single result row from the executed query.
        tuple_row = cursor_result.fetchone()
        # Determine whether the query returned a matching Action record.
        if tuple_row is None:
            # Return None to indicate the Action does not exist.
            return None
        # Define the first portion of the ordered column list for the Actions table.
        list_columns = ["ID", "StrackID", "Title", "Description"]
        # Append the remaining column names to complete the ordered list.
        list_columns += ["Status", "CreatedAt", "UpdatedAt"]
        # Build a dictionary by zipping column names with row values.
        dict_action = dict(zip(list_columns, tuple_row))
        # Return the Action dictionary to the caller.
        return dict_action

    def list_actions(
        # Declare the typed parameters for filtering Action records.
        self, strack_id: Optional[str] = None, item_status: Optional[str] = None
        # Annotate the return type as a list of Action dictionaries.
    ) -> list:
        """
        List Actions with optional Strack and status filters.

        Builds a dynamic SELECT query that applies StrackId and Status
        WHERE clauses only when the corresponding arguments are provided.

        The parameters are as follows:

        :param strack_id: Optional parent Strack identifier to filter by.
        :type strack_id: Optional[str]
        :param item_status: Optional status value to filter by, one of
            pending, in_progress, done, or cancelled.
        :type item_status: Optional[str]
        :return: A list of Action dictionaries matching the filters.
        :rtype: list
        :raise Exception: If the database query operation fails.
        """
        # Start building the base SELECT SQL column list.
        string_sql = "SELECT Id, StrackId, Title, Description, "
        # Append the remaining columns and the FROM clause.
        string_sql += "Status, CreatedAt, UpdatedAt FROM Actions"
        # Initialize the list of WHERE clause fragments for filtering.
        list_conditions = []
        # Initialize the list of query parameter values.
        list_parameters = []
        # Apply the StrackId filter clause when a Strack identifier is supplied.
        if strack_id is not None:
            # Append the StrackId condition to the WHERE clause fragments.
            list_conditions.append("StrackId = ?")
            # Append the strack_id value to the parameter list.
            list_parameters.append(strack_id)
        # Apply the Status filter clause when a status value is supplied.
        if item_status is not None:
            # Append the Status condition to the WHERE clause fragments.
            list_conditions.append("Status = ?")
            # Append the item_status value to the parameter list.
            list_parameters.append(item_status)
        # Build the WHERE clause by joining all accumulated filter conditions.
        if list_conditions:
            # Join the conditions with AND and prepend the WHERE keyword.
            string_sql += " WHERE " + " AND ".join(list_conditions)
        # Append an ORDER BY clause for deterministic result ordering.
        string_sql += " ORDER BY CreatedAt ASC"
        # Convert the parameter list to a tuple for SQLite execution.
        tuple_parameters = tuple(list_parameters)
        # Attempt to execute the filtered SELECT query against the database.
        try:
            # Execute the SELECT statement with the assembled parameters.
            cursor_result = self.database_manager.run_sql_statement(string_sql, tuple_parameters)
        # Handle any database error that occurs during the filtered SELECT.
        except Exception as exception_error:
            # Build the error message describing the query failure in Chinese.
            message_error = f"[X] (OtherError) 查询Action列表失败: {exception_error}"
            # Output the error message to the console for user visibility.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Fetch all matching result rows from the executed query.
        list_records = cursor_result.fetchall()
        # Define the first portion of the ordered column list for the Actions table.
        list_columns = ["ID", "StrackID", "Title", "Description"]
        # Append the remaining column names to complete the ordered list.
        list_columns += ["Status", "CreatedAt", "UpdatedAt"]
        # Build a list of dictionaries by mapping each row to column names.
        list_results = [dict(zip(list_columns, tuple_row)) for tuple_row in list_records]
        # Return the list of Action dictionaries to the caller.
        return list_results

    def modify_action_fields(self, action_id: str, **keyword_arguments: Any) -> dict:
        """
        Update fields of an existing Action record.

        Accepts Title, Description, and Status as keyword arguments,
        updates only the provided fields, and refreshes the UpdatedAt
        timestamp automatically.

        The parameters are as follows:

        :param action_id: The unique identifier of the Action to update.
        :type action_id: str
        :param keyword_arguments: Keyword arguments mapping column names to new
            values. Supported keys are Title, Description, and Status.
        :type keyword_arguments: Any
        :return: The updated Action as a dictionary.
        :rtype: dict
        :raise ValueError: If no valid update fields are provided.
        :raise Exception: If the database update operation fails.
        """
        # Define the set of allowed column names for Action updates.
        set_allowed = {"Title", "Description", "Status"}
        # Initialize an empty dictionary for the filtered update fields.
        dict_updates = {}
        # Iterate over keyword arguments to collect allowed columns.
        for key, update_value in keyword_arguments.items():
            # Only include fields that are safe to update on this record.
            if key in set_allowed:
                # Store the allowed value in the updates dictionary.
                dict_updates[key] = update_value
        # Verify that at least one allowed field was specified for the update operation.
        if not dict_updates:
            # Build the error message in Chinese for missing update fields.
            message_error = "[X] (ValueError) 没有提供有效的更新字段，支持 Title, Description, Status"
            # Output the error message to the console for user visibility.
            print(message_error)
            # Raise the ValueError to signal invalid input to the caller.
            raise ValueError(message_error)
        # Generate the current UTC timestamp for the UpdatedAt column.
        timestamp_utc = self._init_form_timestamp_function_()
        # Inject the UpdatedAt timestamp into the update dictionary.
        dict_updates["UpdatedAt"] = timestamp_utc
        # Build the SET clause fragments from the update dictionary keys.
        clause_fragments = [f"{column_name} = ?" for column_name in dict_updates.keys()]
        # Join the SET clause fragments with commas.
        string_set = ", ".join(clause_fragments)
        # Build the full UPDATE SQL statement string.
        string_sql = "UPDATE Actions SET "
        # Append the assembled SET clause fragment to the base UPDATE statement.
        string_sql += string_set
        # Append the WHERE clause to target the specific Action by primary key.
        string_sql += " WHERE Id = ?"
        # Assemble the parameter tuple with update values followed by action_id.
        tuple_parameters = tuple(dict_updates.values()) + (action_id,)
        # Attempt to execute the UPDATE statement against the database.
        try:
            # Execute the UPDATE statement with the assembled parameters.
            cursor_result = self.database_manager.run_sql_statement(string_sql, tuple_parameters)
            # Commit the transaction to persist the updated Action record.
            self.database_manager.connection.commit()
        # Handle any database error that occurs during the UPDATE operation.
        except Exception as exception_error:
            # Build the error message describing the update failure in Chinese.
            message_error = f"[X] (OtherError) 更新Action失败，Action ID: {action_id}: {exception_error}"
            # Output the error message to the console for user visibility.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Return the updated Action as a dictionary from the database.
        return self.retrieve_action(action_id)

    def erase_action_record(self, action_id: str) -> bool:
        """
        Erase an Action record from the database permanently.

        Removes the Action row identified by the given primary key
        and returns a boolean indicating whether a row was deleted.

        The parameters are as follows:

        :param action_id: The unique identifier of the Action to erase.
        :type action_id: str
        :return: True if a row was deleted, False if no matching Action.
        :rtype: bool
        :raise Exception: If the database deletion operation fails.
        """
        # Build the DELETE SQL statement targeting the specific Action.
        string_sql = "DELETE FROM Actions WHERE Id = ?"
        # Attempt to execute the DELETE statement against the database.
        try:
            # Execute the DELETE statement with the action_id parameter.
            cursor_result = self.database_manager.run_sql_statement(string_sql, (action_id,))
            # Commit the transaction to persist the deletion.
            self.database_manager.connection.commit()
        # Handle any database error that occurs during the DELETE operation.
        except Exception as exception_error:
            # Build the error message describing the deletion failure in Chinese.
            message_error = f"[X] (OtherError) 删除Action失败，Action ID: {action_id}: {exception_error}"
            # Output the error message to the console for user visibility.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Determine whether at least one record was removed by the DELETE operation.
        is_deleted = cursor_result.rowcount > 0
        # Return the boolean deletion result to the caller.
        return is_deleted

    def _init_form_timestamp_function_(self) -> str:
        """
        Generate a UTC timestamp string in ISO 8601 format.

        Produces a timezone-aware UTC datetime string suitable for
        writing to the CreatedAt and UpdatedAt database columns.

        The parameters are as follows:

        :return: The current UTC timestamp in ISO 8601 format.
        :rtype: str
        """
        # Generate the current datetime in UTC with timezone awareness.
        timestamp_utc = datetime.now(timezone.utc)
        # Format the UTC datetime as an ISO 8601 string for database storage.
        string_timestamp = timestamp_utc.isoformat()
        # Return the formatted ISO 8601 timestamp string to the caller.
        return string_timestamp
