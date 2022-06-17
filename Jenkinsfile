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


    stage('Java version') {
      steps {
        sh '''
          java -version
        '''
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

    stage('merge fix to main') {
      when {
        branch "main"
      }
      steps {
        sh "echo mergin bug_fix to main"
        sh 'git checkout main'
        sh 'git pull'
        sh 'git merge origin/bug_fix_345'
        sh 'git commit -am "Merged bug_fix_345 branch to main"'
        sh "git push origin main"
      }
    }
  }
}
