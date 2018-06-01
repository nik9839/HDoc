pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                checkout scm
                script {
                        def customImage = docker.build("nikhil1996/hdoc_image:${env.BUILD_ID}")

                }
            }
        }
    }
}

