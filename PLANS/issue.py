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

PROJECT VERSION      : 0.1.2


FILE CREATE DATE     : 2026-07-15

FILE VERSION DATE    : 2026-07-15

FILE VERSION         : 0.1.1


STATUS               : Stable

PYTHON               : >=3.9

LICENSE              : GPL-3.0-only

SPDX ID              : GPL-3.0-only


USAGE                :
    from PLANS.issue import IssueManager

    issue_manager = IssueManager(database_manager)
    issue = issue_manager.insert_issue_record(
        strack_id="strack-001",
        issue_id="issue-001",
        item_title="Login page crash on submit",
        severity_level="critical",
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
__version__ = "0.1.2"

# Define the set of allowed status values for the Issue entity.
allowed_statuses = ["open", "in_progress", "resolved", "closed"]

# Define the set of allowed severity values for the Issue entity.
allowed_severities = ["critical", "high", "medium", "low"]


class IssueManager:
    """
    IssueManager CLASS IS CORE PART OF PLANS ISSUE.PY.

    PLANS.issue.IssueManager:
        Manages Issue entities within the PLANS project management system.
        Provides full CRUD operations for Issue records stored in a
        Strack container with status tracking and severity classification.

    ATTRIBUTES                         :
        database_manager (DatabaseManager): Reference to the database
            connection manager for executing SQL operations.
        table_name (str): Name of the database table storing Issue records.

    PUBLIC METHODS                     :
        insert_issue_record(strack_id, issue_id, item_title,
            item_description="", severity_level="medium") -> Dict[str, Any]:
            Create a new Issue record with the specified attributes.
        retrieve_issue(issue_id) -> Optional[Dict[str, Any]]:
            Retrieve a single Issue by its unique identifier.
        list_issues(strack_id=None, item_status=None, severity_level=None) -> List[Dict[str, Any]]:
            List Issue records filtered by optional Strack, status, or severity.
        modify_issue_fields(issue_id, **keyword_arguments) -> Dict[str, Any]:
            Update mutable fields of an existing Issue record.
        erase_issue_record(issue_id) -> bool:
            Erase an Issue record permanently by its unique identifier.

    PRIVATE METHODS                    :
        _init_form_timestamp_function_(self) -> str:
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

    def _init_form_timestamp_function_(self):
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

    def insert_issue_record(
        # Declare the self reference and required identifier parameters.
        self, strack_id, issue_id, item_title,
        # Declare optional description and severity keyword parameters.
        item_description="", severity_level="medium",
    ):
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
        :param item_title: The descriptive title of the Issue.
        :type item_title: str
        :param item_description: The optional detailed description of the Issue.
        :type item_description: str
        :param severity_level: The severity level, one of critical, high, medium, low.
        :type severity_level: str
        :return: A dictionary representation of the created Issue record.
        :rtype: Dict[str, Any]
        :raise ValueError: If the provided severity is not in the allowed set.
        :raise Exception: If an unexpected database error occurs during insertion.
        """
        # Validate that the provided severity is within the allowed set.
        if severity_level not in allowed_severities:
            # Raise an error with a message listing all valid severity options.
            raise ValueError(
                # Format the error message with the invalid severity and allowed values.
                f"Invalid severity '{severity_level}'. Must be one of: {allowed_severities}"
            )
        # Generate the current UTC timestamp for record creation and update.
        timestamp_current = self._init_form_timestamp_function_()
        # Attempt to insert the new Issue record into the database.
        try:
            # Build the Issue data dictionary with PascalCase keys for storage.
            issue_data = {
                # Map the Issue primary key identifier to the ID column.
                "ID": issue_id,
                # Map the parent Strack container identifier to the StrackID column.
                "StrackID": strack_id,
                # Map the descriptive title to the Title column.
                "Title": item_title,
                # Map the optional description to the Description column.
                "Description": item_description,
                # Set the initial status to the open enum value.
                "Status": "open",
                # Map the validated severity level to the Severity column.
                "Severity": severity_level,
                # Map the creation timestamp to the CreatedAt column.
                "CreatedAt": timestamp_current,
                # Map the update timestamp to the UpdatedAt column.
                "UpdatedAt": timestamp_current,
            }
            # Execute the SQL insert operation through the database manager.
            self.database_manager.insert_record(self.table_name, issue_data)
            # Return the created Issue dictionary to the caller.
            return issue_data
        # Handle any database error that occurs during the insert operation.
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 创建Issue时发生未知错误: "
            # Append the exception details to the Chinese error message.
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error

    def retrieve_issue(self, issue_id):
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
                # Supply the table name and filter condition as positional arguments.
                self.table_name, filter_condition
            )
            # Return the first matching record as a dictionary, or None.
            if record_list:
                # Convert the sqlite3.Row to a dict with CLASP-compliant PascalCase keys.
                dict_issue = dict(record_list[0])
                # Remap the database column name Id to CLASP-compliant ID key.
                dict_issue["ID"] = dict_issue.pop("Id")
                # Remap the database column name StrackId to CLASP-compliant StrackID key.
                dict_issue["StrackID"] = dict_issue.pop("StrackId")
                # Return the transformed dictionary with standardized key names.
                return dict_issue
            # Return None when no matching Issue record is found.
            return None
        # Handle any database error that occurs during the select operation.
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 获取Issue时发生未知错误: "
            # Append the exception details to the Chinese error message.
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error

    def list_issues(self, strack_id=None, item_status=None, severity_level=None):
        """
        List Issue records filtered by optional criteria.

        Retrieves all Issue records optionally narrowed by Strack container,
        status, and severity. Returns an empty list when no records match.

        The parameters are as follows:

        :param strack_id: Optional Strack container identifier for filtering.
        :type strack_id: Optional[str]
        :param item_status: Optional status filter, one of open, in_progress, resolved, closed.
        :type item_status: Optional[str]
        :param severity_level: Optional severity filter, one of critical, high, medium, low.
        :type severity_level: Optional[str]
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
            # Add the status filter if an item_status argument is provided.
            if item_status is not None:
                # Build the equality condition clause for the Status column.
                condition_list.append(f"Status = '{item_status}'")
            # Add the severity filter if a severity_level argument is provided.
            if severity_level is not None:
                # Build the equality condition clause for the Severity column.
                condition_list.append(f"Severity = '{severity_level}'")
            # Join all accumulated conditions with AND to form the full filter.
            if condition_list:
                # Combine the conditions into a single filter string with AND.
                filter_condition = " AND ".join(condition_list)
            # Handle the fallback path when no filter conditions are specified.
            else:
                # Use an empty filter string when no conditions are specified.
                filter_condition = ""
            # Execute the SQL select query through the database manager.
            record_list = self.database_manager.select_records(
                # Supply the table name and filter condition as positional arguments.
                self.table_name, filter_condition
            )
            # Initialize an empty list to collect Issue dictionaries with standardized keys.
            result_list = []
            # Convert each sqlite3.Row to a CLASP-compliant dict with PascalCase keys.
            for issue_row in record_list:
                # Convert the current row to a mutable dictionary keyed by database column names.
                dict_issue = dict(issue_row)
                # Remap the database column name Id to CLASP-compliant ID key.
                dict_issue["ID"] = dict_issue.pop("Id")
                # Remap the database column name StrackId to CLASP-compliant StrackID key.
                dict_issue["StrackID"] = dict_issue.pop("StrackId")
                # Accumulate the transformed dictionary into the result list.
                result_list.append(dict_issue)
            # Return the complete list of Issue dictionaries with standardized keys.
            return result_list
        # Handle any database error that occurs during the filtered select.
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 列出Issue时发生未知错误: "
            # Append the exception details to the Chinese error message.
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error

    def modify_issue_fields(self, issue_id, **keyword_arguments):
        """
        Update mutable fields of an existing Issue record.

        Modifies the Title, Description, Status, and Severity fields of
        the Issue identified by issue_id. The UpdatedAt timestamp is
        automatically refreshed on every update.

        The parameters are as follows:

        :param issue_id: The unique identifier of the Issue to update.
        :type issue_id: str
        :param keyword_arguments: Keyword arguments specifying fields to update.
            Supported keys are Title, Description, Status, and Severity.
        :type keyword_arguments: Dict[str, Any]
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
        for keyword_key in keyword_arguments:
            # Raise an error when an unsupported field name is provided.
            if keyword_key not in allowed_fields:
                # Raise with a descriptive message listing the allowed fields.
                raise ValueError(
                    # Format the error message with the invalid field name and allowed set.
                    f"Invalid field '{keyword_key}'. Allowed fields: {allowed_fields}"
                )
        # Validate the Status value if it is being updated in this call.
        if "Status" in keyword_arguments:
            # Raise an error when the status value is not in the allowed set.
            if keyword_arguments["Status"] not in allowed_statuses:
                # Build the error message with the invalid status and allowed values.
                message_error = f"Invalid status '{keyword_arguments['Status']}'. "
                # Append the list of valid status options to the error message.
                message_error += f"Must be one of: {allowed_statuses}"
                # Raise ValueError with the assembled error message.
                raise ValueError(message_error)
        # Validate the Severity value if it is being updated in this call.
        if "Severity" in keyword_arguments:
            # Raise an error when the severity value is not in the allowed set.
            if keyword_arguments["Severity"] not in allowed_severities:
                # Build the error message with the invalid severity and allowed values.
                message_error = f"Invalid severity '{keyword_arguments['Severity']}'. "
                # Append the list of valid severity options to the error message.
                message_error += f"Must be one of: {allowed_severities}"
                # Raise ValueError with the assembled error message.
                raise ValueError(message_error)
        # Attempt to update the Issue record in the database.
        try:
            # Retrieve the existing Issue record to confirm it exists.
            existing_issue = self.retrieve_issue(issue_id)
            # Raise an error when the specified Issue record is not found.
            if existing_issue is None:
                # Raise with a message identifying the missing Issue identifier.
                raise ValueError(f"Issue with Id '{issue_id}' not found.")
            # Generate a fresh UTC timestamp for the UpdatedAt field.
            timestamp_current = self._init_form_timestamp_function_()
            # Set the UpdatedAt field to the freshly generated current timestamp.
            keyword_arguments["UpdatedAt"] = timestamp_current
            # Build the WHERE clause to target the specific Issue record by Id.
            filter_condition = f"Id = '{issue_id}'"
            # Execute the SQL update operation through the database manager.
            self.database_manager.modify_table_record(
                # Supply the table name, update data, and filter condition as arguments.
                self.table_name, keyword_arguments, filter_condition
            )
            # Retrieve and return the fully updated Issue from the database.
            return self.retrieve_issue(issue_id)
        # Handle any database error that occurs during the update operation.
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 更新Issue时发生未知错误: "
            # Append the exception details to the Chinese error message.
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error

    def erase_issue_record(self, issue_id):
        """
        Erase an Issue record permanently by its unique identifier.

        Removes the Issue from the database and returns a boolean
        indicating whether a record was actually deleted.

        The parameters are as follows:

        :param issue_id: The unique identifier of the Issue to erase.
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
            records_affected = self.database_manager.purge_table_record(
                # Supply the table name and filter condition as positional arguments.
                self.table_name, filter_condition
            )
            # Determine whether the deletion affected at least one record row.
            is_deleted = records_affected > 0
            # Return the boolean result indicating the success of the deletion.
            return is_deleted
        # Handle any database error that occurs during the delete operation.
        except Exception as exception_error:
            # Build the error message with the exception context in Chinese.
            message_error = "[X] (OtherError) 删除Issue时发生未知错误: "
            # Append the exception details to the Chinese error message.
            message_error += f"{exception_error}"
            # Output the error message since no logger is configured.
            print(message_error)
            # Re-raise with the diagnostic message for upstream handling.
            raise Exception(message_error) from exception_error
