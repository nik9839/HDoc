pipeline {
    agent { docker { image 'python:3.5.1' } }
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

