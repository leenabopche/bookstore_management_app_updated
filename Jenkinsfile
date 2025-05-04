pipeline {
    agent any

    environment {
        IMAGE_NAME = 'bookstore_app_image'
        CONTAINER_NAME = 'bookstore_app_container'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build(IMAGE_NAME)
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    docker.image(IMAGE_NAME).inside {
                        sh 'python manage.py test'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh 'docker-compose down'
                    sh 'docker-compose up -d --build'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker system prune -f'
        }
    }
}
