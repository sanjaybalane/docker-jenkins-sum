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

                    // unique container name per build
                    env.CONTAINER_ID = "sum-container-${env.BUILD_NUMBER}"

                    // start container detached
                    bat "docker run -d --name ${env.CONTAINER_ID} ${env.IMAGE_NAME}"

                    echo "Container started: ${env.CONTAINER_ID}"
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "Running tests..."

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
    
                def dockerRepo = "sanjaybalane/sum-image"
    
                bat """
                    docker tag sum-image:latest ${dockerRepo}:latest
                    docker push ${dockerRepo}:latest
                """
    
                echo "Image successfully pushed to DockerHub"
            }
    }
}

