pipeline {

  agent any

  options {
    buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
  }

  stages {

    stage('Hello') {
      steps {
        sh "echo Hello"
      }
    }
    stage('cat README') {
      when {
        branch "bug_fix*"
      }      
      steps {
        sh "cat README.md"
      }
    }    
    stage('Java version') {
      steps {
        sh '''
          java -version
        '''
      }
    }

  }

}
