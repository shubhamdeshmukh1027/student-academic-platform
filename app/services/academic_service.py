from database.db import db
from app.models.student import GRADE_POINTS, MAX_CREDITS


class AcademicService:
    """Business rules for student records, enrollment and grading."""

    @staticmethod
    def add_student(student_id, name, email):
        if not student_id or not name or not email:
            raise ValueError("student_id, name and email are mandatory.")
        if student_id in db.students:
            raise ValueError(f"Student '{student_id}' already exists.")
        record = {"student_id": student_id, "name": name, "email": email, "credits": 0}
        db.students[student_id] = record
        return record

    @staticmethod
    def get_student(student_id):
        return db.students.get(student_id)

    @staticmethod
    def enroll(student_id, course_id):
        student = db.students.get(student_id)
        course = db.courses.get(course_id)
        if not student:
            raise ValueError("Student not found.")
        if not course:
            raise ValueError("Course not found.")
        mine = [e for e in db.enrollments if e["student_id"] == student_id]
        if any(e["course_id"] == course_id for e in mine):
            raise ValueError("Student already enrolled in this course.")
        if course["enrolled"] >= course["capacity"]:
            raise ValueError("Course is full.")
        for e in mine:
            if db.courses[e["course_id"]]["slot"] == course["slot"]:
                raise ValueError("Schedule conflict: same time slot.")
        if student["credits"] + course["credits"] > MAX_CREDITS:
            raise ValueError(f"Credit limit exceeded (max {MAX_CREDITS}).")
        record = {"student_id": student_id, "course_id": course_id, "grade": None}
        db.enrollments.append(record)
        student["credits"] += course["credits"]
        course["enrolled"] += 1
        return record

    @staticmethod
    def assign_grade(student_id, course_id, grade):
        grade = (grade or "").upper()
        if grade not in GRADE_POINTS:
            raise ValueError("Grade must be one of A, B, C, D, F.")
        for e in db.enrollments:
            if e["student_id"] == student_id and e["course_id"] == course_id:
                e["grade"] = grade
                return e
        raise ValueError("Enrollment not found.")

    @staticmethod
    def calculate_gpa(student_id):
        if student_id not in db.students:
            raise ValueError("Student not found.")
        total_points = total_credits = 0
        for e in db.enrollments:
            if e["student_id"] == student_id and e["grade"]:
                credits = db.courses[e["course_id"]]["credits"]
                total_points += GRADE_POINTS[e["grade"]] * credits
                total_credits += credits
        return round(total_points / total_credits, 2) if total_credits else 0.0
