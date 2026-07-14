# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================

MODULE               : PLANS.strack

TYPE                 : Python Script

DESCRIPTION          :
    Strack entity CRUD operations. Strack is the top-level organizing
    container in PLANS, linking Plans, Issues, Actions, and Notes under
    a single stack identifier for project-based management.

AUTHOR               : Suzuki Yumemi

CONTACT              : szkymm@gmail.com

MAINTAINER           :
    Suzuki Yumemi (szkymm@gmail.com)
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
    from PLANS.strack import StrackManager
    from PLANS.database import DatabaseManager
    database = DatabaseManager("plans.db")
    database.initialize_schema()
    manager = StrackManager(database)
    manager.create_strack("my-project", "My Project Description")

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
import logging
import sqlite3

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .database import DatabaseManager

__version__ = "0.1.0"

# Configure the module-level logger for diagnostic output.
logger = logging.getLogger(__name__)


class StrackManager:
    """
    STRACKMANAGER CLASS IS CORE PART OF PLANS STRACK.PY.

    PLANS.strack.StrackManager:
        Manages Strack entity lifecycle including creation, retrieval,
        updating, deletion, and listing operations against the SQLite database.

    ATTRIBUTES                         :
        database_manager (DatabaseManager): The DatabaseManager instance providing the SQLite connection.

    PUBLIC METHODS                     :
        create_strack(strack_id, title, description="", priority=3) -> dict:
            Create a new Strack entity and return its data dictionary.
        get_strack(strack_id) -> Optional[dict]:
            Retrieve a single Strack by its identifier.
        list_stracks(status=None) -> list:
            List all Stracks, optionally filtered by status.
        update_strack(strack_id, **kwargs) -> dict:
            Update fields of an existing Strack.
        delete_strack(strack_id) -> bool:
            Remove a Strack and all its associated entities.

    PRIVATE METHODS                    :
        _init_generate_timestamp_function_() -> str:
            Generate an ISO8601 UTC timestamp string for the current moment.

    USAGE                             :
        manager = StrackManager(database_manager)
        strack = manager.create_strack("backend-api", "Backend API Project")
        all_stracks = manager.list_stracks()

    WARNING                           :
        Private methods should not be called from outside the class.
    """

    def __init__(self, database_manager):
        """
        Initialize the StrackManager with a database connection.

        Stores the DatabaseManager reference for all subsequent
        CRUD operations against the Stracks table.

        The parameters are as follows:

        :param database_manager: The DatabaseManager instance with an active SQLite connection.
        :type database_manager: DatabaseManager
        """
        # Store the database manager reference for connection access.
        self.database_manager = database_manager

    def _init_generate_timestamp_function_(self):
        """
        Generate an ISO8601 UTC timestamp string for the current moment.

        Uses datetime.now with UTC timezone to produce a timezone-aware
        ISO 8601 formatted string suitable for database storage.

        :return: The current UTC timestamp in ISO8601 format.
        :rtype: str
        """
        # Obtain the current moment in UTC with timezone awareness.
        return datetime.now(timezone.utc).isoformat()

    def create_strack(self, strack_id, title, description="", priority=3):
        """
        Create a new Strack entity and persist it to the database.

        Inserts a new row into the Stracks table with the provided
        identifier, title, description, and priority level. Timestamps
        are automatically generated for creation and update tracking.

        The parameters are as follows:

        :param strack_id: The kebab-case string identifier for the strack.
        :type strack_id: str
        :param title: The human-readable title of the strack.
        :type title: str
        :param description: An optional longer description of the strack.
        :type description: str
        :param priority: The numeric priority level, lower values indicate higher priority.
        :type priority: int
        :return: A dictionary representation of the newly created strack row.
        :rtype: dict
        :raise sqlite3.Error: When the database insert operation fails.
        :raise Exception: When an unanticipated error occurs during creation.
        """
        # Capture the current UTC timestamp for creation and update tracking.
        timestamp_now = str(datetime.now(timezone.utc).isoformat())
        # Attempt to insert the new strack row into the database.
        try:
            # Build the SQL insert prefix with column names.
            sql_insert = "INSERT INTO Stracks (Id, Title, Description, Priority, Status, "
            # Append the remaining column names and value placeholders.
            sql_insert += "CreatedAt, UpdatedAt) VALUES (?, ?, ?, ?, ?, ?, ?)"
            # Execute the insert with the provided strack attribute values.
            self.database_manager.connection.execute(
                sql_insert,
                (strack_id, title, description, priority, "active",
                 timestamp_now, timestamp_now),
            )
            # Persist the transaction to the database file.
            self.database_manager.connection.commit()
        except sqlite3.Error as sqlite_error:
            # Build the error message with the exception context in Chinese.
            message_error = f"[X] (SQLError) 数据库插入失败: {sqlite_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise sqlite3.Error(message_error) from sqlite_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = f"[X] (OtherError) 发生其他未知错误，具体查看: {exception_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Return the newly created strack as a dictionary.
        return self.get_strack(strack_id)

    def get_strack(self, strack_id):
        """
        Retrieve a single Strack by its identifier.

        Queries the Stracks table for a row matching the given
        strack identifier and returns its data as a dictionary.

        The parameters are as follows:

        :param strack_id: The kebab-case string identifier of the strack to retrieve.
        :type strack_id: str
        :return: A dictionary of the strack data, or None when no match exists.
        :rtype: Optional[dict]
        :raise sqlite3.Error: When the database select operation fails.
        :raise Exception: When an unanticipated error occurs during retrieval.
        """
        # Attempt to retrieve the strack row from the database.
        try:
            # Build the SQL select statement for a single strack.
            sql_select = "SELECT * FROM Stracks WHERE Id = ?"
            # Execute the select query with the strack identifier.
            connection_cursor = self.database_manager.connection.execute(
                sql_select, (strack_id,)
            )
            # Fetch the first matching row from the result set.
            row_result = connection_cursor.fetchone()
        except sqlite3.Error as sqlite_error:
            # Build the error message with the exception context in Chinese.
            message_error = f"[X] (SQLError) 数据库查询失败: {sqlite_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise sqlite3.Error(message_error) from sqlite_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = f"[X] (OtherError) 发生其他未知错误，具体查看: {exception_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Return None when no matching strack exists in the database.
        if row_result is None:
            return None
        # Convert the row tuple to a dictionary keyed by PascalCase column names.
        dict_result = {
            "Id": row_result[0],
            "Title": row_result[1],
            "Description": row_result[2],
            "Priority": row_result[3],
            "Status": row_result[4],
            "CreatedAt": row_result[5],
            "UpdatedAt": row_result[6],
        }
        # Return the dictionary representation of the strack.
        return dict_result

    def list_stracks(self, status=None):
        """
        List all Stracks, optionally filtered by status.

        Queries the Stracks table and returns all rows ordered by
        priority in ascending order. An optional status parameter
        filters results to a specific status value.

        The parameters are as follows:

        :param status: An optional status string to filter strack results.
        :type status: Optional[str]
        :return: A list of dictionaries, each representing a strack row.
        :rtype: list
        :raise sqlite3.Error: When the database list query fails.
        :raise Exception: When an unanticipated error occurs during listing.
        """
        # Attempt to list all stracks from the database.
        try:
            # Determine whether a status filter was provided for the query.
            has_status = status is not None
            # Check if a status filter was provided for the query.
            if has_status:
                # Build the filtered select statement ordered by priority.
                sql_select = "SELECT * FROM Stracks WHERE Status = ? ORDER BY Priority ASC"
                # Execute the filtered query with the status parameter.
                connection_cursor = self.database_manager.connection.execute(
                    sql_select, (status,)
                )
            else:
                # Build the unfiltered select statement ordered by priority.
                sql_select = "SELECT * FROM Stracks ORDER BY Priority ASC"
                # Execute the unfiltered query without parameters.
                connection_cursor = self.database_manager.connection.execute(sql_select)
            # Fetch all matching rows from the result set.
            list_rows = connection_cursor.fetchall()
        except sqlite3.Error as sqlite_error:
            # Build the error message with the exception context in Chinese.
            message_error = f"[X] (SQLError) 数据库列表查询失败: {sqlite_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise sqlite3.Error(message_error) from sqlite_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = f"[X] (OtherError) 发生其他未知错误，具体查看: {exception_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Initialize the empty list for accumulating result dictionaries.
        list_results = []
        # Iterate over each row to convert to dictionary format.
        for row_data in list_rows:
            # Build the dictionary from column values for the current row.
            dict_result = {
                "Id": row_data[0],
                "Title": row_data[1],
                "Description": row_data[2],
                "Priority": row_data[3],
                "Status": row_data[4],
                "CreatedAt": row_data[5],
                "UpdatedAt": row_data[6],
            }
            # Append the converted dictionary to the results list.
            list_results.append(dict_result)
        # Return the complete list of strack dictionaries.
        return list_results

    def update_strack(self, strack_id, **kwargs):
        """
        Update fields of an existing Strack entity.

        Dynamically builds a SET clause from the provided keyword
        arguments, restricted to allowed columns. The UpdatedAt
        timestamp is always refreshed on modification.

        The parameters are as follows:

        :param strack_id: The kebab-case string identifier of the strack to update.
        :type strack_id: str
        :param kwargs: Keyword arguments mapping column names to new values.
        :type kwargs: dict
        :return: A dictionary representation of the updated strack row.
        :rtype: dict
        :raise sqlite3.Error: When the database update operation fails.
        :raise Exception: When an unanticipated error occurs during updating.
        """
        # Define the set of allowed column names for updating.
        set_allowed = {"Title", "Description", "Status", "Priority"}
        # Filter kwargs to only include allowed update columns.
        dict_updates = {
            key_name: key_value
            for key_name, key_value in kwargs.items()
            if key_name in set_allowed
        }
        # Return early when no valid update fields are provided.
        if not dict_updates:
            return self.get_strack(strack_id)
        # Capture the current UTC timestamp for the update tracking.
        timestamp_now = str(datetime.now(timezone.utc).isoformat())
        # Build the SET clause from the filtered update field names.
        set_clause = ", ".join(
            f"{key_name} = ?" for key_name in dict_updates
        )
        # Append the UpdatedAt column to the SET clause.
        set_clause += ", UpdatedAt = ?"
        # Build the parameter tuple from update values, timestamp, and identifier.
        tuple_params = tuple(dict_updates.values()) + (timestamp_now, strack_id)
        # Attempt to update the strack row in the database.
        try:
            # Build the SQL update statement with the dynamic SET clause.
            sql_update = f"UPDATE Stracks SET {set_clause} WHERE Id = ?"
            # Execute the update statement with the parameter tuple.
            self.database_manager.connection.execute(sql_update, tuple_params)
            # Persist the transaction to the database file.
            self.database_manager.connection.commit()
        except sqlite3.Error as sqlite_error:
            # Build the error message with the exception context in Chinese.
            message_error = f"[X] (SQLError) 数据库更新失败: {sqlite_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise sqlite3.Error(message_error) from sqlite_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = f"[X] (OtherError) 发生其他未知错误，具体查看: {exception_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Return the updated strack as a dictionary.
        return self.get_strack(strack_id)

    def delete_strack(self, strack_id):
        """
        Remove a Strack and all its associated entities from the database.

        Deletes the strack row identified by the given strack identifier.
        Returns a boolean indicating whether a row was actually removed.

        The parameters are as follows:

        :param strack_id: The kebab-case string identifier of the strack to delete.
        :type strack_id: str
        :return: True when a row was deleted, False when no matching row existed.
        :rtype: bool
        :raise sqlite3.Error: When the database delete operation fails.
        :raise Exception: When an unanticipated error occurs during deletion.
        """
        # Attempt to delete the strack row from the database.
        try:
            # Build the SQL delete statement for the specified strack.
            sql_delete = "DELETE FROM Stracks WHERE Id = ?"
            # Execute the delete statement with the strack identifier.
            connection_cursor = self.database_manager.connection.execute(
                sql_delete, (strack_id,)
            )
            # Persist the transaction to the database file.
            self.database_manager.connection.commit()
        except sqlite3.Error as sqlite_error:
            # Build the error message with the exception context in Chinese.
            message_error = f"[X] (SQLError) 数据库删除失败: {sqlite_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise sqlite3.Error(message_error) from sqlite_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = f"[X] (OtherError) 发生其他未知错误，具体查看: {exception_error}"
            # Output the error message with full traceback for diagnostics.
            logger.error(message_error, exc_info=True)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Verify that at least one row was affected by the deletion.
        is_deleted = connection_cursor.rowcount > 0
        # Return the boolean result indicating deletion success.
        return is_deleted
