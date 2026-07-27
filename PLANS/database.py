# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================

MODULE               : PLANS.database

TYPE                 : Python Script

DESCRIPTION          :
    SQLite database connection management, schema initialization, and
    base CRUD operations for the PLANS local-first project management system.

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
    from PLANS.database import DatabaseManager
    database = DatabaseManager("path/to/plans.db")
    database.initialize_schema()

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

import sqlite3

import os

from datetime import datetime, timezone

# Define the module version synchronized with the project version in the docstring.
__version__ = "0.1.2"


class DatabaseManager:
    """
    DatabaseManager CLASS IS CORE PART OF PLANS DATABASE.PY.

    PLANS.database.DatabaseManager:
        Manages SQLite database connections, schema initialization, and provides
        the foundational data access layer for the PLANS project management system.

    ATTRIBUTES                         :
        database_path (str): Absolute or relative filesystem path to the SQLite database file.
        database_connection (sqlite3.Connection or None): Active
            SQLite connection object or None when closed.

    PUBLIC METHODS                     :
        __init__(database_path: str) -> None:
            Initialize the database manager with a configurable file path.
        initialize_schema() -> None:
            Open the database, create all five entity tables, and close the connection.
        run_sql_statement(sql_statement: str, query_parameters: Optional[tuple]) -> sqlite3.Cursor:
            Execute a SQL statement with optional parameters via the database connection.
        insert_record(table_name: str, record_data: dict) -> int:
            Insert a row into the specified table using a dictionary of column values.
        modify_table_record(table_name: str, record_data: dict, where_condition: str) -> None:
            Update rows in a table matching the given WHERE condition.
        purge_table_record(table_name: str, where_condition: str) -> int:
            Delete rows from a table matching the given WHERE condition.
        fetchone(sql_statement: str, query_parameters: Optional[tuple]) -> Optional[tuple]:
            Execute a query and return the first matching row.
        fetchall(sql_statement: str, query_parameters: Optional[tuple]) -> list:
            Execute a query and return all matching rows as a list of tuples.
        select_records(table_name: str, filter_condition: Union[dict, str]) -> list:
            Select rows from a table matching the given filter.

    PRIVATE METHODS                    :
        _init_open_link_function_() -> None:
            Open or create the SQLite database and enable WAL mode with foreign keys.
        _init_close_link_function_() -> None:
            Close the active database connection and reset the attribute to None.
        _init_create_tables_function_() -> None:
            Execute all CREATE TABLE statements for the five entity tables.

    USAGE                             :
        from PLANS.database import DatabaseManager
        database = DatabaseManager("path/to/plans.db")
        database.initialize_schema()

    WARNING                           :
        Private methods should not be called from outside the class.
    """

    def __init__(self, database_path="plans.db"):
        """
        Initialize the database manager with a configurable file path.

        Stores the database path for later connection use and sets the
        connection attribute to None before any connection is opened.

        The parameters are as follows:

        :param database_path: Filesystem path to the SQLite database file.
        :type database_path: str
        """
        # Store the database path for later connection use.
        self.database_path = database_path
        # Initialize the connection attribute to None before any connection opens.
        self.database_connection = None

    @property
    def connection(self):
        """
        Return the active database connection, opening it if necessary.

        Provides lazy-on-demand access to the SQLite connection so that
        entity managers can transparently obtain a working connection
        without manually managing the open/close lifecycle.

        :return: The active sqlite3.Connection object.
        :rtype: sqlite3.Connection
        """
        # Open the connection if it has not been established yet.
        if self.database_connection is None:
            # Establish the database connection via the private opener method.
            self._init_open_link_function_()
        # Return the active database connection reference.
        return self.database_connection

    def _init_open_link_function_(self):
        """
        Open or create the SQLite database connection.

        Establishes a connection to the SQLite database at the configured path,
        enables foreign key constraint enforcement, and activates WAL journaling
        mode for improved concurrent read performance.
        """
        # Open or create the SQLite database at the configured file path.
        self.database_connection = sqlite3.connect(self.database_path)
        # Enable foreign key constraint enforcement for referential integrity.
        self.database_connection.execute("PRAGMA foreign_keys = ON")
        # Enable Write-Ahead Logging mode for concurrent read performance.
        self.database_connection.execute("PRAGMA journal_mode = WAL")
        # Configure rows to be accessible by column name for readability.
        self.database_connection.row_factory = sqlite3.Row

    def _init_close_link_function_(self):
        """
        Close the active database connection gracefully.

        Checks whether a connection is currently open and closes it, then
        resets the connection attribute to None for safety.
        """
        # Verify a connection exists before attempting to close it.
        if self.database_connection is not None:
            # Close the active database connection to release resources.
            self.database_connection.close()
            # Reset the connection attribute to None for safety.
            self.database_connection = None

    def run_sql_statement(self, sql_statement, query_parameters=None):
        """
        Execute a SQL statement with optional parameters via the database connection.

        Provides a unified execution interface so that entity managers can run
        SQL without directly accessing the underlying connection object.

        The parameters are as follows:

        :param sql_statement: The SQL statement string to execute.
        :type sql_statement: str
        :param query_parameters: Optional tuple or dict of parameter bindings.
        :type query_parameters: Optional[tuple]
        :return: The cursor object after executing the statement.
        :rtype: sqlite3.Cursor
        """
        # Obtain the active database connection through the property accessor.
        database_connection = self.connection
        # Execute with parameter bindings when parameters are provided.
        if query_parameters is not None:
            # Bind parameters to the statement and execute against the database.
            return database_connection.execute(sql_statement, query_parameters)
        # Execute the statement without parameter bindings for DDL or simple queries.
        return database_connection.execute(sql_statement)

    def insert_record(self, table_name, record_data):
        """
        Insert a row into the specified table using a dictionary of column values.

        Generates an INSERT statement from the dictionary keys and values,
        executes it, and commits the transaction.

        The parameters are as follows:

        :param table_name: The target table name for the insert operation.
        :type table_name: str
        :param record_data: Dictionary mapping PascalCase column names to values.
        :type record_data: dict
        :return: The last inserted row identifier.
        :rtype: int
        """
        # Collect the column names from the record data dictionary keys.
        list_columns = list(record_data.keys())
        # Build the comma-separated column name string for the SQL statement.
        string_columns = ", ".join(list_columns)
        # Build the placeholder string with one question mark per column.
        string_placeholders = ", ".join(["?" for _ in list_columns])
        # Collect the values in matching column order for parameter binding.
        list_values = [record_data[col] for col in list_columns]
        # Build the full INSERT statement with column names and placeholders.
        string_sql = "INSERT INTO "
        # Append the target table name to the INSERT prefix.
        string_sql += table_name
        # Append the opening parenthesis and column list for the INSERT.
        string_sql += " ("
        # Append the comma-separated column name string for the INSERT.
        string_sql += string_columns
        # Append the closing parenthesis and VALUES keyword with opening parenthesis.
        string_sql += ") VALUES ("
        # Append the comma-separated placeholder string for parameter binding.
        string_sql += string_placeholders
        # Append the closing parenthesis to complete the INSERT statement.
        string_sql += ")"
        # Execute the insert statement via the unified run_sql_statement method.
        self.run_sql_statement(string_sql, tuple(list_values))
        # Commit the transaction to persist the inserted row.
        self.connection.commit()

    def modify_table_record(self, table_name, record_data, where_condition):
        """
        Update rows in a table matching the given WHERE condition.

        Builds an UPDATE statement from the record data dictionary and the
        WHERE condition string, executes it, and commits the transaction.

        The parameters are as follows:

        :param table_name: The target table name for the update operation.
        :type table_name: str
        :param record_data: Dictionary mapping PascalCase column names to new values.
        :type record_data: dict
        :param where_condition: The raw SQL WHERE clause string identifying target rows.
        :type where_condition: str
        """
        # Collect the column names from the record data dictionary keys.
        list_columns = list(record_data.keys())
        # Build the SET clause with placeholders for parameterized binding.
        list_setclauses = [f"{col} = ?" for col in list_columns]
        # Combine the SET clauses into a comma-separated string.
        string_set = ", ".join(list_setclauses)
        # Collect the new values in column order for parameter binding.
        list_values = [record_data[col] for col in list_columns]
        # Build the full UPDATE statement with SET and WHERE clauses.
        string_sql = "UPDATE "
        # Append the target table name to the UPDATE prefix.
        string_sql += table_name
        # Append the SET keyword for the update clause.
        string_sql += " SET "
        # Append the comma-separated column assignment string.
        string_sql += string_set
        # Append the WHERE keyword for the filter clause.
        string_sql += " WHERE "
        # Append the WHERE condition string to identify target rows.
        string_sql += where_condition
        # Execute the UPDATE statement with the assembled parameters.
        self.run_sql_statement(string_sql, tuple(list_values))
        # Commit the transaction to persist the updated row.
        self.connection.commit()

    def purge_table_record(self, table_name, where_condition):
        """
        Delete rows from a table matching the given WHERE condition.

        Builds a DELETE statement with the WHERE condition string,
        executes it, and commits the transaction.

        The parameters are as follows:

        :param table_name: The target table name for the delete operation.
        :type table_name: str
        :param where_condition: The raw SQL WHERE clause string identifying target rows.
        :type where_condition: str
        :return: The number of rows affected by the delete operation.
        :rtype: int
        """
        # Build the DELETE statement for the target table with WHERE condition.
        string_sql = "DELETE FROM "
        # Append the target table name to the DELETE FROM prefix.
        string_sql += table_name
        # Append the WHERE keyword for the filter clause.
        string_sql += " WHERE "
        # Append the WHERE condition string to identify target rows.
        string_sql += where_condition
        # Execute the DELETE statement against the database.
        cursor_result = self.run_sql_statement(string_sql)
        # Retrieve the number of rows affected by the deletion.
        int_rowcount = cursor_result.rowcount
        # Commit the transaction to persist the deleted rows.
        self.connection.commit()
        # Return the count of affected rows for caller verification.
        return int_rowcount

    def fetchone(self, sql_statement, query_parameters=None):
        """
        Execute a query and return the first matching row.

        Convenience method that executes a SQL SELECT statement and returns
        the first result row as a tuple, or None when no match exists.

        The parameters are as follows:

        :param sql_statement: The SELECT SQL statement string.
        :type sql_statement: str
        :param query_parameters: Optional tuple of parameter bindings.
        :type query_parameters: Optional[tuple]
        :return: The first result row tuple, or None.
        :rtype: Optional[tuple]
        """
        # Execute the query statement via the unified run_sql_statement method.
        cursor_result = self.run_sql_statement(sql_statement, query_parameters)
        # Fetch and return the first row from the result set.
        return cursor_result.fetchone()

    def fetchall(self, sql_statement, query_parameters=None):
        """
        Execute a query and return all matching rows as a list of tuples.

        Convenience method that executes a SQL SELECT statement and returns
        all result rows as a list.

        The parameters are as follows:

        :param sql_statement: The SELECT SQL statement string.
        :type sql_statement: str
        :param query_parameters: Optional tuple of parameter bindings.
        :type query_parameters: Optional[tuple]
        :return: A list of result row tuples.
        :rtype: list
        """
        # Execute the query statement via the unified run_sql_statement method.
        cursor_result = self.run_sql_statement(sql_statement, query_parameters)
        # Fetch and return all rows from the result set as a list.
        return cursor_result.fetchall()

    def select_records(self, table_name, filter_condition):
        """
        Select rows from a table matching the given filter.

        Supports both a dictionary of column-value pairs for parameterized
        queries and a raw SQL WHERE clause string for dynamic filtering.

        The parameters are as follows:

        :param table_name: The target table name for the select operation.
        :type table_name: str
        :param filter_condition: A dict of column-value pairs or a raw WHERE clause string.
        :type filter_condition: Union[dict, str]
        :return: A list of sqlite3.Row objects matching the filter.
        :rtype: list
        """
        # Build the base SELECT statement for the target table.
        string_sql = "SELECT * FROM " + table_name
        # Handle dictionary-based filter with parameterized placeholders.
        if isinstance(filter_condition, dict):
            # Collect filter columns and values for the WHERE clause.
            list_columns = list(filter_condition.keys())
            # Assemble the WHERE clause from the filter dictionary keys.
            list_clauses = [f"{col} = ?" for col in list_columns]
            # Append the WHERE clause to the SQL statement.
            string_sql += " WHERE " + " AND ".join(list_clauses)
            # Collect the filter values in column order.
            list_values = [filter_condition[col] for col in list_columns]
            # Execute the parameterized query with filter values.
            cursor_result = self.run_sql_statement(string_sql, tuple(list_values))
            # Return all rows from the result set.
            return cursor_result.fetchall()
        # Handle string-based filter as a raw WHERE clause.
        if isinstance(filter_condition, str) and filter_condition:
            # Append the raw WHERE clause string to the base statement.
            string_sql += " WHERE " + filter_condition
        # Execute the query without parameter bindings for raw string filters.
        cursor_result = self.run_sql_statement(string_sql)
        # Return all rows from the result set.
        return cursor_result.fetchall()

    def _init_create_tables_function_(self):
        """
        Create all five entity tables in the database schema.

        Executes CREATE TABLE IF NOT EXISTS statements for Stracks, Plans,
        Issues, Actions, and Notes tables with appropriate column definitions,
        constraints, and foreign key relationships.
        """
        # Build the SQL CREATE statement for the Stracks table.
        sql_stracks = "CREATE TABLE IF NOT EXISTS Stracks ("
        # Append the identifier and title column definitions.
        sql_stracks += "Id TEXT PRIMARY KEY, Title TEXT NOT NULL, "
        # Append the description column with an empty default value.
        sql_stracks += "Description TEXT DEFAULT '', "
        # Append the priority column with its data type and default.
        sql_stracks += "Priority INTEGER DEFAULT 3 "
        # Append the CHECK constraint for the allowed priority range.
        sql_stracks += "CHECK(Priority BETWEEN 1 AND 5), "
        # Append the status column with its data type and default.
        sql_stracks += "Status TEXT DEFAULT 'active' "
        # Append the CHECK constraint for allowed status values.
        sql_stracks += "CHECK(Status IN ('active','archived')), "
        # Append the timestamp columns for record tracking.
        sql_stracks += "CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
        # Execute the Stracks table creation statement against the database connection.
        self.database_connection.execute(sql_stracks)
        # Build the SQL CREATE statement for the Plans table.
        sql_plans = "CREATE TABLE IF NOT EXISTS Plans ("
        # Append the identifier and foreign key column definitions.
        sql_plans += "Id TEXT PRIMARY KEY, StrackId TEXT NOT NULL "
        # Append the foreign key reference clause with cascade delete.
        sql_plans += "REFERENCES Stracks(Id) ON DELETE CASCADE, "
        # Append the title column with a NOT NULL constraint.
        sql_plans += "Title TEXT NOT NULL, "
        # Append the description column with an empty default value.
        sql_plans += "Description TEXT DEFAULT '', "
        # Append the status column with its data type and default.
        sql_plans += "Status TEXT DEFAULT 'pending' "
        # Append the CHECK constraint for allowed status values.
        sql_plans += "CHECK(Status IN ('pending','in_progress',"
        # Append the remaining allowed status enumeration values.
        sql_plans += "'done','blocked')), "
        # Append the priority column with its data type and default.
        sql_plans += "Priority INTEGER DEFAULT 3 "
        # Append the CHECK constraint for the allowed priority range.
        sql_plans += "CHECK(Priority BETWEEN 1 AND 5), "
        # Append the timestamp columns for record tracking.
        sql_plans += "CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
        # Execute the Plans table creation statement against the database connection.
        self.database_connection.execute(sql_plans)
        # Build the SQL CREATE statement for the Issues table.
        sql_issues = "CREATE TABLE IF NOT EXISTS Issues ("
        # Append the identifier and foreign key column definitions.
        sql_issues += "Id TEXT PRIMARY KEY, StrackId TEXT NOT NULL "
        # Append the foreign key reference clause with cascade delete.
        sql_issues += "REFERENCES Stracks(Id) ON DELETE CASCADE, "
        # Append the title column with a NOT NULL constraint.
        sql_issues += "Title TEXT NOT NULL, "
        # Append the description column with an empty default value.
        sql_issues += "Description TEXT DEFAULT '', "
        # Append the status column with its data type and default.
        sql_issues += "Status TEXT DEFAULT 'open' "
        # Append the CHECK constraint for allowed status values.
        sql_issues += "CHECK(Status IN ('open','in_progress',"
        # Append the remaining allowed status enumeration values.
        sql_issues += "'resolved','closed')), "
        # Append the severity column with its data type and default.
        sql_issues += "Severity TEXT DEFAULT 'medium' "
        # Append the CHECK constraint for allowed severity values.
        sql_issues += "CHECK(Severity IN ('critical','high',"
        # Append the remaining allowed severity enumeration values.
        sql_issues += "'medium','low')), "
        # Append the timestamp columns for record tracking.
        sql_issues += "CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
        # Execute the Issues table creation statement against the database connection.
        self.database_connection.execute(sql_issues)
        # Build the SQL CREATE statement for the Actions table.
        sql_actions = "CREATE TABLE IF NOT EXISTS Actions ("
        # Append the identifier and foreign key column definitions.
        sql_actions += "Id TEXT PRIMARY KEY, StrackId TEXT NOT NULL "
        # Append the foreign key reference clause with cascade delete.
        sql_actions += "REFERENCES Stracks(Id) ON DELETE CASCADE, "
        # Append the title column with a NOT NULL constraint.
        sql_actions += "Title TEXT NOT NULL, "
        # Append the description column with an empty default value.
        sql_actions += "Description TEXT DEFAULT '', "
        # Append the status column with its data type and default.
        sql_actions += "Status TEXT DEFAULT 'pending' "
        # Append the CHECK constraint for allowed status values.
        sql_actions += "CHECK(Status IN ('pending','in_progress',"
        # Append the remaining allowed status enumeration values.
        sql_actions += "'done','cancelled')), "
        # Append the timestamp columns for record tracking.
        sql_actions += "CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
        # Execute the Actions table creation statement against the database connection.
        self.database_connection.execute(sql_actions)
        # Build the SQL CREATE statement for the Notes table.
        sql_notes = "CREATE TABLE IF NOT EXISTS Notes ("
        # Append the identifier and foreign key column definitions.
        sql_notes += "Id TEXT PRIMARY KEY, StrackId TEXT NOT NULL "
        # Append the foreign key reference clause with cascade delete.
        sql_notes += "REFERENCES Stracks(Id) ON DELETE CASCADE, "
        # Append the title column with a NOT NULL constraint.
        sql_notes += "Title TEXT NOT NULL, "
        # Append the content column with an empty default value.
        sql_notes += "Content TEXT DEFAULT '', "
        # Append the timestamp columns for record tracking.
        sql_notes += "CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
        # Execute the Notes table creation statement against the database connection.
        self.database_connection.execute(sql_notes)
        # Commit all table creation statements to persist the schema changes.
        self.database_connection.commit()

    def initialize_schema(self):
        """
        Initialize the full database schema for the PLANS system.

        Opens the database connection, creates all five entity tables if they
        do not already exist, and closes the connection. Handles operational
        errors and unexpected failures with diagnostic messages.

        The parameters are as follows:

        :raise sqlite3.OperationalError: When the database file cannot be opened or written.
        :raise Exception: When any other unexpected error occurs during initialization.
        """
        # Attempt to open the database connection and create all schema tables.
        try:
            # Open the database connection before schema initialization.
            self._init_open_link_function_()
            # Create all five entity tables in the database schema.
            self._init_create_tables_function_()
        # Handle operational errors such as disk I/O failures or locked database files.
        except sqlite3.OperationalError as exception_error:
            # Build the error message with operational failure context in Chinese.
            message_error = "[X] (OperationalError) 数据库操作失败，无法打开或写入数据库文件"
            # Append the exception detail to the error message for diagnostics.
            message_error += f"，错误详情: {exception_error}"
            # Output the error message for diagnostics since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream error handling.
            raise sqlite3.OperationalError(message_error) from exception_error
        # Handle all other unexpected errors during schema initialization.
        except Exception as exception_error:
            # Build the error message for unanticipated failures in Chinese.
            message_error = "[X] (OtherError) 数据库初始化过程中发生未知错误"
            # Append the exception detail to the error message for diagnostics.
            message_error += f"，具体查看: {exception_error}"
            # Output the error message for diagnostics since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream error handling.
            raise Exception(message_error) from exception_error
        # Ensure the database connection is always closed after initialization.
        finally:
            # Close the database connection regardless of success or failure.
            self._init_close_link_function_()
