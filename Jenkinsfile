pipeline {
    agent any

    environment {
        // Required by the project statement
        IMAGE_NAME      = "sum-image"
        CONTAINER_NAME  = "sum-container"
        CONTAINER_ID    = ""          // will be filled in Run stage
        DIR_PATH        = "${WORKSPACE}"
        SUM_PY_PATH     = "${WORKSPACE}/sum.py"
        TEST_FILE_PATH  = "${WORKSPACE}/test_variables.txt"

        // DockerHub deploy
        DOCKERHUB_REPO  = "sanjaybalane/sum-image"
        DOCKER_CREDS_ID = "dockerhub-creds"   // must match Jenkins credential ID
    }

    stages {

        /*-------------------  STEP 2 : BUILD  -------------------*/
        stage('Build') {
            steps {
                script {
                    echo "Building Docker image..."
                    bat "docker build -t ${env.IMAGE_NAME} ."
                }
            }
        }

        /*-------------------  STEP 3 : RUN  -------------------*/
        stage('Run') {
            steps {
                script {
                    echo "Starting container..."

                    // Run container and capture the ID
                    def output = bat(
                        script: "docker run -d --name ${env.CONTAINER_NAME} ${env.IMAGE_NAME}",
                        returnStdout: true
                    )

                    def lines = output.trim().split('\\r?\\n')
                    env.CONTAINER_ID = lines[lines.length - 1].trim()

                    echo "Container started with ID: ${env.CONTAINER_ID}"
                }
            }
        }

        /*-------------------  STEP 4 : TEST  -------------------*/
        stage('Test') {
            steps {
                script {
                    if (!env.CONTAINER_ID?.trim()) {
                        error "No container ID available, cannot run tests."
                    }

                    echo "Running tests from: ${env.TEST_FILE_PATH}"

                    def testLines = readFile(env.TEST_FILE_PATH).trim().split('\\r?\\n')

                    for (line in testLines) {
                        if (!line.trim()) {
                            continue
                        }

                        def vars = line.split('\\s+')
                        def arg1 = vars[0]
                        def arg2 = vars[1]
                        def expectedSum = vars[2].toFloat()

                        echo "Testing ${arg1} + ${arg2}"

                        def out = bat(
                            script: "docker exec ${env.CONTAINER_ID} python /app/sum.py ${arg1} ${arg2}",
                            returnStdout: true
                        )

                        // take the last token from the output as the result
                        def tokens = out.trim().split('\\s+')
                        def result = tokens[tokens.length - 1].toFloat()

                        if (result == expectedSum) {
                            echo "SUCCESS: ${arg1} + ${arg2} = ${result}"
                        } else {
                            error "FAIL: ${arg1} + ${arg2} expected ${expectedSum} but got ${result}"
                        }
                    }
                }
            }
        }

        /*-------------------  STEP 6 : DEPLOY TO DOCKERHUB  -------------------*/
        stage('Deploy') {
            steps {
                script {
                    echo "Deploying image to DockerHub..."

                    withCredentials([usernamePassword(
                        credentialsId: env.DOCKER_CREDS_ID,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        // Login using Jenkins credentials
                        bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"

                        // Tag and push
                        bat "docker tag ${env.IMAGE_NAME}:latest ${env.DOCKERHUB_REPO}:latest"
                        bat "docker push ${env.DOCKERHUB_REPO}:latest"
                    }

                    echo "Image successfully pushed to DockerHub"
                }
            }
        }
    }

    /*-------------------  STEP 5 : POST (CLEANUP)  -------------------*/
    post {
        always {
            script {
                echo "Cleaning container..."

                if (env.CONTAINER_ID?.trim()) {
                    bat "docker stop ${env.CONTAINER_ID} || echo already stopped"
                    bat "docker rm ${env.CONTAINER_ID} || echo already removed"
                } else {
                    echo "No container to clean."
                }
            }
        }
    }
}

