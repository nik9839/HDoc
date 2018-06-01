pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                checkout scm
                script {
                    docker.withRegistry('https://registry.hub.docker.com/r/nikhil1996/hdoc_image/','1e4db286-dfd3-4096-8943-e85714358c09') {

                             def customImage = docker.build("nikhil1996/hdoc_image:${env.BUILD_ID}")

                            /* Push the container to the custom Registry */
                             customImage.push()
                    }
                }
            }
        }
    }
}

