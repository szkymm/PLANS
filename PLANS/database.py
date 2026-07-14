# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================

MODULE               : PLANS.database

TYPE                 : Python Script

DESCRIPTION          :
    SQLite database connection management, schema initialization, and
    base CRUD operations for the PLANS local-first project management system.

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
__version__ = "0.1.0"


class DatabaseManager:
    """
    DATABASEMANAGER CLASS IS CORE PART OF PLANS database.

    PLANS.database.DatabaseManager:
        Manages SQLite database connections, schema initialization, and provides
        the foundational data access layer for the PLANS project management system.

    ATTRIBUTES                         :
        database_path (str): Absolute or relative filesystem path to the SQLite database file.
        database_connection (sqlite3.Connection or None): Active SQLite connection object or None when closed.

    PUBLIC METHODS                     :
        __init__(database_path: str) -> None:
            Initialize the database manager with a configurable file path.
        initialize_schema() -> None:
            Open the database, create all five entity tables, and close the connection.

    PRIVATE METHODS                    :
        _init_open_connection_function_() -> None:
            Open or create the SQLite database and enable WAL mode with foreign keys.
        _init_close_connection_function_() -> None:
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
            self._init_open_connection_function_()
        # Return the active database connection reference.
        return self.database_connection

    def _init_open_connection_function_(self):
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

    def _init_close_connection_function_(self):
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

    def execute(self, sql_statement, parameters=None):
        """
        Execute a SQL statement with optional parameters via the database connection.

        Provides a unified execution interface so that entity managers can run
        SQL without directly accessing the underlying connection object.

        The parameters are as follows:

        :param sql_statement: The SQL statement string to execute.
        :type sql_statement: str
        :param parameters: Optional tuple or dict of parameter bindings.
        :type parameters: Optional[tuple]
        :return: The cursor object after executing the statement.
        :rtype: sqlite3.Cursor
        """
        # Obtain the active database connection through the property accessor.
        database_connection = self.connection
        # Execute with parameter bindings when parameters are provided.
        if parameters is not None:
            # Bind parameters to the statement and execute against the database.
            return database_connection.execute(sql_statement, parameters)
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
        string_sql += table_name
        string_sql += " ("
        string_sql += string_columns
        string_sql += ") VALUES ("
        string_sql += string_placeholders
        string_sql += ")"
        # Execute the insert statement via the unified execute method.
        self.execute(string_sql, tuple(list_values))
        # Commit the transaction to persist the inserted row.
        self.connection.commit()

    def update_record(self, table_name, record_data, where_condition):
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
        list_set_parts = [f"{col} = ?" for col in list_columns]
        # Combine the SET clauses into a comma-separated string.
        string_set = ", ".join(list_set_parts)
        # Collect the new values in column order for parameter binding.
        list_values = [record_data[col] for col in list_columns]
        # Build the full UPDATE statement with SET and WHERE clauses.
        string_sql = "UPDATE "
        string_sql += table_name
        string_sql += " SET "
        string_sql += string_set
        string_sql += " WHERE "
        string_sql += where_condition
        # Execute the UPDATE statement with the assembled parameters.
        self.execute(string_sql, tuple(list_values))
        # Commit the transaction to persist the updated row.
        self.connection.commit()

    def fetchone(self, sql_statement, parameters=None):
        """
        Execute a query and return the first matching row.

        Convenience method that executes a SQL SELECT statement and returns
        the first result row as a tuple, or None when no match exists.

        The parameters are as follows:

        :param sql_statement: The SELECT SQL statement string.
        :type sql_statement: str
        :param parameters: Optional tuple of parameter bindings.
        :type parameters: Optional[tuple]
        :return: The first result row tuple, or None.
        :rtype: Optional[tuple]
        """
        # Execute the query statement via the unified execute method.
        cursor_result = self.execute(sql_statement, parameters)
        # Fetch and return the first row from the result set.
        return cursor_result.fetchone()

    def fetchall(self, sql_statement, parameters=None):
        """
        Execute a query and return all matching rows as a list of tuples.

        Convenience method that executes a SQL SELECT statement and returns
        all result rows as a list.

        The parameters are as follows:

        :param sql_statement: The SELECT SQL statement string.
        :type sql_statement: str
        :param parameters: Optional tuple of parameter bindings.
        :type parameters: Optional[tuple]
        :return: A list of result row tuples.
        :rtype: list
        """
        # Execute the query statement via the unified execute method.
        cursor_result = self.execute(sql_statement, parameters)
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
            cursor_result = self.execute(string_sql, tuple(list_values))
            # Return all rows from the result set.
            return cursor_result.fetchall()
        # Handle string-based filter as a raw WHERE clause.
        if isinstance(filter_condition, str) and filter_condition:
            # Append the raw WHERE clause string to the base statement.
            string_sql += " WHERE " + filter_condition
        # Execute the query without parameter bindings for raw string filters.
        cursor_result = self.execute(string_sql)
        # Return all rows from the result set.
        return cursor_result.fetchall()

    def _init_create_tables_function_(self):
        """
        Create all five entity tables in the database schema.

        Executes CREATE TABLE IF NOT EXISTS statements for Stracks, Plans,
        Issues, Actions, and Notes tables with appropriate column definitions,
        constraints, and foreign key relationships.
        """
        # Define the SQL to create the Stracks strategic tracks table with full schema constraints.
        sql_stracks = "CREATE TABLE IF NOT EXISTS Stracks (Id TEXT PRIMARY KEY, Title TEXT NOT NULL, Description TEXT DEFAULT '', Priority INTEGER DEFAULT 3 CHECK(Priority BETWEEN 1 AND 5), Status TEXT DEFAULT 'active' CHECK(Status IN ('active','archived')), CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
        # Execute the Stracks table creation statement against the database connection.
        self.database_connection.execute(sql_stracks)
        # Define the SQL to create the Plans project plans table with foreign key and status constraints.
        sql_plans = "CREATE TABLE IF NOT EXISTS Plans (Id TEXT PRIMARY KEY, StrackId TEXT NOT NULL REFERENCES Stracks(Id) ON DELETE CASCADE, Title TEXT NOT NULL, Description TEXT DEFAULT '', Status TEXT DEFAULT 'pending' CHECK(Status IN ('pending','in_progress','done','blocked')), Priority INTEGER DEFAULT 3 CHECK(Priority BETWEEN 1 AND 5), CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
        # Execute the Plans table creation statement against the database connection.
        self.database_connection.execute(sql_plans)
        # Define the SQL to create the Issues tracking table with severity classification.
        sql_issues = "CREATE TABLE IF NOT EXISTS Issues (Id TEXT PRIMARY KEY, StrackId TEXT NOT NULL REFERENCES Stracks(Id) ON DELETE CASCADE, Title TEXT NOT NULL, Description TEXT DEFAULT '', Status TEXT DEFAULT 'open' CHECK(Status IN ('open','in_progress','resolved','closed')), Severity TEXT DEFAULT 'medium' CHECK(Severity IN ('critical','high','medium','low')), CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
        # Execute the Issues table creation statement against the database connection.
        self.database_connection.execute(sql_issues)
        # Define the SQL to create the Actions task table with status tracking.
        sql_actions = "CREATE TABLE IF NOT EXISTS Actions (Id TEXT PRIMARY KEY, StrackId TEXT NOT NULL REFERENCES Stracks(Id) ON DELETE CASCADE, Title TEXT NOT NULL, Description TEXT DEFAULT '', Status TEXT DEFAULT 'pending' CHECK(Status IN ('pending','in_progress','done','cancelled')), CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
        # Execute the Actions table creation statement against the database connection.
        self.database_connection.execute(sql_actions)
        # Define the SQL to create the Notes content table for freeform documentation.
        sql_notes = "CREATE TABLE IF NOT EXISTS Notes (Id TEXT PRIMARY KEY, StrackId TEXT NOT NULL REFERENCES Stracks(Id) ON DELETE CASCADE, Title TEXT NOT NULL, Content TEXT DEFAULT '', CreatedAt TEXT NOT NULL, UpdatedAt TEXT NOT NULL)"
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
            self._init_open_connection_function_()
            # Create all five entity tables in the database schema.
            self._init_create_tables_function_()
        # Handle operational errors such as disk I/O failures or locked database files.
        except sqlite3.OperationalError as operational_error:
            # Build the error message with operational failure context in Chinese.
            message_error = "[X] (OperationalError) 数据库操作失败，无法打开或写入数据库文件"
            message_error += f"，错误详情: {operational_error}"
            # Output the error message for diagnostics since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream error handling.
            raise sqlite3.OperationalError(message_error) from operational_error
        # Handle all other unexpected errors during schema initialization.
        except Exception as exception_error:
            # Build the error message for unanticipated failures in Chinese.
            message_error = "[X] (OtherError) 数据库初始化过程中发生未知错误"
            message_error += f"，具体查看: {exception_error}"
            # Output the error message for diagnostics since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream error handling.
            raise Exception(message_error) from exception_error
        # Ensure the database connection is always closed after initialization.
        finally:
            # Close the database connection regardless of success or failure.
            self._init_close_connection_function_()
