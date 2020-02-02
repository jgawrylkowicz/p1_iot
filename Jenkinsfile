pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh './build-images.sh'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}