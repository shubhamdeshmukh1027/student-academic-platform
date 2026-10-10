def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200 and r.get_json()["status"] == "UP"


def test_list_students(client):
    assert len(client.get("/api/students").get_json()) == 2


def test_create_student(client):
    r = client.post("/api/students", json={"student_id": "S300", "name": "D",
                                           "email": "d@u.edu"})
    assert r.status_code == 201


def test_enroll_and_gpa(client):
    client.post("/api/enroll", json={"student_id": "S101", "course_id": "C101"})
    client.post("/api/grades", json={"student_id": "S101", "course_id": "C101",
                                     "grade": "A"})
    assert client.get("/api/students/S101/gpa").get_json()["gpa"] == 4.0


def test_unknown_student_404(client):
    assert client.get("/api/students/NOPE").status_code == 404
