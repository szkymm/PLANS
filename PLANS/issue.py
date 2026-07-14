# -*- coding: utf-8 -*-
"""
THIS FILE IS CORE PART OF PLANS BY MATT BELFAST BROWN.

====================
MODULE               : PLANS.issue

TYPE                 : Python Script

DESCRIPTION          :
    Issue entity module for the PLANS local-first project management
    system. An Issue represents a bug or problem belonging to a Strack
    container with status open, in_progress, resolved, closed and
    severity critical, high, medium, low tracking.

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

FILE VERSION         : 0.1.0


STATUS               : Stable

PYTHON               : >=3.9

LICENSE              : GPL-3.0-only

SPDX ID              : GPL-3.0-only


USAGE                :
    from PLANS.issue import IssueManager

    issue_manager = IssueManager(database_manager)
    issue = issue_manager.create_issue(
        strack_id="strack-001",
        issue_id="issue-001",
        title="Login page crash on submit",
        severity="critical",
    )
    all_issues = issue_manager.list_issues()

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

from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from .database import DatabaseManager

# Define the package version string to match PROJECT VERSION in docstring.
__version__ = "0.1.0"

# Define the set of allowed status values for the Issue entity.
allowed_statuses = ["open", "in_progress", "resolved", "closed"]

# Define the set of allowed severity values for the Issue entity.
allowed_severities = ["critical", "high", "medium", "low"]


class IssueManager:
    """
    ISSUEMANAGER CLASS IS CORE PART OF PLANS issue.py.

    PLANS.issue.IssueManager:
        Manages Issue entities within the PLANS project management system.
        Provides full CRUD operations for Issue records stored in a
        Strack container with status tracking and severity classification.

    ATTRIBUTES                         :
        database_manager (DatabaseManager): Reference to the database
            connection manager for executing SQL operations.
        table_name (str): Name of the database table storing Issue records.

    PUBLIC METHODS                     :
        create_issue(strack_id, issue_id, title, description="", severity="medium") -> Dict[str, Any]:
            Create a new Issue record with the specified attributes.
        get_issue(issue_id) -> Optional[Dict[str, Any]]:
            Retrieve a single Issue by its unique identifier.
        list_issues(strack_id=None, status=None, severity=None) -> List[Dict[str, Any]]:
            List Issue records filtered by optional Strack, status, or severity.
        update_issue(issue_id, **kwargs) -> Dict[str, Any]:
            Update mutable fields of an existing Issue record.
        delete_issue(issue_id) -> bool:
            Delete an Issue record permanently by its unique identifier.

    PRIVATE METHODS                    :
        _init_build_timestamp_function_(self) -> str:
            Generate the current UTC timestamp in ISO 8601 string format.

    USAGE                             :
        Instantiate IssueManager with a DatabaseManager instance and call
        its public methods to create, read, update, or delete Issue records.
        Each Issue belongs to a parent Strack identified by strack_id and
        tracks its own status and severity independently.

    WARNING                           :
        Private methods should not be called from outside the class.
    """

    def __init__(self, database_manager):
        """
        Initialize the IssueManager with a database connection reference.

        The constructor stores the database manager and sets the fixed
        table name constant used for all Issue record operations.

        The parameters are as follows:

        :param database_manager: The database connection manager instance.
        :type database_manager: DatabaseManager
        """
        # Store the database manager reference for executing SQL operations.
        self.database_manager = database_manager
        # Set the table name constant for Issue records storage.
        self.table_name = "Issues"

    def _init_build_timestamp_function_(self):
        """
        Generate the current UTC timestamp in ISO 8601 string format.

        This private method obtains the current date and time in UTC
        and formats it as an ISO 8601 string suitable for database storage.

        :return: The current UTC timestamp as an ISO 8601 formatted string.
        :rtype: str
        """
        # Obtain the current moment in the UTC timezone.
        datetime_current = datetime.now(timezone.utc)
        # Format the datetime object into an ISO 8601 string representation.
        timestamp_isoformat = datetime_current.isoformat()
        # Return the formatted timestamp string for database insertion.
        return timestamp_isoformat

    def create_issue(self, strack_id, issue_id, title, description="", severity="medium"):
        """
        Create a new Issue record in the database.

        Inserts a new Issue with the provided attributes after validating
        the severity value against the allowed set. The initial status
        is always set to open and timestamps are generated automatically.

        The parameters are as follows:

        :param strack_id: The identifier of the parent Strack container.
        :type strack_id: str
        :param issue_id: The unique identifier for the new Issue record.
        :type issue_id: str
        :param title: The descriptive title of the Issue.
        :type title: str
        :param description: The optional detailed description of the Issue.
        :type description: str
        :param severity: The severity level, one of critical, high, medium, low.
        :type severity: str
        :return: A dictionary representation of the created Issue record.
        :rtype: Dict[str, Any]
        :raise ValueError: If the provided severity is not in the allowed set.
        :raise Exception: If an unexpected database error occurs during insertion.
        """
        # Validate that the provided severity is within the allowed set.
        if severity not in allowed_severities:
            # Raise an error with a message listing all valid severity options.
            raise ValueError(
                f"Invalid severity '{severity}'. Must be one of: {allowed_severities}"
            )
        # Generate the current UTC timestamp for record creation and update.
        timestamp_current = self._init_build_timestamp_function_()
        # Attempt to insert the new Issue record into the database.
        try:
            # Build the Issue data dictionary with PascalCase keys for storage.
            issue_data = {
                "Id": issue_id,
                "StrackId": strack_id,
                "Title": title,
                "Description": description,
                "Status": "open",
                "Severity": severity,
                "CreatedAt": timestamp_current,
                "UpdatedAt": timestamp_current,
            }
            # Execute the SQL insert operation through the database manager.
            self.database_manager.insert_record(self.table_name, issue_data)
            # Return the created Issue dictionary to the caller.
            return issue_data
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 创建Issue时发生未知错误: "
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error

    def get_issue(self, issue_id):
        """
        Retrieve a single Issue by its unique identifier.

        Fetches an Issue record from the database and returns it as a
        dictionary, or None if no matching record is found.

        The parameters are as follows:

        :param issue_id: The unique identifier of the Issue to retrieve.
        :type issue_id: str
        :return: The Issue record as a dictionary, or None if not found.
        :rtype: Optional[Dict[str, Any]]
        :raise Exception: If an unexpected database error occurs during retrieval.
        """
        # Attempt to fetch the Issue record from the database.
        try:
            # Build a WHERE clause filter targeting the Id primary key column.
            filter_condition = f"Id = '{issue_id}'"
            # Execute the SQL select query through the database manager.
            record_list = self.database_manager.select_records(
                self.table_name, filter_condition
            )
            # Return the first matching record as a dictionary, or None.
            if record_list:
                # Convert the sqlite3.Row object to a plain dictionary.
                return dict(record_list[0])
            # Return None when no matching Issue record is found.
            return None
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 获取Issue时发生未知错误: "
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error

    def list_issues(self, strack_id=None, status=None, severity=None):
        """
        List Issue records filtered by optional criteria.

        Retrieves all Issue records optionally narrowed by Strack container,
        status, and severity. Returns an empty list when no records match.

        The parameters are as follows:

        :param strack_id: Optional Strack container identifier for filtering.
        :type strack_id: Optional[str]
        :param status: Optional status filter, one of open, in_progress, resolved, closed.
        :type status: Optional[str]
        :param severity: Optional severity filter, one of critical, high, medium, low.
        :type severity: Optional[str]
        :return: A list of Issue record dictionaries matching the applied filters.
        :rtype: List[Dict[str, Any]]
        :raise Exception: If an unexpected database error occurs during listing.
        """
        # Attempt to fetch filtered Issue records from the database.
        try:
            # Initialize an empty list to accumulate WHERE condition clauses.
            condition_list = []
            # Add the Strack container filter if a strack_id argument is provided.
            if strack_id is not None:
                # Build the equality condition clause for the StrackId column.
                condition_list.append(f"StrackId = '{strack_id}'")
            # Add the status filter if a status argument is provided.
            if status is not None:
                # Build the equality condition clause for the Status column.
                condition_list.append(f"Status = '{status}'")
            # Add the severity filter if a severity argument is provided.
            if severity is not None:
                # Build the equality condition clause for the Severity column.
                condition_list.append(f"Severity = '{severity}'")
            # Join all accumulated conditions with AND to form the full filter.
            if condition_list:
                # Combine the conditions into a single filter string with AND.
                filter_condition = " AND ".join(condition_list)
            else:
                # Use an empty filter string when no conditions are specified.
                filter_condition = ""
            # Execute the SQL select query through the database manager.
            record_list = self.database_manager.select_records(
                self.table_name, filter_condition
            )
            # Convert each sqlite3.Row object to a plain dictionary.
            return [dict(row) for row in record_list]
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 列出Issue时发生未知错误: "
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error

    def update_issue(self, issue_id, **kwargs):
        """
        Update mutable fields of an existing Issue record.

        Modifies the Title, Description, Status, and Severity fields of
        the Issue identified by issue_id. The UpdatedAt timestamp is
        automatically refreshed on every update.

        The parameters are as follows:

        :param issue_id: The unique identifier of the Issue to update.
        :type issue_id: str
        :param kwargs: Keyword arguments specifying fields to update.
            Supported keys are Title, Description, Status, and Severity.
        :type kwargs: Dict[str, Any]
        :return: The fully updated Issue record as a dictionary.
        :rtype: Dict[str, Any]
        :raise ValueError: If an unsupported keyword argument is provided.
        :raise ValueError: If the provided status or severity value is invalid.
        :raise ValueError: If no Issue exists with the given issue_id.
        :raise Exception: If an unexpected database error occurs during update.
        """
        # Define the set of field names that are allowed to be updated.
        allowed_fields = {"Title", "Description", "Status", "Severity"}
        # Validate each provided keyword argument against the allowed field set.
        for keyword_key in kwargs:
            # Raise an error when an unsupported field name is provided.
            if keyword_key not in allowed_fields:
                # Raise with a descriptive message listing the allowed fields.
                raise ValueError(
                    f"Invalid field '{keyword_key}'. Allowed fields: {allowed_fields}"
                )
        # Validate the Status value if it is being updated in this call.
        if "Status" in kwargs:
            # Raise an error when the status value is not in the allowed set.
            if kwargs["Status"] not in allowed_statuses:
                # Raise with a descriptive message listing valid status options.
                raise ValueError(
                    f"Invalid status '{kwargs['Status']}'. "
                    f"Must be one of: {allowed_statuses}"
                )
        # Validate the Severity value if it is being updated in this call.
        if "Severity" in kwargs:
            # Raise an error when the severity value is not in the allowed set.
            if kwargs["Severity"] not in allowed_severities:
                # Raise with a descriptive message listing valid severity options.
                raise ValueError(
                    f"Invalid severity '{kwargs['Severity']}'. "
                    f"Must be one of: {allowed_severities}"
                )
        # Attempt to update the Issue record in the database.
        try:
            # Retrieve the existing Issue record to confirm it exists.
            existing_issue = self.get_issue(issue_id)
            # Raise an error when the specified Issue record is not found.
            if existing_issue is None:
                # Raise with a message identifying the missing Issue identifier.
                raise ValueError(f"Issue with Id '{issue_id}' not found.")
            # Generate a fresh UTC timestamp for the UpdatedAt field.
            timestamp_current = self._init_build_timestamp_function_()
            # Set the UpdatedAt field to the freshly generated current timestamp.
            kwargs["UpdatedAt"] = timestamp_current
            # Build the WHERE clause to target the specific Issue record by Id.
            filter_condition = f"Id = '{issue_id}'"
            # Execute the SQL update operation through the database manager.
            self.database_manager.update_record(
                self.table_name, kwargs, filter_condition
            )
            # Retrieve and return the fully updated Issue from the database.
            return self.get_issue(issue_id)
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 更新Issue时发生未知错误: "
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error

    def delete_issue(self, issue_id):
        """
        Delete an Issue record permanently by its unique identifier.

        Removes the Issue from the database and returns a boolean
        indicating whether a record was actually deleted.

        The parameters are as follows:

        :param issue_id: The unique identifier of the Issue to delete.
        :type issue_id: str
        :return: True if the Issue was found and deleted, False otherwise.
        :rtype: bool
        :raise Exception: If an unexpected database error occurs during deletion.
        """
        # Attempt to delete the Issue record from the database.
        try:
            # Build the WHERE clause to target the specific Issue record by Id.
            filter_condition = f"Id = '{issue_id}'"
            # Execute the SQL delete operation through the database manager.
            rows_affected = self.database_manager.delete_record(
                self.table_name, filter_condition
            )
            # Determine whether the deletion affected at least one record row.
            is_deleted = rows_affected > 0
            # Return the boolean result indicating the success of the deletion.
            return is_deleted
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 删除Issue时发生未知错误: "
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
