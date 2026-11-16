# Docker + Jenkins pipeline for a Python sum script

A Jenkins pipeline that builds a Docker image around a small Python script (sum.py), runs it in a container, tests it with a list of test cases, and pushes the image to Docker Hub.

## Files

- sum.py: takes two numbers as arguments and prints their sum. It prints an error and exits if the arguments are missing or are not numbers.
- Dockerfile: Python 3.13 on Alpine, copies sum.py into /app and keeps the container running so Jenkins can use docker exec.
- Jenkinsfile: the pipeline.
- test_variables.txt: test cases, one per line, in the format "a b expected_sum".

## Pipeline stages

1. Build: docker build of the image (sum-image).
2. Run: starts the container in the background and saves its ID.
3. Test: reads test_variables.txt, runs sum.py inside the container for each line with docker exec, and fails the build if a result does not match the expected sum.
4. Deploy: logs in to Docker Hub with Jenkins credentials, tags the image and pushes it.

## Tools

Jenkins (declarative pipeline, Windows agent), Docker, Docker Hub, Python.

## Setup

1. Create a Jenkins credential of type username with password for Docker Hub, with the ID dockerhub-creds.
2. Create a Pipeline job that uses this repository and its Jenkinsfile.
3. Change DOCKERHUB_REPO in the Jenkinsfile to your own Docker Hub repository.
4. Run the job.
