# Colourful Calculator

A small Flask calculator with a colourful responsive webpage, automated tests, and a Docker image.

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
python app.py
```
Open http://localhost:5000.

## Docker
```bash
docker build -t colourful-calculator:local .
docker run --rm -p 5000:5000 colourful-calculator:local
```
Open http://localhost:5000.

## Jenkins
The Jenkinsfile checks out Git, runs unit tests, builds a Docker image, smoke-tests the image, and deploys the container on the Jenkins host at port 5000. The Jenkins agent needs Python 3, venv/pip, Docker CLI/daemon, curl, and permission to use Docker.

This starter deploys to the Jenkins host. Deploying to separate EC2 servers is a follow-up step and should use SSH/credentials or a container registry.

## GitHub webhook
Create a Jenkins Pipeline job configured as **Pipeline script from SCM**, select Git and enter the GitHub repository URL, then enable the GitHub push trigger. In GitHub repository Settings → Webhooks, add `https://YOUR-JENKINS-DOMAIN/github-webhook/`. Jenkins must be securely reachable from GitHub over HTTPS; do not expose an unsecured Jenkins instance publicly.

Flow: Git push → webhook → Jenkins checkout → unit tests → Docker image build → image smoke test → deploy.
