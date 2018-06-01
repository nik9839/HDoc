pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                checkout scm
                script {
                    docker.withRegistry('https://hub.docker.com/r/nikhil1996/hdoc_image/') {

                             def customImage = docker.build("my-image:${env.BUILD_ID}")

                            /* Push the container to the custom Registry */
                             customImage.push()
                    }
                }
            }
        }
    }
}

