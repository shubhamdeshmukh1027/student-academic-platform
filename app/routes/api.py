from flask import Blueprint, jsonify, request
from app.services.academic_service import AcademicService as S
from database.db import db

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/health")
def health():
    return jsonify({"status": "UP", "service": "student-academic-platform"}), 200


@api.route("/students", methods=["GET"])
def list_students():
    return jsonify(list(db.students.values()))


@api.route("/students", methods=["POST"])
def create_student():
    d = request.get_json(silent=True) or {}
    try:
        return jsonify(S.add_student(d.get("student_id"), d.get("name"),
                                     d.get("email"))), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api.route("/students/<sid>", methods=["GET"])
def get_student(sid):
    s = S.get_student(sid)
    return (jsonify(s), 200) if s else (jsonify({"error": "Student not found"}), 404)


@api.route("/courses", methods=["GET"])
def list_courses():
    return jsonify(list(db.courses.values()))


@api.route("/enroll", methods=["POST"])
def enroll():
    d = request.get_json(silent=True) or {}
    try:
        return jsonify(S.enroll(d.get("student_id"), d.get("course_id"))), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api.route("/grades", methods=["POST"])
def grade():
    d = request.get_json(silent=True) or {}
    try:
        return jsonify(S.assign_grade(d.get("student_id"), d.get("course_id"),
                                      d.get("grade"))), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api.route("/students/<sid>/gpa", methods=["GET"])
def gpa(sid):
    try:
        return jsonify({"student_id": sid, "gpa": S.calculate_gpa(sid)})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
