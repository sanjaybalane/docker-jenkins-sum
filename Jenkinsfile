stage('Deploy') {
    steps {
        script {
            echo "Deploying image to DockerHub..."

            def dockerRepo = "sanjaybalane/sum-image"

            // Tag image
            bat "docker tag ${env.IMAGE_NAME}:latest ${dockerRepo}:latest"

            // Push image
            bat "docker push ${dockerRepo}:latest"

            echo "Image successfully pushed to DockerHub"
        }
    }
}
