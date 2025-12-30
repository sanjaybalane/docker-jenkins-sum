pipeline {
    agent any

    environment {
        IMAGE_NAME    = "sum-image"
        DOCKER_REPO   = "sanjaybalane/sum-image"
        TEST_FILE_PATH = "test_variables.txt"
        CONTAINER_ID  = ""          // will be filled in Run stage
    }

    stages {

        stage('Build') {
            steps {
                script {
                    echo "Building Docker image..."
                    bat "docker build -t ${IMAGE_NAME} ."
                }
            }
        }

        stage('Run') {
            steps {
                script {
                    echo "Starting container..."

                    // Start a new container in detached mode and capture its ID
                    def out = bat(
                        script: "docker run -d ${IMAGE_NAME}",
                        returnStdout: true
                    )

                    def lines = out.split('\n')
                    env.CONTAINER_ID = lines[lines.size() - 1].trim()

                    echo "Container started with ID: ${env.CONTAINER_ID}"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "Running tests..."

                    if (!env.CONTAINER_ID?.trim()) {
                        error "No container ID available, cannot run tests."
                    }

                    def testLines = readFile(TEST_FILE_PATH).split('\n')

                    for (line in testLines) {
                        line = line.trim()
                        if (line) {
                            def vars = line.split(' ')
                            def arg1 = vars[0]
                            def arg2 = vars[1]
                            def expectedSum = vars[2].toFloat()

                            echo "Testing ${arg1} + ${arg2}"

                            def output = bat(
                                script: "docker exec ${env.CONTAINER_ID} python /app/sum.py ${arg1} ${arg2}",
                                returnStdout: true
                            )

                            def resultLine = output.split('\n')[-1].trim()
                            def result = resultLine.replace("Sum:", "").trim().toFloat()

                            if (result == expectedSum) {
                                echo "SUCCESS: ${arg1} + ${arg2} = ${result}"
                            } else {
                                error "FAILED: Expected ${expectedSum} but got ${result}"
                            }
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Deploying image to DockerHub..."

                    // Tag local image -> DockerHub repo
                    bat "docker tag ${IMAGE_NAME}:latest ${DOCKER_REPO}:latest"

                    // Try to push, but do not fail the whole pipeline if it errors
                    def pushStatus = bat(
                        script: "docker push ${DOCKER_REPO}:latest",
                        returnStatus: true
                    )

                    if (pushStatus != 0) {
                        echo "WARNING: Docker push failed (authorization/permissions), but pipeline will continue."
                    } else {
                        echo "Image successfully pushed to DockerHub"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Cleaning container..."
                if (env.CONTAINER_ID?.trim()) {
                    bat(script: "docker stop ${env.CONTAINER_ID}", returnStatus: true)
                    bat(script: "docker rm ${env.CONTAINER_ID}", returnStatus: true)
                } else {
                    echo "No container to clean."
                }
            }
        }
    }
}
