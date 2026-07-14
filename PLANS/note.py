# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================

MODULE               : PLANS.note

TYPE                 : Python Script

DESCRIPTION          :
    Note entity manager for the PLANS local-first project management system.
    Provides CRUD operations for free-form documentation entries belonging
    to Strack containers, with title and content fields persisted in SQLite.

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

PYTHON               : >=3.8

LICENSE              : GPL-3.0-only

SPDX ID              : GPL-3.0-only


USAGE                :
    from PLANS import NoteManager

    note_manager = NoteManager(database_manager)
    note = note_manager.create_note("strack-1", "note-1", "Meeting Notes",
                                    "Discussed Q3 roadmap milestones.")
    existing = note_manager.get_note("note-1")
    all_notes = note_manager.list_notes(strack_id="strack-1")
    updated = note_manager.update_note("note-1", Title="Revised Title")
    was_deleted = note_manager.delete_note("note-1")

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

# Define the module version string to match PROJECT VERSION in docstring.
__version__ = "0.1.0"

# Import the datetime class for generating ISO 8601 UTC timestamps.
from datetime import datetime, timezone
# Import type hints for method signatures and return type annotations.
from typing import Optional, List, Dict, Any
# Import the DatabaseManager for database connection and query execution.
from .database import DatabaseManager


