# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================

MODULE               : PLANS.plan

TYPE                 : Python Script

DESCRIPTION          :
    Plan entity manager for the PLANS local-first project management system.
    Provides CRUD operations for Plan (todo) items belonging to Strack
    containers, with status tracking and configurable priority levels.

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
    from PLANS import DatabaseManager, PlanManager

    database = DatabaseManager("plans.db")
    database.initialize_schema()
    plan_manager = PlanManager(database)
    plan = plan_manager.insert_plan_record(
        "project-1", "task-1", "Design REST API", "Draft endpoints", 2
    )
    active_plans = plan_manager.list_plans(status_value="in_progress")
    plan_manager.modify_plan_fields("task-1", Status="done")
    plan_manager.erase_plan_record("task-1")

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

# Define the file version string to match FILE VERSION in docstring.
__version__ = "0.1.2"

# Import datetime for UTC-aware timestamp generation in create and update flows.
from datetime import datetime, timezone
# Import type hint classes for method signature annotations and return types.
from typing import Optional, List, Dict, Any
# Import sqlite3 for specific database exception type handling in except blocks.
import sqlite3
# Import the DatabaseManager for dependency injection via the constructor.
from .database import DatabaseManager


class PlanManager:
    """
    PlanManager CLASS IS CORE PART OF PLANS plan.

    PLANS.plan.PlanManager:
        Manages Plan (todo) entities with full CRUD lifecycle including
        creation, retrieval, filtered listing, field-level updates, and
        deletion within the local-first SQLite database.

    ATTRIBUTES                         :
        database_manager (DatabaseManager): Reference to the injected database
            manager providing SQLite connection access for all SQL operations.

    PUBLIC METHODS                     :
        insert_plan_record(strack_id, plan_id, plan_title,
            plan_description, priority_level) -> Dict[str, Any]:
            Insert a new Plan row into the Plans table and return the created
            record as a dictionary with PascalCase keys.
        retrieve_plan(plan_id) -> Optional[Dict[str, Any]]:
            Retrieve a single Plan by its unique identifier, returning None
            when no matching row is found.
        list_plans(strack_id, status_value) -> List[Dict[str, Any]]:
            Return all Plan rows optionally filtered by parent Strack identifier
            or by current status value.
        modify_plan_fields(plan_id, **update_kwargs) -> Dict[str, Any]:
            Update specified PascalCase fields of an existing Plan row and
            return the refreshed record after applying changes.
        erase_plan_record(plan_id) -> bool:
            Remove a Plan row by its unique identifier and indicate whether
            at least one row was actually deleted.

    PRIVATE METHODS                    :
        _init_form_timestamp_function_() -> str:
            Produce an ISO 8601 UTC timestamp string for populating CreatedAt
            and UpdatedAt columns during create and update operations.

    USAGE                             :
        manager = PlanManager(database_manager)
        plan = manager.insert_plan_record("proj-1", "p-1", "Design API", "", 2)
        manager.modify_plan_fields("p-1", Status="in_progress")
        active = manager.list_plans(status_value="in_progress")
        manager.erase_plan_record("p-1")

    WARNING                           :
        Private methods should not be called from outside the class.
    """

    def __init__(self, database_manager: DatabaseManager):
        """
        Initialize the PlanManager with a database connection dependency.

        Stores the provided DatabaseManager instance for use by all subsequent
        create, read, update, and delete method calls on the Plans table.

        The parameters are as follows:

        :param database_manager: The injected database manager providing SQLite
            connection and schema access.
        :type database_manager: DatabaseManager
        """
        # Store the injected database manager for all subsequent SQL operations.
        self.database_manager = database_manager

    def _init_form_timestamp_function_(self) -> str:
        """
        Generate the current UTC timestamp in ISO 8601 format.

        Captures the system UTC clock and formats it as a timezone-aware
        ISO 8601 string suitable for storage in CreatedAt and UpdatedAt.

        The parameters are as follows:

        :return: ISO 8601 formatted UTC timestamp string for database storage.
        :rtype: str
        """
        # Capture the current moment in the UTC timezone for consistent storage.
        current_time = datetime.now(timezone.utc)
        # Return the ISO 8601 formatted string ready for database column storage.
        return current_time.isoformat()

    def insert_plan_record(
        # Accept the class instance reference as the first implicit parameter.
        self,
        # Declare the parent Strack container identifier parameter.
        strack_id: str,
        # Declare the unique Plan identifier parameter.
        plan_id: str,
        # Declare the display title for the Plan entity.
        plan_title: str,
        # Declare the optional longer-form description with an empty string default.
        plan_description: str = "",
        # Declare the numeric priority level with a default of three for medium urgency.
        priority_level: int = 3,
    # Close the parameter list and declare the return type as a string-keyed dictionary.
    ) -> Dict[str, Any]:
        """
        Insert a new Plan row into the Plans table and return the created record.

        Validates the priority level against the allowed closed range of 1
        through 5, generates the creation and update timestamps, and constructs
        the INSERT statement with all required fields before returning the
        newly persisted row.

        The parameters are as follows:

        :param strack_id: Unique identifier of the parent Strack container that
            owns this Plan item.
        :type strack_id: str
        :param plan_id: Unique identifier for this Plan entity, serving as the
            primary key in the Plans table.
        :type plan_id: str
        :param plan_title: Display title describing the Plan item for user-facing
            listing and search contexts.
        :type plan_title: str
        :param plan_description: Optional longer-form description providing
            additional detail beyond the title.
        :type plan_description: str
        :param priority_level: Priority level as an integer from 1 (highest
            urgency) to 5 (lowest urgency). Defaults to 3.
        :type priority_level: int
        :return: Dictionary representation of the newly inserted Plan row with
            PascalCase keys for all columns.
        :rtype: Dict[str, Any]
        """
        # Clamp the priority level to the valid inclusive range of 1 through 5.
        if priority_level < 1:
            # Override values below the minimum with the lowest valid priority.
            priority_level = 1
        # Clamp values above the maximum allowed priority to the ceiling of five.
        if priority_level > 5:
            # Override values above the maximum with the highest valid priority.
            priority_level = 5
        # Generate the current UTC timestamp for CreatedAt and UpdatedAt columns.
        current_time = self._init_form_timestamp_function_()
        # Build the parameterised INSERT SQL targeting all seven Plan columns.
        insert_sql = (
            # Start the INSERT column list with the primary identifier fields.
            "INSERT INTO Plans (Id, StrackId, Title, Description, "
            # Continue the column list with status and timestamp columns.
            + "Status, Priority, CreatedAt, UpdatedAt) "
            # Complete the INSERT with positional parameter placeholders.
            + "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        # Assemble the parameter tuple matching the column order in the INSERT.
        insert_params = (
            # Bind the unique Plan identifier as the first positional parameter.
            plan_id,
            # Bind the parent Strack identifier as the second positional parameter.
            strack_id,
            # Bind the display title as the third positional parameter.
            plan_title,
            # Bind the optional long-form description as the fourth positional parameter.
            plan_description,
            # Bind the default pending status string as the fifth positional parameter.
            "pending",
            # Bind the clamped priority level integer as the sixth positional parameter.
            priority_level,
            # Bind the creation timestamp as the seventh positional parameter.
            current_time,
            # Bind the same timestamp for the initial update time as the eighth parameter.
            current_time,
        )
        # Attempt to execute the parameterised INSERT against the Plans table.
        try:
            # Open a cursor on the database connection for statement execution.
            database_cursor = self.database_manager.connection.cursor()
            # Execute the prepared INSERT statement with the bound parameters.
            database_cursor.execute(insert_sql, insert_params)
            # Commit the transaction to persist the new Plan row to disk.
            self.database_manager.connection.commit()
        # Handle general database-level errors that prevent the INSERT from completing.
        except sqlite3.DatabaseError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (DatabaseError) 数据库通用错误，插入计划失败: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Handle integrity constraint violations such as duplicate primary keys.
        except sqlite3.IntegrityError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix indicating an integrity violation.
                "[X] (IntegrityError) 数据完整性约束违反，"
                # Append the description of the likely constraint failure cause.
                + "计划 ID 或 Strack ID 可能重复或缺失: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Handle operational errors such as missing tables or locked databases.
        except sqlite3.OperationalError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (OperationalError) 数据库操作错误，"
                # Append the description indicating the table or connection may be unavailable.
                + "连接或表可能不可用: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Catch any unanticipated exception type as the final safety net.
        except Exception as exception_error:
            # Build the Chinese-language error message for unanticipated errors.
            message_error = (
                # Append the generic unknown error prefix with Chinese diagnostic text.
                "[X] (OtherError) 发生其他未知错误，插入计划失败: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Build the column list portion of the SELECT SQL for Plan retrieval.
        select_sql = "SELECT Id, StrackId, Title, Description, Status, "
        # Append remaining columns and WHERE clause for the Plan record.
        select_sql += "Priority, CreatedAt, UpdatedAt FROM Plans WHERE Id = ?"
        # Attempt to fetch the inserted row back from the database.
        try:
            # Open a cursor on the database connection for the SELECT query.
            database_cursor = self.database_manager.connection.cursor()
            # Execute the parameterised SELECT using the plan identifier.
            database_cursor.execute(select_sql, (plan_id,))
            # Fetch the single matching row from the cursor result set.
            result_row = database_cursor.fetchone()
        # Handle general database-level errors that prevent the SELECT from completing.
        except sqlite3.DatabaseError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (DatabaseError) 数据库通用错误，无法获取新建计划: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Handle operational errors such as missing tables or locked databases.
        except sqlite3.OperationalError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (OperationalError) 数据库操作错误，"
                # Append the description indicating the SELECT query could not execute.
                + "无法查询新建计划: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Catch any unanticipated exception type as the final safety net.
        except Exception as exception_error:
            # Build the Chinese-language error message for unanticipated errors.
            message_error = (
                # Append the generic unknown error prefix with Chinese diagnostic text.
                "[X] (OtherError) 发生其他未知错误，无法获取新建计划: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Verify that the SELECT query returned a valid row from the cursor.
        if result_row is None:
            # Return an empty dictionary when the select unexpectedly produced no row.
            return {}
        # Convert the raw tuple into a dictionary with PascalCase column keys.
        query_result = {
            # Map the first column to the unique Plan identifier key.
            "ID": result_row[0],
            # Map the second column to the parent Strack identifier key.
            "StrackID": result_row[1],
            # Map the third column to the display title key.
            "Title": result_row[2],
            # Map the fourth column to the optional description key.
            "Description": result_row[3],
            # Map the fifth column to the lifecycle status key.
            "Status": result_row[4],
            # Map the sixth column to the priority level integer key.
            "Priority": result_row[5],
            # Map the seventh column to the creation timestamp key.
            "CreatedAt": result_row[6],
            # Map the eighth column to the last update timestamp key.
            "UpdatedAt": result_row[7],
        }
        # Return the fully constructed dictionary for the newly created Plan.
        return query_result

    def retrieve_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single Plan row by its unique identifier.

        Executes a parameterised SELECT query targeting the primary key and
        returns the matching row as a dictionary, or None when no Plan with
        the given identifier exists in the Plans table.

        The parameters are as follows:

        :param plan_id: The unique identifier of the Plan to retrieve.
        :type plan_id: str
        :return: Dictionary with PascalCase keys representing the Plan row,
            or None when the identifier is not found.
        :rtype: Optional[Dict[str, Any]]
        """
        # Build the parameterised SELECT SQL for the Plan by primary key.
        select_sql = (
            # Start the SELECT statement with all Plan column names for retrieval.
            "SELECT Id, StrackId, Title, Description, Status, "
            # Complete the column list and add the primary key WHERE clause.
            + "Priority, CreatedAt, UpdatedAt FROM Plans WHERE Id = ?"
        )
        # Attempt to execute the SELECT query with the plan identifier.
        try:
            # Open a cursor on the database connection for the SELECT query.
            database_cursor = self.database_manager.connection.cursor()
            # Execute the parameterised SELECT using the plan identifier.
            database_cursor.execute(select_sql, (plan_id,))
            # Fetch the single matching row from the cursor result set.
            result_row = database_cursor.fetchone()
        # Handle general database-level errors that prevent the SELECT from completing.
        except sqlite3.DatabaseError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (DatabaseError) 数据库通用错误，无法获取计划: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception by returning None to signal retrieval failure.
            return None
        # Handle operational errors such as missing tables or locked databases.
        except sqlite3.OperationalError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (OperationalError) 数据库操作错误，"
                # Append the description indicating the SELECT query could not execute.
                + "无法查询计划: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception by returning None to signal retrieval failure.
            return None
        # Catch any unanticipated exception type as the final safety net.
        except Exception as exception_error:
            # Build the Chinese-language error message for unanticipated errors.
            message_error = (
                # Append the generic unknown error prefix with Chinese diagnostic text.
                "[X] (OtherError) 发生其他未知错误，无法获取计划: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception by returning None to signal retrieval failure.
            return None
        # Verify that the SELECT query returned a valid row from the cursor.
        if result_row is None:
            # Return None when no Plan exists with the requested identifier.
            return None
        # Convert the raw cursor tuple into a dictionary with PascalCase keys.
        query_result = {
            # Map the first column to the unique Plan identifier key.
            "ID": result_row[0],
            # Map the second column to the parent Strack identifier key.
            "StrackID": result_row[1],
            # Map the third column to the display title key.
            "Title": result_row[2],
            # Map the fourth column to the optional description key.
            "Description": result_row[3],
            # Map the fifth column to the lifecycle status key.
            "Status": result_row[4],
            # Map the sixth column to the priority level integer key.
            "Priority": result_row[5],
            # Map the seventh column to the creation timestamp key.
            "CreatedAt": result_row[6],
            # Map the eighth column to the last update timestamp key.
            "UpdatedAt": result_row[7],
        }
        # Return the constructed dictionary representing the retrieved Plan row.
        return query_result

    def list_plans(
        # Accept the class instance reference as the first implicit parameter.
        self,
        # Declare the optional parent Strack identifier for result filtering.
        strack_id: Optional[str] = None,
        # Declare the optional status value for filtering Plan lifecycle stages.
        status_value: Optional[str] = None,
    # Close the parameter list and declare the return type as a list of dictionaries.
    ) -> List[Dict[str, Any]]:
        """
        Return all Plan rows optionally filtered by Strack or status.

        Builds a dynamic SELECT query that appends WHERE clauses for the
        parent Strack identifier and current status value when those filters
        are provided, returning the full matching set as a list of dictionaries.

        The parameters are as follows:

        :param strack_id: Optional parent Strack identifier for filtering Plans
            by their containing container. None means no Strack filter.
        :type strack_id: Optional[str]
        :param status_value: Optional status value for filtering Plans by their
            current lifecycle stage. None means no status filter.
        :type status_value: Optional[str]
        :return: List of Plan dictionaries with PascalCase keys, possibly empty
            when no rows match the applied filters.
        :rtype: List[Dict[str, Any]]
        """
        # Detect whether a Strack identifier filter has been provided.
        has_strack = strack_id is not None
        # Detect whether a status value filter has been provided.
        has_status = status_value is not None
        # Start building the base SELECT query targeting all Plan columns.
        query_sql = (
            # Begin the SELECT statement with all Plan column names.
            "SELECT Id, StrackId, Title, Description, Status, "
            # Complete the column list from the Plans table without any filter.
            + "Priority, CreatedAt, UpdatedAt FROM Plans"
        )
        # Initialise the empty parameter list for the dynamic WHERE clauses.
        query_params = []
        # Append a WHERE clause for the Strack identifier when the filter is set.
        if has_strack:
            # Add the first filtering condition with the Strack identifier.
            query_sql += " WHERE StrackId = ?"
            # Append the Strack identifier to the parameter list for binding.
            query_params.append(strack_id)
        # Append a WHERE or AND clause for the status value when the filter is set.
        if has_status:
            # Choose the conjunction based on whether a prior WHERE clause exists.
            if has_strack:
                # Extend the existing WHERE clause with an AND conjunction.
                query_sql += " AND Status = ?"
            # Start a new WHERE clause when no prior Strack filter was applied.
            else:
                # Start a new WHERE clause with the Status filter as the first condition.
                query_sql += " WHERE Status = ?"
            # Append the status value to the parameter list for binding.
            query_params.append(status_value)
        # Append the default ordering clause to sort by creation time descending.
        query_sql += " ORDER BY CreatedAt DESC"
        # Attempt to execute the dynamically built SELECT query.
        try:
            # Open a cursor on the database connection for the SELECT query.
            database_cursor = self.database_manager.connection.cursor()
            # Execute the parameterised SELECT with the accumulated bindings.
            database_cursor.execute(query_sql, query_params)
            # Fetch all matching rows from the cursor result set.
            result_records = database_cursor.fetchall()
        # Handle general database-level errors that prevent the SELECT from completing.
        except sqlite3.DatabaseError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (DatabaseError) 数据库通用错误，无法列出计划: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception by returning an empty list as the fallback.
            return []
        # Handle operational errors such as missing tables or locked databases.
        except sqlite3.OperationalError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (OperationalError) 数据库操作错误，"
                # Append the description indicating the list query could not execute.
                + "无法查询计划列表: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception by returning an empty list as the fallback.
            return []
        # Catch any unanticipated exception type as the final safety net.
        except Exception as exception_error:
            # Build the Chinese-language error message for unanticipated errors.
            message_error = (
                # Append the generic unknown error prefix with Chinese diagnostic text.
                "[X] (OtherError) 发生其他未知错误，无法列出计划: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception by returning an empty list as the fallback.
            return []
        # Initialise the output list for collecting converted Plan dictionaries.
        list_result = []
        # Iterate over each raw tuple returned by the SELECT query.
        for result_row in result_records:
            # Convert the raw cursor tuple into a dictionary with PascalCase keys.
            query_result = {
                # Map the first column to the unique Plan identifier key.
                "ID": result_row[0],
                # Map the second column to the parent Strack identifier key.
                "StrackID": result_row[1],
                # Map the third column to the display title key.
                "Title": result_row[2],
                # Map the fourth column to the optional description key.
                "Description": result_row[3],
                # Map the fifth column to the lifecycle status key.
                "Status": result_row[4],
                # Map the sixth column to the priority level integer key.
                "Priority": result_row[5],
                # Map the seventh column to the creation timestamp key.
                "CreatedAt": result_row[6],
                # Map the eighth column to the last update timestamp key.
                "UpdatedAt": result_row[7],
            }
            # Append the constructed dictionary to the accumulating result list.
            list_result.append(query_result)
        # Return the complete list of Plan dictionaries matching the filters.
        return list_result

    def modify_plan_fields(self, plan_id: str, **update_kwargs: Any) -> Dict[str, Any]:
        """
        Update specified fields of an existing Plan and return the refreshed record.

        Builds a dynamic UPDATE statement from the provided PascalCase keyword
        arguments, generates a new UpdatedAt timestamp, and re-fetches the
        modified row from the database after committing the change.

        The parameters are as follows:

        :param plan_id: The unique identifier of the Plan to update.
        :type plan_id: str
        :param update_kwargs: PascalCase field names and their new values.
            Supported keys: Title, Description, Status, Priority.
        :type update_kwargs: Dict[str, Any]
        :return: Dictionary representation of the Plan row after the update,
            or an empty dictionary when no matching Plan exists.
        :rtype: Dict[str, Any]
        """
        # Define the set of PascalCase column names permitted for field updates.
        allowed_columns = {"Title", "Description", "Status", "Priority"}
        # Exit early with an empty dict when no keyword arguments were provided.
        if not update_kwargs:
            # Return an empty dictionary signalling an empty update request.
            return {}
        # Initialise the list of SET clause fragments for the dynamic UPDATE.
        set_clauses = []
        # Initialise the list of bound parameter values for the prepared statement.
        update_params = []
        # Iterate over each provided keyword argument to build SET clauses.
        for plan_keyword, plan_value in update_kwargs.items():
            # Skip any keyword argument whose key is not in the allowed set.
            if plan_keyword not in allowed_columns:
                # Advance to the next iteration without processing this entry.
                continue
            # Generate a unique parameter placeholder for the current column.
            set_clauses.append(plan_keyword + " = ?")
            # Append the parameter value for binding in positional order.
            update_params.append(plan_value)
        # Exit early with an empty dict when no valid columns remain after filtering.
        if not set_clauses:
            # Return an empty dictionary signalling no valid fields to update.
            return {}
        # Append the UpdatedAt timestamp clause so it is always refreshed.
        set_clauses.append("UpdatedAt = ?")
        # Generate the current UTC timestamp for the UpdatedAt column value.
        current_time = self._init_form_timestamp_function_()
        # Append the fresh timestamp string to the parameter list.
        update_params.append(current_time)
        # Append the plan identifier as the final parameter for the WHERE clause.
        update_params.append(plan_id)
        # Build the full UPDATE SQL statement by joining all SET clauses.
        update_sql = "UPDATE Plans SET " + ", ".join(set_clauses) + " WHERE Id = ?"
        # Attempt to execute the parameterised UPDATE against the Plans table.
        try:
            # Open a cursor on the database connection for statement execution.
            database_cursor = self.database_manager.connection.cursor()
            # Execute the prepared UPDATE statement with the bound parameters.
            database_cursor.execute(update_sql, update_params)
            # Commit the transaction to persist the modified Plan row to disk.
            self.database_manager.connection.commit()
        # Handle general database-level errors that prevent the UPDATE from completing.
        except sqlite3.DatabaseError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (DatabaseError) 数据库通用错误，更新计划失败: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Handle integrity constraint violations that may occur during the update.
        except sqlite3.IntegrityError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix indicating an integrity violation.
                "[X] (IntegrityError) 数据完整性约束违反，"
                # Append the description of the update failure context.
                + "更新计划失败: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Handle operational errors such as missing tables or locked databases.
        except sqlite3.OperationalError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (OperationalError) 数据库操作错误，"
                # Append the description of the update failure context.
                + "更新计划失败: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Catch any unanticipated exception type as the final safety net.
        except Exception as exception_error:
            # Build the Chinese-language error message for unanticipated errors.
            message_error = (
                # Append the generic unknown error prefix with Chinese diagnostic text.
                "[X] (OtherError) 发生其他未知错误，更新计划失败: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal failure with an empty dictionary.
            return {}
        # Re-fetch the updated Plan row to return current state to the caller.
        return self.retrieve_plan(plan_id) or {}

    def erase_plan_record(self, plan_id: str) -> bool:
        """
        Remove a Plan row from the Plans table by its unique identifier.

        Executes a parameterised DELETE statement targeting the primary key
        and returns a boolean indicating whether one or more rows were
        actually removed from the database.

        The parameters are as follows:

        :param plan_id: The unique identifier of the Plan to delete.
        :type plan_id: str
        :return: True when at least one row was deleted, False otherwise.
        :rtype: bool
        """
        # Build the parameterised DELETE SQL targeting the Plan by primary key.
        delete_sql = "DELETE FROM Plans WHERE Id = ?"
        # Attempt to execute the parameterised DELETE against the Plans table.
        try:
            # Open a cursor on the database connection for statement execution.
            database_cursor = self.database_manager.connection.cursor()
            # Execute the prepared DELETE statement with the bound plan identifier.
            database_cursor.execute(delete_sql, (plan_id,))
            # Commit the transaction to persist the row removal to disk.
            self.database_manager.connection.commit()
            # Capture the count of rows affected by the DELETE execution.
            success_count = database_cursor.rowcount
        # Handle general database-level errors that prevent the DELETE from completing.
        except sqlite3.DatabaseError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (DatabaseError) 数据库通用错误，删除计划失败: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal that no rows were deleted.
            return False
        # Handle operational errors such as missing tables or locked databases.
        except sqlite3.OperationalError as exception_error:
            # Build the Chinese-language error message with exception context.
            message_error = (
                # Append the error type prefix with Chinese diagnostic text.
                "[X] (OperationalError) 数据库操作错误，"
                # Append the description of the deletion failure context.
                + "删除计划失败: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal that no rows were deleted.
            return False
        # Catch any unanticipated exception type as the final safety net.
        except Exception as exception_error:
            # Build the Chinese-language error message for unanticipated errors.
            message_error = (
                # Append the generic unknown error prefix with Chinese diagnostic text.
                "[X] (OtherError) 发生其他未知错误，删除计划失败: "
                # Append the exception details to the error message for diagnostics.
                + str(exception_error)
            )
            # Output the error message for the caller and diagnostic review.
            print(message_error)
            # Terminate the exception and signal that no rows were deleted.
            return False
        # Evaluate whether the rowcount indicates at least one row was removed.
        if success_count > 0:
            # Return True to confirm successful deletion of one or more rows.
            return True
        # Return False when no matching Plan was found for the given identifier.
        return False
