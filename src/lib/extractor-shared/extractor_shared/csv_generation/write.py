# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License, Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import logging
from typing import Dict, Tuple
import os
from datetime import datetime
from pandas import DataFrame


USERS_ROOT_DIRECTORY = "users/"
SECTIONS_ROOT_DIRECTORY = "sections/"
SECTION_ASSOCIATIONS_ROOT_DIRECTORY = "section={id}/section-associations/"
ASSIGNMENT_ROOT_DIRECTORY = "section={id}/assignments/"
SUBMISSION_ROOT_DIRECTORY = "section={id1}/assignment={id2}/submissions/"
USER_ACTIVITY_ROOT_DIRECTORY = "section={id}/user-activities/"
GRADES_ROOT_DIRECTORY = "section={id}/grades/"
SYSTEM_ACTIVITY_ROOT_DIRECTORY = "system-activities/"

logger = logging.getLogger(__name__)


def _write_csv(df_to_write: DataFrame, output_date: datetime, directory: str):
    """
    Write a LMS UDM DataFrame to a CSV file

    Parameters
    ----------
    df_to_write: DataFrame
        is a LMS UDM DataFrame
    output_date: datetime
        is the timestamp for the filename
    directory: str
        is the directory the file will go in
    """
    filename: str = output_date.strftime("%Y-%m-%d-%H-%M-%S")
    path = os.path.join(directory, f"{filename}.csv")

    try:
        os.makedirs(directory, exist_ok=True)
        df_to_write.to_csv(path, index=False)

        logger.info(f"Generated file => {path}")
    except Exception:
        logger.exception("An exception occurred while writing file %s", path)


def _write_multi_csv(
    dfs_to_write: Dict[str, DataFrame], output_date: datetime, directory_template: str
):
    """
    Write a series of LMS UDM DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: Dict[str, DataFrame]
        is a Dict of id/LMS UDM DataFrame pairs
    output_date: datetime
        is the timestamp for the filename
    directory_template: str
        is the directory the file will go in, with an {id} placeholder
    """
    assert "{id}" in directory_template

    for id_placeholder, df_to_write in dfs_to_write.items():
        directory: str = directory_template.format(id=id_placeholder)
        _write_csv(df_to_write, output_date, directory)


def _write_multi_tuple_csv(
    dfs_to_write: Dict[Tuple[str, str], DataFrame],
    output_date: datetime,
    directory_template: str,
):
    """
    Write a series of LMS UDM DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: Dict[Tuple[str, str], DataFrame]
        is a Dict of 2 id tuples/LMS UDM DataFrame pairs
    output_date: datetime
        is the timestamp for the filename
    directory_template: str
        is the directory the file will go in, with an {id1} and an {id2} placeholder
    """
    assert "{id1}" in directory_template
    assert "{id2}" in directory_template

    for id_tuple, df_to_write in dfs_to_write.items():
        (id1, id2) = id_tuple
        directory: str = directory_template.format(id1=id1, id2=id2)
        _write_csv(df_to_write, output_date, directory)


def write_users(df_to_write: DataFrame, output_date: datetime, output_directory: str):
    """
    Write a LMS UDM Users DataFrame to a CSV file

    Parameters
    ----------
    df_to_write: DataFrame
        is a LMS UDM Users DataFrame
    output_date: datetime
        is the timestamp for the filename
    output_directory: str
        is the root output directory
    """
    _write_csv(
        df_to_write, output_date, os.path.join(output_directory, USERS_ROOT_DIRECTORY)
    )


def write_sections(
    df_to_write: DataFrame, output_date: datetime, output_directory: str
):
    """
    Write a LMS UDM Sections DataFrame to a CSV file

    Parameters
    ----------
    df_to_write: DataFrame
        is a LMS UDM Sections DataFrame
    output_date: datetime
        is the timestamp for the filename
    output_directory: str
        is the root output directory
    """
    _write_csv(
        df_to_write,
        output_date,
        os.path.join(output_directory, SECTIONS_ROOT_DIRECTORY),
    )


def write_section_associations(
    dfs_to_write: Dict[str, DataFrame], output_date: datetime, output_directory: str
):
    """
    Write a series of LMS UDM UserSectionAssociation DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: Dict[str, DataFrame]
        is a Dict of id/LMS UDM UserSectionAssociation DataFrame pairs
    output_date: datetime
        is the timestamp for the filename
    output_directory: str
        is the root output directory
    """
    _write_multi_csv(
        dfs_to_write,
        output_date,
        os.path.join(output_directory, SECTION_ASSOCIATIONS_ROOT_DIRECTORY),
    )


def write_assignments(
    dfs_to_write: Dict[str, DataFrame], output_date: datetime, output_directory: str
):
    """
    Write a series of LMS UDM Assignments DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: Dict[str, DataFrame]
        is a Dict of id/LMS UDM Assignments DataFrame pairs
    output_date: datetime
        is the timestamp for the filename
    output_directory: str
        is the root output directory
    """
    _write_multi_csv(
        dfs_to_write,
        output_date,
        os.path.join(output_directory, ASSIGNMENT_ROOT_DIRECTORY),
    )


def write_user_activities(
    dfs_to_write: Dict[str, DataFrame], output_date: datetime, output_directory: str
):
    """
    Write a series of LMS UDM UserActivities DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: Dict[str, DataFrame]
        is a Dict of id/LMS UDM UserActivities DataFrame pairs
    output_date: datetime
        is the timestamp for the filename
    output_directory: str
        is the root output directory
    """
    _write_multi_csv(
        dfs_to_write,
        output_date,
        os.path.join(output_directory, USER_ACTIVITY_ROOT_DIRECTORY),
    )


def write_assignment_submissions(
    dfs_to_write: Dict[Tuple[str, str], DataFrame],
    output_date: datetime,
    output_directory: str,
):
    """
    Write a series of LMS UDM AssignmentSubmissions DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: Dict[Tuple[str, str], DataFrame]
        is a Dict of 2 id tuples/LMS UDM AssignmentSubmissions DataFrame pairs
    output_date: datetime
        is the timestamp for the filename
    output_directory: str
        is the root output directory
    """
    _write_multi_tuple_csv(
        dfs_to_write,
        output_date,
        os.path.join(output_directory, SUBMISSION_ROOT_DIRECTORY),
    )


def write_grades(
    dfs_to_write: Dict[str, DataFrame], output_date: datetime, output_directory: str
):
    """
    Write a series of LMS UDM Grades DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: Dict[str, DataFrame]
        is a Dict of id/LMS UDM Grades DataFrame pairs
    output_date: datetime
        is the timestamp for the filename
    output_directory: str
        is the root output directory
    """
    _write_multi_csv(
        dfs_to_write,
        output_date,
        os.path.join(output_directory, GRADES_ROOT_DIRECTORY),
    )


def write_system_activities(
    df_to_write: DataFrame, output_date: datetime, output_directory: str
):
    """
    Write a series of LMS UDM System Activities DataFrames to CSV files

    Parameters
    ----------
    dfs_to_write: DataFrame
        Dataframe to write
    output_date: datetime
        is the timestamp for the filename
    output_directory: str
        is the root output directory
    """
    output_path = os.path.join(output_directory, SYSTEM_ACTIVITY_ROOT_DIRECTORY)
    output_path = os.path.join(output_path, "date=" + output_date.strftime("%Y-%m-%d"))

    _write_csv(
        df_to_write,
        output_date,
        output_path,
    )
