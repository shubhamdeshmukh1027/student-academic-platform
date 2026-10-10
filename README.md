# Student Record & Academic Management Platform

A Flask REST API for managing students, faculty, courses, enrollments and grades. The project demonstrates a complete DevOps workflow: Git branching with pull requests, automated testing, Jenkins CI, Docker containerization and Kubernetes orchestration (Minikube).

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Workflow](#2-project-workflow)
3. [Project Structure](#3-project-structure)
4. [Step 1: Set Up the Tools](#4-step-1-set-up-the-tools)
5. [Step 2: Create the Repository and Branches](#5-step-2-create-the-repository-and-branches)
6. [Step 3: Build the Flask Application](#6-step-3-build-the-flask-application)
7. [Step 4: Write and Run Automated Tests](#7-step-4-write-and-run-automated-tests)
8. [Step 5: Set Up Jenkins CI](#8-step-5-set-up-jenkins-ci)
9. [Step 6: Dockerize the Application](#9-step-6-dockerize-the-application)
10. [Step 7: Deploy on Kubernetes (Minikube)](#10-step-7-deploy-on-kubernetes-minikube)
11. [API Documentation](#11-api-documentation)
12. [Troubleshooting](#12-troubleshooting)
13. [Learnings](#13-learnings)
14. [Author](#14-author)

---

## 1. Project Overview

| Item | Details |
|------|---------|
| Project | Student Record & Academic Management Platform |
| Language and framework | Python 3.11, Flask |
| Entities | Students, Faculty, Courses, Enrollments, Grades |
| Business rule | Maximum **18 credits per semester** per student |
| Database | In-memory database with seed data |
| Testing | pytest, pytest-cov, Flask `test_client` |
| Code quality | flake8 |
| CI | Jenkins declarative pipeline |
| Container | Docker, Gunicorn on port 5000 |
| Orchestration | Kubernetes on Minikube, 3 replicas, NodePort 30090 |
| Environment | Ubuntu on WSL2 |

## 2. Project Workflow

The project moves through six stages. Each stage was built on its own Git branch and merged into `main` through a pull request.

| Stage | Branch | What happens |
|-------|--------|--------------|
| 1 | `feature/foundation` | Repository set up with `.gitignore` and base files |
| 2 | `feature/core-app` | Flask app, services, models and REST API built |
| 3 | `feature/automated-tests` | pytest tests written for GPA, enrollment rules and API |
| 4 | `feature/jenkins-ci` | Jenkinsfile added; pipeline lints and tests every run |
| 5 | `feature/dockerization` | Dockerfile added; app runs as a container |
| 6 | `feature/kubernetes-orchestration` | Deployment and Service manifests added; app runs on 3 pods |

**End-to-end flow:**

```
Code on feature branch -> Pull Request -> Merge to main
-> Jenkins: checkout -> install -> flake8 -> pytest -> JUnit report
-> Docker image build -> Kubernetes deployment (3 replicas) -> Service on NodePort 30090
```

## 3. Project Structure

```
student-academic-platform/
├── app/                  # routes, services, models
├── database/
│   └── db.py             # in-memory database with seed data
├── tests/                # pytest unit and API tests
├── k8s/
│   ├── deployment.yaml   # 3 replicas, probes
│   └── service.yaml      # NodePort 30090
├── Dockerfile
├── .dockerignore
├── Jenkinsfile
├── requirements.txt      # Flask, pytest, pytest-cov, gunicorn, flake8
├── run.py                # application entry point
├── .gitignore
└── README.md
```

---

## 4. Step 1: Set Up the Tools

**Goal:** prepare the development environment on Ubuntu (WSL2).

1. Update the system and install Python, Git and curl:

   ```bash
   sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv git curl
   ```

2. Set your Git identity:

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

3. Verify the installation:

   ```bash
   python3 --version
   git --version
   ```

## 5. Step 2: Create the Repository and Branches

**Goal:** create the repo and use one branch per topic.

1. Create the project folder and initialize Git:

   ```bash
   mkdir student-academic-platform && cd student-academic-platform
   git init
   ```

2. Create a `.gitignore` containing:

   ```
   venv/
   __pycache__/
   .pytest_cache/
   reports/
   *.xml
   ```

3. Connect the folder to a GitHub repository and push `main`.

4. For every stage, create a branch, commit your work and push it:

   ```bash
   git checkout -b feature/foundation
   git add .
   git commit -m "Add project foundation"
   git push origin feature/foundation
   ```

5. On GitHub, open a **Pull Request** from the branch to `main` and merge it. Repeat for each branch in this order:

   `feature/foundation` → `feature/core-app` → `feature/automated-tests` → `feature/jenkins-ci` → `feature/dockerization` → `feature/kubernetes-orchestration`

6. Update your local `main` after each merge:

   ```bash
   git checkout main && git pull origin main
   ```

## 6. Step 3: Build the Flask Application

**Branch:** `feature/core-app`

1. Create the folders `app/`, `database/`, `tests/` and `k8s/`.
2. Create `requirements.txt`:

   ```
   Flask
   pytest
   pytest-cov
   gunicorn
   flake8
   ```

3. Build the app:
   - `database/db.py`: in-memory data store with seed data for students, faculty, courses, enrollments and grades.
   - `app/`: models, services (business logic) and routes (API endpoints).
   - `app/__init__.py`: Flask application factory that registers the routes.
   - `run.py`: starts the application.

4. Implement the business logic:
   - **GPA calculation** from grades.
   - **Enrollment checks** for conflicts and the **18-credit semester limit**.

5. Add the health endpoint `GET /api/health`. Docker and Kubernetes use it later to check that the app is alive.

6. Create the virtual environment, install dependencies and run:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python3 run.py
   ```

7. Test the endpoint in another terminal:

   ```bash
   curl http://localhost:5000/api/health
   ```

   Expected output: `{"service":"student-academic-platform","status":"UP"}`

## 7. Step 4: Write and Run Automated Tests

**Branch:** `feature/automated-tests`

1. Create tests in `tests/` covering:
   - GPA calculation
   - Enrollment conflict checks and the 18-credit rule
   - API endpoints, using Flask's `test_client`

2. Run the tests with coverage and a JUnit report:

   ```bash
   pytest -v --cov=app --cov-report=term-missing --junitxml=reports/test-results.xml tests/
   ```

3. Run the linter:

   ```bash
   flake8 .
   ```

All tests should pass before moving on. The JUnit XML file is used by Jenkins in the next step.

## 8. Step 5: Set Up Jenkins CI

**Branch:** `feature/jenkins-ci`

**Part A: Install Jenkins**

1. Install Java 17:

   ```bash
   sudo apt-get install -y openjdk-17-jre
   ```

2. Add the Jenkins repository and key, then install Jenkins:

   ```bash
   sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
   echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list
   sudo apt-get update && sudo apt-get install -y jenkins
   ```

3. Start Jenkins:

   ```bash
   sudo systemctl enable jenkins
   sudo systemctl start jenkins
   ```

4. Open `http://<server-ip>:8080` in a browser and unlock Jenkins with:

   ```bash
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```

5. Choose **Install suggested plugins** and create the admin user.

**Part B: Create the pipeline**

1. Add a declarative `Jenkinsfile` to the repo root with these stages:

   | Stage | Action |
   |-------|--------|
   | Checkout | Pull the code from GitHub |
   | Install dependencies | Create a venv and install `requirements.txt` |
   | Lint | Run `flake8` |
   | Test | Run `pytest` with coverage |
   | Publish report | Publish `reports/test-results.xml` using JUnit |

2. In Jenkins: **New Item → Pipeline**, set **Pipeline script from SCM**, choose Git and enter the GitHub repo URL.
3. Click **Build Now**.
4. Open the build's **Console Output** and **Test Result** pages to confirm a successful run.

## 9. Step 6: Dockerize the Application

**Branch:** `feature/dockerization`

1. Create a `Dockerfile` that:
   - uses a Python 3.11 base image
   - copies the project and installs `requirements.txt`
   - exposes port 5000
   - starts the app with Gunicorn (`gunicorn -w 2 -b 0.0.0.0:5000 ...`)

2. Create a `.dockerignore` (for example `venv/`, `__pycache__/`, `.git/`, `reports/`).

3. Build the image:

   ```bash
   docker build -t student-academic-platform:v1.0.0 .
   docker images
   ```

4. Run the container:

   ```bash
   docker run -d -p 5000:5000 --name student-container student-academic-platform:v1.0.0
   docker ps
   ```

5. Wait a few seconds for Gunicorn to start, then test:

   ```bash
   sleep 5
   curl http://localhost:5000/api/health
   ```

6. Clean up when finished:

   ```bash
   docker stop student-container && docker rm student-container
   ```

## 10. Step 7: Deploy on Kubernetes (Minikube)

**Branch:** `feature/kubernetes-orchestration`

**Part A: Write the manifests**

- `k8s/deployment.yaml`: 3 replicas, `imagePullPolicy: Never`, readiness and liveness probes on `/api/health`.
- `k8s/service.yaml`: type `NodePort`, port 5000, nodePort 30090.

**Part B: Install Minikube and kubectl**

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64

curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl
rm kubectl

minikube version
kubectl version --client
```

**Part C: Start the cluster and deploy**

1. Start Minikube:

   ```bash
   minikube start --driver=docker
   ```

2. Build the image **inside Minikube's Docker** (required because of `imagePullPolicy: Never`):

   ```bash
   eval $(minikube docker-env)
   docker build -t student-academic-platform:v1.0.0 .
   ```

3. Apply the manifests:

   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

4. Verify 3 healthy pods and the service:

   ```bash
   kubectl get pods -o wide
   kubectl get svc student-service
   ```

   Expected: 3 pods `1/1 Running` and `5000:30090/TCP`.

**Part D: Self-healing test**

1. Delete one pod:

   ```bash
   kubectl delete pod <pod-name>
   ```

2. Watch Kubernetes create a replacement:

   ```bash
   kubectl get pods -w
   ```

   A new pod appears automatically and the count returns to 3.

**Part E: Access the application**

1. In one terminal, run (keep it open):

   ```bash
   minikube service student-service --url
   ```

2. In a second terminal, use the URL printed above:

   ```bash
   curl http://127.0.0.1:<port>/api/health
   ```

---

## 11. API Documentation

**Base URL:** `http://localhost:5000` | **Format:** JSON

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Application root |
| GET | `/api/health` | Service health check |
| GET | `/api/students` | List all students |
| POST | `/api/students` | Create a student |
| GET | `/api/students/<sid>` | Get one student |
| GET | `/api/students/<sid>/gpa` | Calculate a student's GPA |
| GET | `/api/courses` | List all courses |
| POST | `/api/enroll` | Enroll a student in a course |
| POST | `/api/grades` | Assign a grade |

**Health response:**

```json
{"service": "student-academic-platform", "status": "UP"}
```

**Business rule:** an enrollment is rejected if it would exceed **18 credits** in a semester or conflicts with an existing enrollment.

**Example requests:**

```bash
curl http://localhost:5000/api/health
curl http://localhost:5000/api/students
curl http://localhost:5000/api/courses
```

Replace `<sid>` with a student ID from the `/api/students` response, for example:

```bash
curl http://localhost:5000/api/students/<sid>/gpa
```

## 12. Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `curl` fails right after `docker run` | Gunicorn is still starting | Wait 5 seconds and retry |
| `ErrImageNeverPull` or `ImagePullBackOff` | Image is not in Minikube's Docker | Run `eval $(minikube docker-env)`, rebuild the image, then `kubectl rollout restart deployment student-platform-deployment` |
| Minikube URL stops working | The tunnel closed or the port changed | Keep the `minikube service --url` terminal open and use the new port |
| `curl: No such file or directory` | A placeholder like `<url>` was typed literally | Replace it with the real URL |
| `minikube start` fails | Docker is not running | Check `docker ps`, then run `sudo service docker start` |

## 13. Learnings

- **Version control:** one branch per feature with pull requests keeps history clean and reviewable.
- **Testing and CI:** automated linting and tests in Jenkins catch problems on every run.
- **Containerization:** Docker makes the app portable, and a health endpoint is essential for monitoring.
- **Orchestration:** Kubernetes keeps the desired number of replicas running and replaces failed pods automatically (self-healing).

## 14. Author

**Shubham**
B.Tech in Artificial Intelligence & Data Science, Sanjivani University, Kopargaon
