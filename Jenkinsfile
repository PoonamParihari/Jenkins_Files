pipeline{
  agent { label 'slave1 || slave2' }
  environment {
        def NOTIFICATION_EMAIL = "poopari36@gmail.com"
              }
  tools {
    maven 'maven36'
        }
  
  stages{
    stage('SCM') { 
      steps{
         deleteDir()
         git branch: 'dev', changelog: false, credentialsId: 'credential_id', poll: false, url: '${Git_URL}'
         sh "echo pwd ${WORKSPACE}"
         sh "echo ${mvnHome}"
           }
        }

    stage('SonarQube Analysis') { 
      options{
             timeout(time: 10)
             }
      steps{
        script{
          try{
              dir("${Application_Name}"){
              withSonarQubeEnv('Sonarqube_Provided') {
                sh "'${sonarMvnHome}/bin/mvn' -Dmaven.test.failure.ignore  $SONAR_MAVEN_GOAL -Dsonar.host.url=${SONAR_HOST_URL} "
                                              }
                            }
              }
          catch(e){
              //currentBuild.result = "UNSTABLE"
              //notifyFailed()
            emailext body: "<br><br>Job logs can be seen at " + "${BUILD_URL}" + "console", recipientProviders: [[$class: 'RequesterRecipientProvider']],
            subject: "Sonarscan Failed - ${JOB_NAME} - ${BUILD_DISPLAY_NAME}", to: "${env.NOTIFICATION_EMAIL}"
            message: """
                     Sonarscan Failed - ${JOB_NAME}- ${BUILD_DISPLAY_NAME}. 
                     """,
            status: "Failure",
            color: "RED"
                //throw e
                  }
                }
               }
            } 

    stage('Build EAR') {
      options{
             timeout(time: 10)
             }
      steps{
        script{
          try{
            sh '''
              BUILDID=$BUILD_NUMBER
              git tag jenkins-build-$y
              git push <git_url> jenkins-build-$y
              ''' 
              // Run the maven build to Build the EAR Artifact
            sh "'${mvnHome}/bin/mvn' --f ${APPLICATION_NAME}.parent/pom.xml clean package"
            sh " cp $WORKSPACE/${APPLICATION_NAME}/target/*.ear $WORKSPACE"
            def response
              response = sh(script: '''
                           Application_Name='''+APPLICATION_NAME+'''
                           name=$(basename '''+APPLICATION_NAME+'''/target/*.ear .ear)
                           name2=$(echo $name|sed -e 's#.*_\\(\\)#\\1#')
                           echo $name2 | tr -d '\n'
                               ''',
                           returnStdout: true,
                            )
            println(response)
            Version = response
            println("EAR Version is " + Version)
          }
          catch (e){
            emailext body: "<br><br>Job logs can be seen at " + "${BUILD_URL}" + "console", recipientProviders: [[$class: 'RequesterRecipientProvider']],
            subject: "Appname EAR Build Failed - ${JOB_NAME} - ${BUILD_DISPLAY_NAME}", to: "${env.NOTIFICATION_EMAIL}"
               message: """
                        Appname EAR Build Failed - ${JOB_NAME}- ${BUILD_DISPLAY_NAME}. 
                        """,
               status: "Failure",
               color: "RED"
            throw e
              }
            }
          }
        }
  
    stage('Artifactory Upload'){
      options{
             timeout(time: 10)
             }
      steps{
        script{
          try{
            println("EAR Version is " + Version)
            def server = Artifactory.server('Artifactory_Name')
            def uploadSpec = """{
                          "files": [
                            {
                              "pattern": "${APPLICATION_NAME}/target/*.ear",
                              "target": "${Artifactory_Repo}"
                            }
                          ]
                        }"""
            server.upload(uploadSpec)
              }
          catch (e){
            emailext body: "<br><br>Job logs can be seen at " + "${BUILD_URL}" + "console", recipientProviders: [[$class: 'RequesterRecipientProvider']],
            subject: "Appname Artifactory Upload Failed - ${JOB_NAME} - ${BUILD_DISPLAY_NAME}", to: "${env.NOTIFICATION_EMAIL}"
               message: """
                        Appname Artifactory Upload Failed - ${JOB_NAME}- ${BUILD_DISPLAY_NAME}. 
                        """,
               status: "Failure",
               color: "RED"
            throw e
                }
              }
            } 
      }
  
    stage('Build Image') {
      options{
             timeout(time: 10)
             }
      steps{
        script{
          try{
               println("Build Image Version is " + Version)
               sh "sed -i -e 's/1.0.0/$Version/g' $WORKSPACE/Dockerfile"
               docker.withRegistry('docker_hub_url', 'docker_registry_cred'){
               docker.build("$docker_repo_name:$Version")
              }
           sh "docker tag $docker_repo_name:$Version docker_hub_url/$docker_repo_name:$Version"
           sh "docker images"
             }
          catch (e){
            emailext body: "<br><br>Job logs can be seen at " + "${BUILD_URL}" + "console", recipientProviders: [[$class: 'RequesterRecipientProvider']],
            subject: "APPname Docker Image Build Failed - ${JOB_NAME} - ${BUILD_DISPLAY_NAME}", to: "${env.NOTIFICATION_EMAIL}"
            office365ConnectorSend webhookUrl: "${NPCHANNELWEBHOOKURL}",
               message: """
                        Appname Docker Image Build Failed - ${JOB_NAME}- ${BUILD_DISPLAY_NAME}. 
                        """,
               status: "Failure",
               color: "RED"
            throw e
                   }
            }
        }   
    }

    stage('Docker Push') {
      options{
             timeout(time: 10)
             }
      steps{
        script{
          try{  
            println("Push Image Version is " + Version)
            docker.withRegistry('docker_hub_url', 'docker_registry_cred') {
            docker.image("docker_hub/$docker_repo_name:$Version").push("$Version")
             }
            }
        catch(e){
            emailext body: "<br><br>Job logs can be seen at " + "${BUILD_URL}" + "console", recipientProviders: [[$class: 'RequesterRecipientProvider']],
            subject: "Appname Docker Push Failed - ${JOB_NAME} - ${BUILD_DISPLAY_NAME}", to: "${env.NOTIFICATION_EMAIL}"
            office365ConnectorSend webhookUrl: "${NPCHANNELWEBHOOKURL}",
               message: """
                        Appname Docker Push Failed - ${JOB_NAME}- ${BUILD_DISPLAY_NAME}. 
                        """,
               status: "Failure",
               color: "RED"
            throw e
          }
        finally{
           sh "docker rmi -f  docker_hub_name/$docker_repo_name:$Version"
           sh "docker rmi -f  $docker_repo_name:$Version"
          }
      }
    }
  }
  }
  }
