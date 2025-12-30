pipeline {
    agent any

    environment {
        IMAGE_NAME     = "sum-image"
        CONTAINER_ID   = ""
        SUM_PY_PATH    = "/app/sum.py"
        DIR_PATH       = "."
        TEST_FILE_PATH = "test_variables.txt"
        DOCKER_REPO    = "sanjaybalane/sum-image"
    }

    stages {

        stage('Build') {
            steps {
                echo "Building Docker image..."
                bat "docker build -t ${env.IMAGE_NAME} ${env.DIR_PATH}"
            }
        }

        stage('Run') {
            steps {
                script {
                    echo "Starting container..."

                    env.CONTAINER_ID = "sum-container-${env.BUILD_NUMBER}"

                    bat "docker run -d --name ${env.CONTAINER_ID} ${env.IMAGE_NAME}"

                    echo "Container started: ${env.CONTAINER_ID}"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'

                    def testLines = readFile(env.TEST_FILE_PATH).split('\n')

                    for (line in testLines) {
                        line = line.trim()
                        if (!line) continue

                        def vars = line.split(' ')
                        def arg1 = vars[0]
                        def arg2 = vars[1]
                        def expectedSum = vars[2].toFloat()

                        echo "Testing ${arg1} + ${arg2}"

                        def output = bat(
                            script: "docker exec ${env.CONTAINER_ID} python ${env.SUM_PY_PATH} ${arg1} ${arg2}",
                            returnStdout: true
                        )

                        def resultStr = output.split('\n')[-1].trim()
                        def result = resultStr.toFloat()

                        if (result == expectedSum) {
                            echo "SUCCESS: ${arg1} + ${arg2} = ${result}"
                        } else {
                            error "FAILED: Expected ${expectedSum} but got ${result}"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Deploying image to DockerHub..."

                    bat "docker tag ${env.IMAGE_NAME}:latest ${env.DOCKER_REPO}:latest"

                    bat "docker push ${env.DOCKER_REPO}:latest"

                    echo "Image successfully pushed to DockerHub"
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Cleaning container..."
                bat(returnStatus: true, script: "docker stop ${env.CONTAINER_ID}")
                bat(returnStatus: true, script: "docker rm ${env.CONTAINER_ID}")
            }
        }
    }
}

