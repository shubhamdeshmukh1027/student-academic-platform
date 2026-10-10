import pytest
from app.services.academic_service import AcademicService as S
from database.db import db


def test_enroll_updates_credits():
    S.enroll("S101", "C101")
    assert db.students["S101"]["credits"] == 6


def test_duplicate_enrollment_blocked():
    S.enroll("S101", "C101")
    with pytest.raises(ValueError):
        S.enroll("S101", "C101")


def test_schedule_conflict_blocked():
    S.enroll("S101", "C101")
    with pytest.raises(ValueError, match="conflict"):
        S.enroll("S101", "C104")


def test_credit_limit_enforced():
    S.enroll("S101", "C101")
    S.enroll("S101", "C102")
    S.enroll("S101", "C103")
    db.courses["C900"] = {"course_id": "C900", "title": "Extra", "credits": 3,
                          "slot": "FRI-09", "capacity": 30, "enrolled": 0}
    with pytest.raises(ValueError, match="Credit limit"):
        S.enroll("S101", "C900")


def test_gpa_calculation():
    S.enroll("S101", "C101")
    S.enroll("S101", "C102")
    S.assign_grade("S101", "C101", "A")
    S.assign_grade("S101", "C102", "B")
    assert S.calculate_gpa("S101") == 3.5


def test_invalid_grade():
    S.enroll("S101", "C101")
    with pytest.raises(ValueError):
        S.assign_grade("S101", "C101", "Z")
