# Enterprise Student Record & Academic Management Platform
Flask REST API with pytest, Jenkins CI, Docker and Kubernetes (Minikube).

Run locally:  pip install -r requirements.txt && python run.py
Test:         pytest -v --cov=app tests/
Endpoints:    GET /api/health, GET/POST /api/students, GET /api/courses,
              POST /api/enroll, POST /api/grades, GET /api/students/<id>/gpa
Rule:         max 18 credits per semester per student.
