pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                checkout scm
                script {
                    def customimage = docker.build("my-image:${env.BUILD_ID}")
                }
            }
        }
    }
}

