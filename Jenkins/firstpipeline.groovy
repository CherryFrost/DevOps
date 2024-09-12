pipeline {
    agent any
    stages {
        stage('Clone a repo') {
            steps {
                git branch: 'main', url:"https://github.com/CherryFrost/DevOps.git"
            }
        }
        stage('Execute script'){
            steps{
                sh "chmod +x script1.sh"
                sh "./script1.sh"
            }
        }
    }
}