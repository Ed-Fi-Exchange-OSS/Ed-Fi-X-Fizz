# SPDX-License-Identifier: Apache-2.0
# Licensed to the Ed-Fi Alliance under one or more agreements.
# The Ed-Fi Alliance licenses this file to you under the Apache License,  Version 2.0.
# See the LICENSE and NOTICES files in the project root for more information.

import pandas as pd
import pytest

from edfi_schoology_extractor.mapping.assignments import map_to_udm


def describe_when_mapping_empty_DataFrame():
    def it_should_return_empty_DataFrame():
        df = map_to_udm(pd.DataFrame(), 1234)
        assert (df == pd.DataFrame()).all().all()


def describe_when_mapping_Schoology_DataFrame_to_EdFi_DataFrame():
    @pytest.fixture
    def result() -> pd.DataFrame:

        assignment = {
            "id": 123355,
            "title": "The title",
            "type": "assignment",
            "description": "The description",
            "due": "2020-08-21 23:59:00",
            "max_points": 52,
            "CreateDate": "2020-11-04 09:46:45",
            "LastModifiedDate": "2020-11-04 09:46:45",
        }
        section_id = 42

        # Arrange
        schoology_df = pd.DataFrame([assignment])

        # Act
        return map_to_udm(schoology_df, section_id)

    def it_should_have_correct_number_of_columns(result):
        assert result.shape[1] == 15

    def it_should_have_schoology_as_SourceSystem(result):
        assert result["SourceSystem"].iloc[0] == "Schoology"

    def it_should_map_id_to_SourceSystemIdentifier(result):
        assert result["SourceSystemIdentifier"].iloc[0] == 123355

    def it_should_map_title_to_Title(result):
        assert result["Title"].iloc[0] == "The title"

    def it_should_map_description_to_AssignmentDescription(result):
        assert result["AssignmentDescription"].iloc[0] == "The description"

    def it_should_map_due_to_DueDateTime(result):
        assert str(result["DueDateTime"].iloc[0]) == "2020-08-21 23:59:00"

    def it_should_map_max_points_to_MaxPoints(result):
        assert result["MaxPoints"].iloc[0] == 52

    def it_should_map_section_id_to_LMSSectionSourceSystemIdentifier(result):
        assert result["LMSSectionSourceSystemIdentifier"].iloc[0] == 42

    def it_should_map_type_to_AssignmentCategory(result):
        assert result["AssignmentCategory"].iloc[0] == "assignment"

    def it_should_have_CreateDate(result):
        assert result["CreateDate"].iloc[0] == "2020-11-04 09:46:45"

    def it_should_have_LastModifiedDate(result):
        assert result["LastModifiedDate"].iloc[0] == "2020-11-04 09:46:45"

    def it_should_have_empty_SubmissionType(result):
        assert result["SubmissionType"].iloc[0] is None

    def it_should_have_empty_SourceCreateDate(result):
        assert result["SourceCreateDate"].iloc[0] == ""

    def it_should_have_empty_SourceLastModifiedDate(result):
        assert result["SourceLastModifiedDate"].iloc[0] == ""

    def it_should_have_empty_StartDateTime(result):
        assert result["StartDateTime"].iloc[0] == ""

    def it_should_have_empty_EndDateTime(result):
        assert result["EndDateTime"].iloc[0] == ""
