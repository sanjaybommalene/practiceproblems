# Jenkins: Advanced Topics
https://codefresh.io/learn/jenkins/
https://www.tutorialspoint.com/jenkins/jenkins_quick_guide.htm
## Introduction

Jenkins is a leading open-source automation server used to automate building, testing, and deploying software. It supports continuous integration (CI) and continuous delivery (CD), enabling teams to deliver high-quality software faster. Jenkins is highly extensible, with a rich ecosystem of plugins for integrating with various tools and platforms.
Jenkins Job:
A job is a project within Jenkins that defines a specific task or workflow. It can be a build process, a testing suite, or a deployment procedure. 
Jenkins Pipeline:
A pipeline is a way to define the steps in a job, allowing for visualization of the workflow and automated execution. It essentially provides a structured way to define the tasks that a job performs. 
Jenkins Agent:
An agent is a machine or a container that Jenkins uses to execute the tasks defined in a pipeline or job. It's like a worker that performs the actual execution of the job instructions. 
Relationship:
Jobs are defined using pipelines. When a job is triggered, it runs the pipeline, and the pipeline steps are then executed by the Jenkins agents. 

---

## Integrating Jenkins with Git Repositories

### 1. Installing Git Plugin

- Go to **Manage Jenkins > Manage Plugins**.
- Search for and install the **Git plugin**.

### 2. Configuring Git in Jenkins

- In **Manage Jenkins > Global Tool Configuration**, add your Git installation path.
- Configure credentials for private repositories under **Credentials**.

### 3. Creating a Jenkins Job with Git Integration

- Create a new **Freestyle** or **Pipeline** job.
- In the **Source Code Management** section, select **Git**.
- Enter the repository URL and credentials.
- Optionally, specify branches to build (e.g., `main`, `develop`).

---

## Running Tests on Commit

### 1. Polling the Repository

- In the job configuration, under **Build Triggers**, select **Poll SCM**.
- Use a cron syntax (e.g., `H/5 * * * *`) to check for changes every 5 minutes.

### 2. Webhooks

- Configure a webhook in your Git hosting service (GitHub, GitLab, Bitbucket) to notify Jenkins of new commits.
- Jenkins will trigger the job automatically on each push.

### 3. Running Tests

- Add a **Build Step** (e.g., **Execute Shell**) to run your test commands:
    ```sh
    ./gradlew test
    # or
    mvn test
    ```

---

## Deploying Artifacts to a Kubernetes Cluster

### 1. Building and Publishing Artifacts

- Use build tools (Maven, Gradle, npm) to package your application.
- Store artifacts in a repository (e.g., JFrog Artifactory, Nexus).

### 2. Building Docker Images

- Add a build step to build and push Docker images:
    ```sh
    docker build -t myapp:${BUILD_NUMBER} .
    docker push myrepo/myapp:${BUILD_NUMBER}
    ```

### 3. Deploying to Kubernetes

- Use the **Kubernetes CLI** (`kubectl`) or **Helm** in a build step:
    ```sh
    kubectl set image deployment/myapp myapp=myrepo/myapp:${BUILD_NUMBER} --record
    # or with Helm
    helm upgrade myapp ./chart --set image.tag=${BUILD_NUMBER}
    ```
- Configure Kubernetes credentials in Jenkins (via secrets or plugins).

---

## Real-World Pipeline Example (Jenkinsfile)

```groovy
pipeline {
        agent any

        environment {
                REGISTRY = 'myrepo'
                IMAGE = 'myapp'
                KUBE_CONFIG = credentials('kubeconfig-cred-id')
        }

        stages {
                stage('Checkout') {
                        steps {
                                git branch: 'main', url: 'https://github.com/org/repo.git'
                        }
                }
                stage('Build') {
                        steps {
                                sh 'mvn clean package'
                        }
                }
                stage('Test') {
                        steps {
                                sh 'mvn test'
                        }
                }
                stage('Build Docker Image') {
                        steps {
                                sh 'docker build -t $REGISTRY/$IMAGE:$BUILD_NUMBER .'
                                sh 'docker push $REGISTRY/$IMAGE:$BUILD_NUMBER'
                        }
                }
                stage('Deploy to Kubernetes') {
                        steps {
                                withCredentials([file(credentialsId: 'kubeconfig-cred-id', variable: 'KUBECONFIG')]) {
                                        sh 'kubectl set image deployment/myapp myapp=$REGISTRY/$IMAGE:$BUILD_NUMBER --kubeconfig=$KUBECONFIG'
                                }
                        }
                }
        }
        post {
                always {
                        junit '**/target/surefire-reports/*.xml'
                }
                failure {
                    slackSend channel: '#alerts', message: "Build ${BUILD_NUMBER} failed!"
                }
        }
}
```

```
pipeline {
  agent none
  stages {
    stage('Build & Test') {
      agent {
        docker {
          image 'maven:3.8-openjdk-11'
          args '-v $HOME/.m2:/root/.m2'
        }
      }
      steps {
        sh 'mvn clean package'
      }
    }
    stage('Build Docker Image') {
      agent {
        kubernetes {
          yaml """
            spec:
              containers:
              - name: docker
                image: docker:24.0
                command: ["cat"]
                tty: true
                volumeMounts:
                - mountPath: /var/run/docker.sock
                  name: docker-sock
              volumes:
              - name: docker-sock
                hostPath:
                  path: /var/run/docker.sock
          """
        }
      }
      steps {
        container('docker') {
          sh 'docker build -t my-app:${BUILD_NUMBER} .'
          sh 'docker push my-registry/my-app:${BUILD_NUMBER}'
        }
      }
    }
    stage('Deploy to K8s') {
      agent any
      steps {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
          sh 'kubectl apply -f k8s/'
        }
      }
    }
  }
}
```
---

