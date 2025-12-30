pipeline {
    agent any

    environment {
        IMAGE_NAME = "sum-image"
        DOCKER_REPO = "sanjaybalane/sum-image"
        TEST_FILE_PATH = "test_variables.txt"
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
                    // stop old container if exists
                    bat "docker stop null || echo already stopped"
                    bat "docker rm null || echo already removed"

                    bat "docker run -d --name null ${IMAGE_NAME}"
                    echo "Container started: null"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "Running tests..."

                    def testLines = readFile(TEST_FILE_PATH).split('\n')

                    for (line in testLines) {
                        if (line.trim()) {
                            def vars = line.split(' ')
                            def arg1 = vars[0]
                            def arg2 = vars[1]
                            def expectedSum = vars[2].toFloat()

                            echo "Testing ${arg1} + ${arg2}"

                            def output = bat(
                                script: "docker exec null python /app/sum.py ${arg1} ${arg2}",
                                returnStdout: true
                            )

                            def result = output.split('\n')[-1].trim().toFloat()

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

                    bat "docker tag ${IMAGE_NAME}:latest ${DOCKER_REPO}:latest"

                    def pushStatus = bat(
                        script: "docker push ${DOCKER_REPO}:latest",
                        returnStatus: true
                    )

                    if (pushStatus != 0) {
                        echo "⚠️ WARNING: Docker push failed (authorization / permission), continuing pipeline."
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
                bat "docker stop null || echo already stopped"
                bat "docker rm null || echo already removed"
            }
        }
    }
}
