pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                checkout scm
                script {
                    docker.withRegistry('https://registry.hub.docker.com/r/nikhil1996/hdoc_image/') {

                             def customImage = docker.build("nikhil1996/hdoc_image:${env.BUILD_ID}")

                            /* Push the container to the custom Registry */
                             customImage.push()
                    }
                }
            }
        }
    }
}