class NoteManager:
    """
    NOTEMANAGER CLASS IS CORE PART OF PLANS NOTE.PY.

    PLANS.note.NoteManager:
        Manages Note entity lifecycle in the PLANS local-first project
        management system. Each Note is a free-form documentation entry
        belonging to a Strack container, persisted in the Notes table with
        title, content, and timestamp fields.

    ATTRIBUTES                         :
        database_manager (DatabaseManager): The database connection manager
            for executing SQL queries and commands against the SQLite database.

    PUBLIC METHODS                     :
        create_note(strack_id, note_id, note_title, note_content="") -> Dict[str, Any]:
            Insert a new Note row into the Notes table and return the created record.
        get_note(note_id) -> Optional[Dict[str, Any]]:
            Retrieve a single Note by its unique identifier from the Notes table.
        list_notes(strack_id=None) -> List[Dict[str, Any]]:
            List all Notes optionally filtered by the parent Strack container.
        update_note(note_id, **kwargs) -> Dict[str, Any]:
            Update the Title or Content fields of an existing Note and return it.
        delete_note(note_id) -> bool:
            Remove a Note row from the Notes table by its unique identifier.

    PRIVATE METHODS                    :
        _init_generate_timestamp_function_() -> str:
            Generate the current UTC timestamp in ISO 8601 string format.

    USAGE                             :
        note_manager = NoteManager(database_manager)
        note = note_manager.create_note("s-1", "n-1", "Meeting Notes",
                                        "Discussed Q3 milestones.")
        all_notes = note_manager.list_notes(strack_id="s-1")
        updated = note_manager.update_note("n-1", Title="New Title")
        was_deleted = note_manager.delete_note("n-1")

    WARNING                           :
        Private methods should not be called from outside the class.
    """

    def __init__(self, database_manager: DatabaseManager):
        """
        Initialize the NoteManager with a database connection manager.

        Stores the DatabaseManager reference for executing SQL operations
        against the Notes table throughout the Note entity lifecycle.

        The parameters are as follows:

        :param database_manager: The database connection manager providing
            SQL execution methods for CRUD operations on the Notes table.
        :type database_manager: DatabaseManager
        """
        # Store the database manager reference for subsequent CRUD operations.
        self.database_manager = database_manager

    def create_note(self, strack_id, note_id, note_title, note_content=""):
        """
        Insert a new Note into the Notes table and return the created record.

        Generates a UTC timestamp for both CreatedAt and UpdatedAt fields,
        then inserts a new row and returns the full Note record as a
        dictionary with PascalCase keys.

        The parameters are as follows:

        :param strack_id: The unique identifier of the parent Strack container.
        :type strack_id: str
        :param note_id: The unique identifier for the new Note entity.
        :type note_id: str
        :param note_title: The human-readable title of the Note.
        :type note_title: str
        :param note_content: The free-form text content of the Note, defaults
            to an empty string.
        :type note_content: str
        :return: The newly created Note record as a dictionary with PascalCase keys.
        :rtype: Dict[str, Any]
        :raise AttributeError: When the database manager is not properly initialized.
        :raise TypeError: When any parameter has an unexpected type.
        :raise ValueError: When the SQL operation fails due to invalid values.
        :raise Exception: When any other unexpected database error occurs.
        """
        # Generate the current UTC timestamp for creation and update fields.
        current_time = self._init_generate_timestamp_function_()
        # Build the INSERT SQL command for the Notes table with parameter placeholders.
        command_sql = "INSERT INTO Notes (Id, StrackId, Title, Content, CreatedAt, UpdatedAt) "
        command_sql += "VALUES (?, ?, ?, ?, ?, ?)"
        # Attempt to execute the INSERT command with all Note field values.
        try:
            # Execute the parameterized INSERT command against the database.
            self.database_manager.execute(
                command_sql,
                (note_id, strack_id, note_title, note_content, current_time, current_time),
            )
            # Commit the transaction to persist the new Note record.
            self.database_manager.connection.commit()
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法创建笔记: "
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 创建笔记时参数类型错误: "
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 创建笔记时数据值无效: "
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 创建笔记时发生未知错误，具体查看: "
            message_error += str(exception_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Construct the Note record dictionary with PascalCase keys per CLASP 4.2.
        note_record = {
            "Id": note_id,
            "StrackId": strack_id,
            "Title": note_title,
            "Content": note_content,
            "CreatedAt": current_time,
            "UpdatedAt": current_time,
        }
        # Return the newly created Note record to the caller.
        return note_record

    def get_note(self, note_id):
        """
        Retrieve a single Note by its unique identifier from the Notes table.

        Queries the Notes table for a row matching the given identifier and
        returns it as a dictionary with PascalCase keys, or None if no match
        is found.

        The parameters are as follows:

        :param note_id: The unique identifier of the Note to retrieve.
        :type note_id: str
        :return: The matching Note record dictionary or None if not found.
        :rtype: Optional[Dict[str, Any]]
        :raise AttributeError: When the database manager is not properly initialized.
        :raise TypeError: When the note identifier has an unexpected type.
        :raise ValueError: When the SQL query fails due to invalid values.
        :raise Exception: When any other unexpected database error occurs.
        """
        # Build the SELECT query for retrieving a Note by its identifier.
        query_sql = "SELECT Id, StrackId, Title, Content, CreatedAt, UpdatedAt "
        query_sql += "FROM Notes WHERE Id = ?"
        # Attempt to execute the SELECT query against the database.
        try:
            # Fetch a single row matching the Note identifier from the database.
            result_row = self.database_manager.fetchone(query_sql, (note_id,))
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法获取笔记: "
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 获取笔记时参数类型错误: "
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 获取笔记时查询参数无效: "
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 获取笔记时发生未知错误，具体查看: "
            message_error += str(exception_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Return None early if no matching Note row was found in the database.
        if result_row is None:
            # Exit early with None to indicate the Note was not found.
            return None
        # Convert the database row into a dictionary with PascalCase column keys.
        note_record = {
            "Id": result_row["Id"],
            "StrackId": result_row["StrackId"],
            "Title": result_row["Title"],
            "Content": result_row["Content"],
            "CreatedAt": result_row["CreatedAt"],
            "UpdatedAt": result_row["UpdatedAt"],
        }
        # Return the Note record dictionary to the caller.
        return note_record

    def list_notes(self, strack_id=None):
        """
        List all Notes optionally filtered by the parent Strack container.

        Queries the Notes table, optionally filtering by a Strack identifier,
        and returns a list of Note record dictionaries with PascalCase keys.

        The parameters are as follows:

        :param strack_id: The optional parent Strack identifier to filter by.
            When None, all Notes across all Stracks are returned.
        :type strack_id: Optional[str]
        :return: A list of Note record dictionaries matching the filter criteria.
        :rtype: List[Dict[str, Any]]
        :raise AttributeError: When the database manager is not properly initialized.
        :raise TypeError: When the filter parameter has an unexpected type.
        :raise ValueError: When the SQL query fails due to invalid values.
        :raise Exception: When any other unexpected database error occurs.
        """
        # Attempt to query the Notes table with optional StrackId filtering.
        try:
            # Determine whether to filter by a specific Strack container or fetch all.
            if strack_id is None:
                # Build the SELECT query for retrieving all Note rows without filtering.
                query_sql = "SELECT Id, StrackId, Title, Content, CreatedAt, UpdatedAt "
                query_sql += "FROM Notes"
                # Fetch all Note rows from the database without a StrackId filter.
                result_rows = self.database_manager.fetchall(query_sql)
            else:
                # Build the SELECT query for retrieving Notes filtered by StrackId.
                query_sql = "SELECT Id, StrackId, Title, Content, CreatedAt, UpdatedAt "
                query_sql += "FROM Notes WHERE StrackId = ?"
                # Fetch Note rows matching the StrackId filter from the database.
                result_rows = self.database_manager.fetchall(query_sql, (strack_id,))
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法列出笔记: "
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 列出笔记时参数类型错误: "
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 列出笔记时查询参数无效: "
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 列出笔记时发生未知错误，具体查看: "
            message_error += str(exception_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Initialize the result list for accumulating Note record dictionaries.
        result_list = []
        # Convert each fetched database row into a Note dictionary with PascalCase keys.
        for note_row in result_rows:
            # Build the Note record dictionary from the current database row.
            note_record = {
                "Id": note_row["Id"],
                "StrackId": note_row["StrackId"],
                "Title": note_row["Title"],
                "Content": note_row["Content"],
                "CreatedAt": note_row["CreatedAt"],
                "UpdatedAt": note_row["UpdatedAt"],
            }
            # Append the constructed Note record to the result list.
            result_list.append(note_record)
        # Return the list of Note record dictionaries to the caller.
        return result_list

    def update_note(self, note_id, **kwargs):
        """
        Update the Title or Content fields of an existing Note and return it.

        Accepts keyword arguments for Title and Content with PascalCase keys,
        sets the UpdatedAt timestamp to the current UTC time, executes the
        UPDATE command, and returns the refreshed Note record.

        The parameters are as follows:

        :param note_id: The unique identifier of the Note to update.
        :type note_id: str
        :param kwargs: Keyword arguments specifying fields to update.
            Supported keys are Title (str) and Content (str).
        :return: The updated Note record dictionary after the modification.
        :rtype: Dict[str, Any]
        :raise AttributeError: When the database manager is not properly initialized.
        :raise TypeError: When any parameter has an unexpected type.
        :raise ValueError: When the SQL operation fails due to invalid values.
        :raise Exception: When any other unexpected database error occurs.
        """
        # Generate the current UTC timestamp for the UpdatedAt field.
        current_time = self._init_generate_timestamp_function_()
        # Extract the update field names from the keyword arguments for the SET clause.
        keys_update = list(kwargs.keys())
        # Build the comma-separated column assignment expressions with placeholders.
        set_clause = ", ".join(f"{key} = ?" for key in keys_update)
        # Append the UpdatedAt column assignment to the SET clause.
        set_clause += ", UpdatedAt = ?"
        # Build the complete UPDATE SQL command with the dynamic SET clause.
        command_sql = "UPDATE Notes SET "
        command_sql += set_clause
        command_sql += " WHERE Id = ?"
        # Collect the new field values in order matching the SET clause placeholders.
        parameters_update = [kwargs[key] for key in keys_update]
        # Append the current timestamp as the UpdatedAt parameter value.
        parameters_update.append(current_time)
        # Append the note identifier for the WHERE clause condition.
        parameters_update.append(note_id)
        # Attempt to execute the UPDATE command against the database.
        try:
            # Execute the parameterized UPDATE command with all field values.
            self.database_manager.execute(command_sql, tuple(parameters_update))
            # Commit the transaction to persist the updated Note record.
            self.database_manager.connection.commit()
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法更新笔记: "
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 更新笔记时参数类型错误: "
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 更新笔记时数据值无效: "
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 更新笔记时发生未知错误，具体查看: "
            message_error += str(exception_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Retrieve the updated Note record to return to the caller.
        note_record = self.get_note(note_id)
        # Return the updated Note record dictionary.
        return note_record

    def delete_note(self, note_id):
        """
        Remove a Note row from the Notes table by its unique identifier.

        Executes a DELETE command targeting the specified Note identifier
        and returns True if a row was actually removed, False otherwise.

        The parameters are as follows:

        :param note_id: The unique identifier of the Note to delete.
        :type note_id: str
        :return: True if the Note was found and deleted, False otherwise.
        :rtype: bool
        :raise AttributeError: When the database manager is not properly initialized.
        :raise TypeError: When the note identifier has an unexpected type.
        :raise ValueError: When the SQL operation fails due to invalid values.
        :raise Exception: When any other unexpected database error occurs.
        """
        # Build the DELETE SQL command for removing a Note by its identifier.
        command_sql = "DELETE FROM Notes WHERE Id = ?"
        # Attempt to execute the DELETE command against the database.
        try:
            # Execute the parameterized DELETE command to remove the Note row.
            cursor_object = self.database_manager.execute(command_sql, (note_id,))
            # Commit the transaction to persist the deletion.
            self.database_manager.connection.commit()
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法删除笔记: "
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 删除笔记时参数类型错误: "
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 删除笔记时数据值无效: "
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 删除笔记时发生未知错误，具体查看: "
            message_error += str(exception_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Determine whether a row was actually deleted by checking the row count.
        is_deleted = cursor_object.rowcount > 0
        # Return the deletion boolean status to the caller.
        return is_deleted

    def _init_generate_timestamp_function_(self):
        """
        Generate the current UTC timestamp in ISO 8601 string format.

        Uses the datetime module to obtain the current time in UTC and
        formats it as an ISO 8601 compliant string for database storage.
        """
        # Obtain the current datetime in the UTC timezone.
        current_time = datetime.now(timezone.utc)
        # Convert the datetime object to an ISO 8601 formatted string.
        time_string = current_time.isoformat()
        # Return the formatted timestamp string to the caller.
        return time_string
