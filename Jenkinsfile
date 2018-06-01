pipeline {
    agent { docker { image 'python:3.5.1' } }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                echo "hello world"
                checkout scm
                docker.build("my-image:${env.BUILD_ID}")

            }
        }
    }
}

