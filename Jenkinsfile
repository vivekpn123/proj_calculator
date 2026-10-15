pipeline {
    agent any
    environment {
        IMAGE_NAME = 'colourful-calculator'
        CONTAINER_NAME = 'colourful-calculator'
        APP_PORT = '5000'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install test dependencies') {
            steps {
                sh 'python3 -m venv .venv && . .venv/bin/activate && pip install --upgrade pip && pip install -r requirements-dev.txt'
            }
        }
        stage('Unit tests') {
            steps { sh '. .venv/bin/activate && pytest -q' }
        }
        stage('Build Docker image') {
            steps { sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .' }
        }
        stage('Test built image') {
            steps {
                sh '''
                    set -eu
                    docker rm -f ${CONTAINER_NAME}-test >/dev/null 2>&1 || true
                    docker run -d --name ${CONTAINER_NAME}-test -p 127.0.0.1:15000:5000 ${IMAGE_NAME}:${BUILD_NUMBER}
                    trap 'docker rm -f ${CONTAINER_NAME}-test >/dev/null 2>&1 || true' EXIT
                    for i in $(seq 1 20); do
                      if curl -fsS http://127.0.0.1:15000/ >/dev/null; then break; fi
                      sleep 2
                    done
                    curl -fsS http://127.0.0.1:15000/ | grep -q 'Colourful Calculator'
                    curl -fsS -X POST http://127.0.0.1:15000/calculate -H 'Content-Type: application/json' -d '{"a":8,"b":2,"op":"multiply"}' | grep -q '"result":16'
                '''
            }
        }
        stage('Deploy on Jenkins host') {
            steps {
                sh '''
                    docker rm -f ${CONTAINER_NAME} >/dev/null 2>&1 || true
                    docker run -d --restart unless-stopped --name ${CONTAINER_NAME} -p ${APP_PORT}:5000 ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
    }
    post {
        always { sh 'docker rm -f ${CONTAINER_NAME}-test >/dev/null 2>&1 || true' }
    }
}
