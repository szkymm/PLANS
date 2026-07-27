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
    from PLANS import NoteManager

    note_manager = NoteManager(database_manager)
    note = note_manager.insert_note_record("strack-1", "note-1", "Meeting Notes",
                                           "Discussed Q3 roadmap milestones.")
    existing = note_manager.retrieve_note("note-1")
    all_notes = note_manager.list_notes(strack_id="strack-1")
    updated = note_manager.modify_note_fields("note-1", Title="Revised Title")
    was_deleted = note_manager.erase_note_record("note-1")

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
__version__ = "0.1.2"

# Import the datetime class for generating ISO 8601 UTC timestamps.
from datetime import datetime, timezone
# Import type hints for method signatures and return type annotations.
from typing import Optional, List, Dict, Any
# Import the DatabaseManager for database connection and query execution.
from .database import DatabaseManager


class NoteManager:
    """
    NoteManager CLASS IS CORE PART OF PLANS note.py.

    PLANS.note.NoteManager:
        Manages Note entity lifecycle in the PLANS local-first project
        management system. Each Note is a free-form documentation entry
        belonging to a Strack container, persisted in the Notes table with
        title, content, and timestamp fields.

    ATTRIBUTES                         :
        database_manager (DatabaseManager): The database connection manager
            for executing SQL queries and commands against the SQLite database.

    PUBLIC METHODS                     :
        insert_note_record(strack_id, note_id, note_title, note_content="") -> Dict[str, Any]:
            Insert a new Note row into the Notes table and return the created record.
        retrieve_note(note_id) -> Optional[Dict[str, Any]]:
            Retrieve a single Note by its unique identifier from the Notes table.
        list_notes(strack_id=None) -> List[Dict[str, Any]]:
            List all Notes optionally filtered by the parent Strack container.
        modify_note_fields(note_id, **update_kwargs) -> Dict[str, Any]:
            Update the Title or Content fields of an existing Note and return it.
        erase_note_record(note_id) -> bool:
            Remove a Note row from the Notes table by its unique identifier.

    PRIVATE METHODS                    :
        _init_form_timestamp_function_() -> str:
            Generate the current UTC timestamp in ISO 8601 string format.

    USAGE                             :
        note_manager = NoteManager(database_manager)
        note = note_manager.insert_note_record("s-1", "n-1", "Meeting Notes",
                                                "Discussed Q3 milestones.")
        all_notes = note_manager.list_notes(strack_id="s-1")
        updated = note_manager.modify_note_fields("n-1", Title="New Title")
        was_deleted = note_manager.erase_note_record("n-1")

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

    def insert_note_record(self, strack_id, note_id, note_title, note_content=""):
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
        current_time = self._init_form_timestamp_function_()
        # Build the INSERT SQL command for the Notes table with parameter placeholders.
        command_sql = "INSERT INTO Notes (Id, StrackId, Title, Content, CreatedAt, UpdatedAt) "
        # Append the VALUES clause with parameter placeholders for all Note fields.
        command_sql += "VALUES (?, ?, ?, ?, ?, ?)"
        # Attempt to execute the INSERT command with all Note field values.
        try:
            # Execute the parameterized INSERT command against the database.
            self.database_manager.run_sql_statement(
                # Pass the assembled SQL command string as the first argument.
                command_sql,
                # Pass the tuple of parameter values corresponding to the placeholders.
                (note_id, strack_id, note_title, note_content, current_time, current_time),
            )
            # Commit the transaction to persist the new Note record.
            self.database_manager.connection.commit()
        # Catch attribute errors due to improper database init for insertion.
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法创建笔记: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        # Catch type errors from the database manager when insert parameters have unexpected types.
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 创建笔记时参数类型错误: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        # Catch value errors when the SQL operation fails due to invalid values during insertion.
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 创建笔记时数据值无效: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        # Catch all other unexpected database errors during insertion as a fallback.
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 创建笔记时发生未知错误，具体查看: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(exception_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Construct the Note record dictionary with PascalCase keys per CLASP 4.2.
        note_record = {
            # Map the unique Note identifier with PascalCase key per CLASP.
            "ID": note_id,
            # Map the parent Strack identifier with PascalCase key.
            "StrackID": strack_id,
            # Map the Note title with PascalCase key.
            "Title": note_title,
            # Map the Note content with PascalCase key.
            "Content": note_content,
            # Map the creation timestamp with PascalCase key.
            "CreatedAt": current_time,
            # Map the last update timestamp with PascalCase key.
            "UpdatedAt": current_time,
        }
        # Return the newly created Note record to the caller.
        return note_record

    def retrieve_note(self, note_id):
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
        # Append the FROM clause with a parameterized WHERE condition for a single Note lookup.
        query_sql += "FROM Notes WHERE Id = ?"
        # Attempt to execute the SELECT query against the database.
        try:
            # Fetch a single row matching the Note identifier from the database.
            result_row = self.database_manager.fetchone(query_sql, (note_id,))
        # Catch attribute errors due to improper database init for retrieval.
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法获取笔记: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        # Catch type errors due to an unexpected type for the note identifier.
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 获取笔记时参数类型错误: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        # Catch value errors when the SQL query fails due to invalid values during retrieval.
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 获取笔记时查询参数无效: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        # Catch all other unexpected database errors during retrieval as a fallback.
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 获取笔记时发生未知错误，具体查看: "
            # Append the exception details to the error message for diagnostics.
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
            # Map the Note identifier column with PascalCase key per CLASP.
            "ID": result_row["Id"],
            # Map the parent Strack identifier column with PascalCase key.
            "StrackID": result_row["StrackId"],
            # Map the Note title column with PascalCase key.
            "Title": result_row["Title"],
            # Map the Note content column with PascalCase key.
            "Content": result_row["Content"],
            # Map the creation timestamp column with PascalCase key.
            "CreatedAt": result_row["CreatedAt"],
            # Map the last update timestamp column with PascalCase key.
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
                # Append the FROM clause to complete the SELECT query for all Notes.
                query_sql += "FROM Notes"
                # Fetch all Note rows from the database without a StrackId filter.
                result_records = self.database_manager.fetchall(query_sql)
            # Handle the case where a StrackId filter is provided for scoped retrieval.
            else:
                # Build the SELECT query for retrieving Notes filtered by StrackId.
                query_sql = "SELECT Id, StrackId, Title, Content, CreatedAt, UpdatedAt "
                # Append FROM clause with parameterized WHERE for StrackId filtering.
                query_sql += "FROM Notes WHERE StrackId = ?"
                # Fetch Note rows matching the StrackId filter from the database.
                result_records = self.database_manager.fetchall(query_sql, (strack_id,))
        # Catch attribute errors when the database manager is not properly initialized for listing.
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法列出笔记: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        # Catch type errors from the database manager when listing parameters have unexpected types.
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 列出笔记时参数类型错误: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        # Catch value errors when the SQL query fails due to invalid values during listing.
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 列出笔记时查询参数无效: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        # Catch all other unexpected database errors during listing as a fallback.
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 列出笔记时发生未知错误，具体查看: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(exception_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Initialize the result list for accumulating Note record dictionaries.
        result_list = []
        # Convert each fetched database row into a Note dictionary with PascalCase keys.
        for note_row in result_records:
            # Build the Note record dictionary from the current database row.
            note_record = {
                # Map the Note identifier column with PascalCase key per CLASP.
                "ID": note_row["Id"],
                # Map the parent Strack identifier column with PascalCase key.
                "StrackID": note_row["StrackId"],
                # Map the Note title column with PascalCase key.
                "Title": note_row["Title"],
                # Map the Note content column with PascalCase key.
                "Content": note_row["Content"],
                # Map the creation timestamp column with PascalCase key.
                "CreatedAt": note_row["CreatedAt"],
                # Map the last update timestamp column with PascalCase key.
                "UpdatedAt": note_row["UpdatedAt"],
            }
            # Append the constructed Note record to the result list.
            result_list.append(note_record)
        # Return the list of Note record dictionaries to the caller.
        return result_list

    def modify_note_fields(self, note_id, **update_kwargs):
        """
        Update the Title or Content fields of an existing Note and return it.

        Accepts keyword arguments for Title and Content with PascalCase keys,
        sets the UpdatedAt timestamp to the current UTC time, executes the
        UPDATE command, and returns the refreshed Note record.

        The parameters are as follows:

        :param note_id: The unique identifier of the Note to update.
        :type note_id: str
        :param update_kwargs: Keyword arguments specifying fields to update.
            Supported keys are Title (str) and Content (str).
        :type update_kwargs: Dict[str, Any]
        :return: The updated Note record dictionary after the modification.
        :rtype: Dict[str, Any]
        :raise AttributeError: When the database manager is not properly initialized.
        :raise TypeError: When any parameter has an unexpected type.
        :raise ValueError: When the SQL operation fails due to invalid values.
        :raise Exception: When any other unexpected database error occurs.
        """
        # Generate the current UTC timestamp for the UpdatedAt field.
        current_time = self._init_form_timestamp_function_()
        # Extract the update field names from the keyword arguments for the SET clause.
        keys_update = list(update_kwargs.keys())
        # Build the comma-separated column assignment expressions with placeholders.
        set_clause = ", ".join(f"{key} = ?" for key in keys_update)
        # Append the UpdatedAt column assignment to the SET clause.
        set_clause += ", UpdatedAt = ?"
        # Build the complete UPDATE SQL command with the dynamic SET clause.
        command_sql = "UPDATE Notes SET "
        # Append the dynamic SET clause containing column assignments to the UPDATE command.
        command_sql += set_clause
        # Append the WHERE clause to target the specific Note row by its identifier.
        command_sql += " WHERE Id = ?"
        # Collect the new field values in order matching the SET clause placeholders.
        parameters_update = [update_kwargs[key] for key in keys_update]
        # Append the current timestamp as the UpdatedAt parameter value.
        parameters_update.append(current_time)
        # Append the note identifier for the WHERE clause condition.
        parameters_update.append(note_id)
        # Attempt to execute the UPDATE command against the database.
        try:
            # Execute the parameterized UPDATE command with all field values.
            self.database_manager.run_sql_statement(command_sql, tuple(parameters_update))
            # Commit the transaction to persist the updated Note record.
            self.database_manager.connection.commit()
        # Catch attribute errors when the database manager is not properly initialized for update.
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法更新笔记: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        # Catch type errors due to unexpected types in the update parameters.
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 更新笔记时参数类型错误: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        # Catch value errors when the SQL operation fails due to invalid values during update.
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 更新笔记时数据值无效: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        # Catch all other unexpected database errors during update as a fallback.
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 更新笔记时发生未知错误，具体查看: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(exception_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Retrieve the updated Note record to return to the caller.
        note_record = self.retrieve_note(note_id)
        # Return the updated Note record dictionary.
        return note_record

    def erase_note_record(self, note_id):
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
            cursor_object = self.database_manager.run_sql_statement(command_sql, (note_id,))
            # Commit the transaction to persist the deletion.
            self.database_manager.connection.commit()
        # Catch attribute errors when the database manager is not properly initialized for deletion.
        except AttributeError as attribute_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (AttributeError) 数据库管理器未正确初始化，无法删除笔记: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(attribute_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise AttributeError(message_error) from attribute_error
        # Catch type errors due to an unexpected type for the note identifier.
        except TypeError as type_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (TypeError) 删除笔记时参数类型错误: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(type_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise TypeError(message_error) from type_error
        # Catch value errors when the SQL operation fails due to invalid values during deletion.
        except ValueError as value_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (ValueError) 删除笔记时数据值无效: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(value_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise ValueError(message_error) from value_error
        # Catch all other unexpected database errors during deletion as a fallback.
        except Exception as exception_error:
            # Build the error message for unanticipated errors in Chinese.
            message_error = "[X] (OtherError) 删除笔记时发生未知错误，具体查看: "
            # Append the exception details to the error message for diagnostics.
            message_error += str(exception_error)
            # Output the error message for diagnostics since no logger is available.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
        # Determine whether a row was actually deleted by checking the row count.
        is_deleted = cursor_object.rowcount > 0
        # Return the deletion boolean status to the caller.
        return is_deleted

    def _init_form_timestamp_function_(self):
        """
        Generate the current UTC timestamp in ISO 8601 string format.

        Uses the datetime module to obtain the current time in UTC and
        formats it as an ISO 8601 compliant string for database storage.

        :return: The current UTC timestamp as an ISO 8601 formatted string.
        :rtype: str
        """
        # Obtain the current datetime in the UTC timezone.
        current_time = datetime.now(timezone.utc)
        # Convert the datetime object to an ISO 8601 formatted string.
        time_string = current_time.isoformat()
        # Return the formatted timestamp string to the caller.
        return time_string
