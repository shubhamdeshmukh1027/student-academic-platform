pipeline {
    agent any
    environment {
        IMAGE = 'student-academic-platform:v1.0.0'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Lint') {
            steps {
                sh '. venv/bin/activate && flake8 app database tests --max-line-length=100'
            }
        }
        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    mkdir -p reports
                    pytest -v --cov=app --junitxml=reports/test-results.xml tests/
                '''
            }
            post {
                always { junit 'reports/test-results.xml' }
            }
        }
        stage('Docker Build') {
            steps { sh 'docker build -t $IMAGE .' }
        }
    }
    post {
        success { echo 'Pipeline succeeded' }
        failure { echo 'Pipeline failed' }
    }
}