## Troubleshooting Q&A

### Q1: Jenkins can't connect to my Git repository.

- **A:** Check repository URL, credentials, and network/firewall settings. Ensure the Git plugin is installed.

### Q2: Builds are not triggered on commit.

- **A:** Verify webhook configuration in your Git service. Check Jenkins job triggers and logs for errors.

### Q3: Docker build fails due to permission issues.

- **A:** Ensure Jenkins agent has Docker installed and the user is in the `docker` group. sudo usermod -aG docker jenkins

### Q4: Deployment to Kubernetes fails.

- **A:** Check Kubernetes credentials, context, and network access. Validate `kubectl` or `helm` commands manually.

### Q5: Tests are not being detected.

- **A:** Confirm test reports are generated in the expected location. Update the `junit` step in the pipeline accordingly.

---

## Conclusion

Jenkins is a powerful tool for automating the software delivery process. By integrating with Git, running automated tests, building artifacts, and deploying to Kubernetes, Jenkins enables robust CI/CD pipelines. With proper configuration and troubleshooting, Jenkins can streamline your DevOps workflows.


## Real World Example:
pipeline {
    agent {
        kubernetes { // Run on Kubernetes (optional, can use `agent any` for non-K8s)
            label 'jenkins-agent-pod'
            yamlFile 'k8s-pod-template.yaml' // Custom pod template (optional)
        }
    }
    options {
        skipStagesAfterUnstable() // Skip further stages if current stage is unstable
        timeout(time: 1, unit: 'HOURS') // Global timeout
    }
    environment {
        // Cache directory (shared across stages)
        CACHE_DIR = '/tmp/jenkins_cache'
        // K8s deployment name (for monitoring)
        DEPLOYMENT_NAME = 'my-app'
        NAMESPACE = 'default'
    }
    stages {
        // ----------------------------
        // 1. DEPENDENCY RESOLUTION
        // ----------------------------
        stage('Resolve Dependencies') {
            steps {
                script {
                    // Use cached dependencies if available (faster execution)
                    if (fileExists("${env.CACHE_DIR}/dependencies.lock")) {
                        echo "Using cached dependencies..."
                        sh "cp -r ${env.CACHE_DIR}/. ./"
                    } else {
                        echo "Fetching fresh dependencies..."
                        sh 'npm install' // Example for Node.js (replace with your tool)
                        sh "mkdir -p ${env.CACHE_DIR} && cp -r node_modules ${env.CACHE_DIR}/"
                        sh "touch ${env.CACHE_DIR}/dependencies.lock"
                    }
                }
            }
        }

        // ----------------------------
        // 2. BUILD (with explicit ordering dependency)
        // ----------------------------
        stage('Build') {
            // Run ONLY after 'Resolve Dependencies' succeeds
            dependsOn 'Resolve Dependencies' // Explicit ordering
            steps {
                sh 'mvn package' // Example for Java (replace as needed)
            }
        }

        // ----------------------------
        // 3. MANUAL APPROVAL STAGE
        // ----------------------------
        stage('Manual Approval') {
            input {
                message "Deploy to production?"
                ok "Deploy"
                submitter "admin,ops-team"
                parameters {
                    choice(choices: ['Yes', 'No'], name: 'CONFIRM')
                }
            }
            steps {
                echo "Approved by ${submitter}"
            }
        }

        // ----------------------------
        // 4. DEPLOY TO K8S (with failure handling)
        // ----------------------------
        stage('Deploy to Kubernetes') {
            // Run even if previous stages failed (e.g., for cleanup)
            when {
                expression { params.CONFIRM == 'Yes' }
            }
            steps {
                script {
                    try {
                        // Deploy using kubectl/helm
                        sh 'kubectl apply -f k8s-manifests/'
                        
                        // Monitor deployment status
                        timeout(time: 5, unit: 'MINUTES') {
                            sh """
                            kubectl rollout status deployment/${DEPLOYMENT_NAME} \
                                -n ${NAMESPACE} \
                                --timeout=300s
                            """
                        }
                    } catch (err) {
                        echo "Deployment failed! Initiating rollback..."
                        // Rollback to previous version
                        sh 'kubectl rollout undo deployment/${DEPLOYMENT_NAME} -n ${NAMESPACE}'
                        error("Deployment failed and was rolled back") // Fail the stage
                    }
                }
            }
        }

        // ----------------------------
        // 5. POST-DEPLOY TEST (always runs)
        // ----------------------------
        stage('Smoke Tests') {
            // Run even if previous stages failed
            when {
                expression { !currentBuild.resultIsWorseOrEqualTo('FAILURE') }
            }
            steps {
                script {
                    // Continue on failure (e.g., for non-critical tests)
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                        sh 'npm run test:smoke'
                    }
                }
            }
        }
    }

    // ----------------------------
    // POST-ACTIONS (Cleanup/Notifications)
    // ----------------------------
    post {
        always {
            echo "Pipeline completed with status: ${currentBuild.currentResult}"
            // Cleanup (e.g., delete temp files)
            sh "rm -rf ${env.WORKSPACE}/tmp"
        }
        failure {
            slackSend channel: '#alerts', message: "Pipeline failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        }
        success {
            archiveArtifacts artifacts: '**/target/*.jar' // Example for Java
        }
    }
}