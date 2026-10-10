import pytest
from app.services.academic_service import AcademicService as S


def test_add_student():
    assert S.add_student("S201", "Carl", "c@u.edu")["credits"] == 0


def test_duplicate_student_rejected():
    with pytest.raises(ValueError):
        S.add_student("S101", "X", "x@u.edu")


def test_missing_fields_rejected():
    with pytest.raises(ValueError):
        S.add_student("", "X", "x@u.edu")
