# **GitLab CI/CD Pipelines: Complete Guide with Docker & Kubernetes Integration**

GitLab CI/CD provides a powerful, container-native approach to automating builds, tests, and deployments. Below is a comprehensive breakdown of how to leverage Docker and Kubernetes in GitLab pipelines.

# Best Example
Below is a comprehensive example of a `.gitlab-ci.yml` file that includes as many GitLab CI/CD keywords and verbs as possible, with detailed comments explaining each section and keyword. This file is structured to demonstrate the breadth of GitLab CI/CD configuration options while maintaining a realistic and functional pipeline structure. Note that not every possible keyword combination is included (as some are mutually exclusive or context-specific), but this covers the majority of commonly used keywords and verbs, organized logically.

```yaml
# The `default` keyword defines settings that apply to all jobs unless overridden.
default:
  image: ubuntu:20.04  # Specifies the default Docker image for all jobs.
  retry:  # Configures automatic retry for failed jobs.
    max: 2  # Maximum number of retries.
    when:  # Conditions under which to retry.
      - runner_system_failure
      - stuck_or_timeout_failure
  timeout: 1h  # Default timeout for all jobs.
  interruptible: true  # Allows jobs to be canceled if a new pipeline starts.
  before_script:  # Commands to run before each job's script.
    - echo "Setting up environment"
    - apt-get update && apt-get install -y curl
  after_script:  # Commands to run after each job's script, even if it fails.
    - echo "Cleaning up environment"
  artifacts:  # Defines artifacts to be stored after job execution.
    paths:
      - output/
    expire_in: 1 week  # Artifacts expire after 1 week.
    when: always  # Artifacts are uploaded regardless of job status.

# The `stages` keyword defines the order of stage execution in the pipeline.
stages:
  - build  # Stage for building artifacts.
  - test   # Stage for running tests.
  - deploy # Stage for deployment.
  - review # Stage for review apps.
  - cleanup # Stage for cleanup tasks.

# The `variables` keyword defines pipeline-wide variables.
variables:
  GLOBAL_VAR: "This is a global variable"  # Available to all jobs.
  DEPLOY_ENV: "staging"  # Can be overridden in specific jobs.

# The `cache` keyword defines files/directories to cache between pipeline runs.
cache:
  key: ${CI_COMMIT_REF_SLUG}  # Cache key based on branch/tag name.
  paths:
    - vendor/  # Cache the vendor directory.
  policy: pull-push  # Cache is pulled and pushed (default behavior).

# The `include` keyword imports external YAML files into the pipeline.
include:
  - local: '/.gitlab/ci/templates/build.yml'  # Include a local file.
  - remote: 'https://example.com/templates/test.yml'  # Include a remote file.
  - template: 'Code-Quality.gitlab-ci.yml'  # Include a GitLab-provided template.
  - project: 'my-group/my-project'  # Include from another project.
    ref: 'main'
    file: '/.gitlab-ci.yml'

# Example job demonstrating build stage.
build_job:
  stage: build  # Assigns the job to the build stage.
  image: node:16  # Overrides default image for this job.
  script:  # Commands to execute for the job.
    - echo "Building the application"
    - npm install
    - npm run build
  artifacts:  # Job-specific artifacts configuration.
    paths:
      - dist/
    reports:  # Special artifacts for reports (e.g., test results).
      junit: test-results.xml
  cache:  # Job-specific cache configuration.
    key: build-cache
    paths:
      - node_modules/
  only:  # Run job only for specific conditions.
    refs:
      - main
      - branches
    variables:
      - $CI_COMMIT_MESSAGE =~ /build/
  except:  # Skip job for specific conditions.
    refs:
      - tags
  tags:  # Restrict job to runners with specific tags.
    - docker
    - linux
  when: on_success  # Run job only if previous jobs in the stage succeed.

# Example job demonstrating test stage with dependencies.
test_job:
  stage: test
  dependencies:  # Depends on artifacts from specified jobs.
    - build_job
  script:
    - echo "Running tests"
    - npm test
  coverage: '/\d+\.\d+%/'  # Extracts code coverage from job output.
  retry:  # Job-specific retry configuration.
    max: 1
    when:
      - script_failure
  allow_failure: true  # Job can fail without failing the pipeline.
  only:
    changes:  # Run job only if specific files change.
      - src/**/*.js
  when: always  # Run job regardless of previous job status.

# Example job demonstrating deploy stage with environment.
deploy_job:
  stage: deploy
  script:
    - echo "Deploying to $DEPLOY_ENV"
    - ./deploy.sh
  environment:  # Associates job with a deployment environment.
    name: $DEPLOY_ENV
    url: https://staging.example.com
    on_stop: stop_review  # Specifies job to run when environment stops.
  rules:  # Advanced control over when job runs (replaces only/except).
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: always
    - if: '$CI_COMMIT_BRANCH =~ /feature/'
      when: manual  # Job requires manual trigger.
      allow_failure: true
  needs:  # Specifies jobs that must complete before this one.
    - job: build_job
      artifacts: true
    - job: test_job
      artifacts: false
  trigger:  # Triggers a downstream pipeline.
    project: my-group/downstream-project
    branch: main
  resource_group: deploy-prod  # Ensures only one job runs at a time for this resource.

# Example job for stopping a review environment.
stop_review:
  stage: review
  script:
    - echo "Stopping review environment"
    - ./stop.sh
  environment:
    name: $DEPLOY_ENV
    action: stop  # Indicates this job stops the environment.
  when: manual  # Requires manual trigger to stop environment.
  variables:
    STOP_ENV: "true"  # Job-specific variable.

# Example job demonstrating parallel execution.
parallel_test:
  stage: test
  parallel:  # Runs multiple instances of the job in parallel.
    matrix:  # Defines matrix variables for parallel execution.
      - NODE_VERSION: ["14", "16", "18"]
        TEST_SUITE: ["unit", "integration"]
  script:
    - echo "Running $TEST_SUITE tests on Node $NODE_VERSION"
    - nvm use $NODE_VERSION
    - npm run test:$TEST_SUITE
  artifacts:
    paths:
      - test-output-$TEST_SUITE-$NODE_VERSION/

# Example job demonstrating DAST (Dynamic Application Security Testing).
dast_job:
  stage: test
  image: registry.gitlab.com/security-products/dast:latest
  script:
    - /analyzer run
  variables:
    DAST_BROWSER_SCAN: "true"
  artifacts:
    reports:
      dast: dast-report.json

# Example job demonstrating secrets and vault integration.
secret_job:
  stage: build
  script:
    - echo "Using secret: $MY_SECRET"
  secrets:  # Integrates with GitLab secrets management or Vault.
    MY_SECRET:
      vault: secret/path/to/secret  # Fetches secret from HashiCorp Vault.
      file: false  # Secret is not stored as a file.

# Example job for scheduled pipelines.
scheduled_job:
  stage: cleanup
  script:
    - echo "Running scheduled cleanup"
    - ./cleanup.sh
  rules:
    - when: delayed  # Delays job execution.
      start_in: 1 hour  # Starts job after 1 hour.
    - if: '$CI_PIPELINE_SOURCE == "schedule"'

# Example job demonstrating job timeout and custom tags.
timeout_job:
  stage: test
  script:
    - echo "This job has a custom timeout"
    - sleep 3600
  timeout: 30m  # Overrides default timeout for this job.
  tags:
    - high-memory

# Example job demonstrating services.
service_job:
  stage: test
  services:  # Defines additional containers to run alongside the job.
    - name: postgres:13
      alias: db
    - name: redis:latest
      alias: cache
  script:
    - echo "Testing with Postgres and Redis"
    - ./test-with-services.sh

# Example job for pages deployment.
pages:
  stage: deploy
  script:
    - echo "Deploying to GitLab Pages"
    - mv public/ public_new/
  artifacts:
    paths:
      - public_new/
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'

# Example job demonstrating release creation.
release_job:
  stage: deploy
  script:
    - echo "Creating release v1.0.$CI_PIPELINE_ID"
  release:  # Creates a release in GitLab.
    tag_name: v1.0.$CI_PIPELINE_ID
    description: 'Release v1.0.$CI_PIPELINE_ID'
    assets:  # Links to release assets.
      links:
        - name: 'Binary'
          url: 'https://example.com/binary.zip'

# Example job demonstrating workflow rules.
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: always
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: always
    - when: never  # Prevents pipeline from running otherwise.
```

### Explanations of Keywords and Verbs

The comments in the YAML file provide inline explanations, but here’s a summary of the key GitLab CI/CD keywords and verbs used, with their purposes:

- **default**: Sets default configurations (e.g., image, retry, timeout) for all jobs unless overridden.
- **stages**: Defines the order of pipeline stages (e.g., build, test, deploy).
- **variables**: Defines pipeline-wide or job-specific environment variables.
- **cache**: Specifies files/directories to cache between pipeline runs to speed up execution.
- **include**: Imports external YAML files to modularize pipeline configuration.
- **image**: Specifies the Docker image for a job.
- **script**: Defines the commands to execute in a job.
- **before_script**/**after_script**: Commands to run before/after the main script.
- **artifacts**: Defines files to store after job execution, with options for paths, expiration, and reports.
- **retry**: Configures automatic retries for failed jobs based on specific conditions.
- **timeout**: Sets a maximum duration for a job.
- **interruptible**: Allows a job to be canceled if a new pipeline starts.
- **only**/**except**: Controls when a job runs or is skipped based on refs, variables, or file changes.
- **rules**: Advanced control over job execution, replacing only/except, with conditions like `if`, `when`, and `changes`.
- **tags**: Restricts jobs to runners with specific tags.
- **when**: Specifies when a job runs (e.g., `on_success`, `always`, `manual`, `delayed`).
- **dependencies**: Specifies which jobs’ artifacts are needed for the current job.
- **needs**: Defines jobs that must complete before the current job, with optional artifact fetching.
- **environment**: Associates a job with a deployment environment, with options for `name`, `url`, and `on_stop`.
- **parallel**: Runs multiple instances of a job with different variables using a `matrix`.
- **services**: Defines additional containers (e.g., databases) to run alongside a job.
- **secrets**: Integrates with GitLab’s secrets management or external vaults for secure variable handling.
- **coverage**: Extracts code coverage information from job output.
- **allow_failure**: Allows a job to fail without failing the entire pipeline.
- **trigger**: Triggers a downstream pipeline in another project.
- **resource_group**: Ensures only one job runs at a time for a specific resource.
- **pages**: Deploys static content to GitLab Pages.
- **release**: Creates a release in GitLab with a tag and optional assets.
- **workflow**: Defines pipeline-level rules to control when the entire pipeline runs.

### Notes
- This `.gitlab-ci.yml` is a demonstration and includes a wide range of keywords for educational purposes. In a real-world scenario, you’d tailor it to your project’s needs, avoiding unnecessary complexity.
- Some keywords (e.g., `only` and `rules`) can be mutually exclusive; `rules` is preferred for newer configurations.
- The file assumes a project with Node.js, Docker, and typical CI/CD needs, but the structure is adaptable.
- For secrets and vault integration, you’d need proper GitLab or Vault configuration in your environment.
- The `include` paths and `trigger` project references are examples and should point to real resources in your setup.

If you need a more specific `.gitlab-ci.yml` tailored to a particular project or additional details on any keyword, let me know!

---

## **1. GitLab CI/CD Core Concepts**
### **Key Components**
| Component          | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| **`.gitlab-ci.yml`** | YAML file defining pipeline stages/jobs                                     |
| **Runners**        | Lightweight agents that execute jobs (can be Docker/Kubernetes-based)       |
| **Stages**         | Logical groups of jobs (e.g., `build`, `test`, `deploy`)                   |
| **Jobs**           | Individual tasks (e.g., `run-tests`, `build-image`)                        |
| **Variables**      | Environment variables for configuration                                    |

### **How It Works**
1. Code is pushed to a GitLab repo.
2. GitLab Runner picks up the `.gitlab-ci.yml` file.
3. Jobs run in isolated containers (Docker) or Kubernetes pods.

---

## **2. Docker Integration**
### **Method 1: Docker-in-Docker (DinD)**
Best for building Docker images within pipelines.

#### **Example `.gitlab-ci.yml`**
```yaml
variables:
  DOCKER_HOST: tcp://docker:2375
  DOCKER_DRIVER: overlay2

services:
  - docker:24.0-dind  # Runs Docker daemon

stages:
  - build
  - test

build-image:
  stage: build
  image: docker:24.0
  script:
    - docker build -t my-app .
    - docker run my-app pytest  # Run tests in container
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

#### **Key Points**
✅ **Isolated Docker environment**  
✅ **No host Docker socket dependency**  
⚠️ **Requires privileged mode** (enable in Runner config)  

---

### **Method 2: Docker Socket Binding**
Faster but less secure (shares host Docker socket).

```yaml
build-image:
  stage: build
  image: docker:24.0
  variables:
    DOCKER_HOST: unix:///var/run/docker.sock
  script:
    - docker build -t my-app .
```

#### **When to Use**
- **Local testing** (non-production)  
- **Performance-critical builds**  

---

## **3. Kubernetes Integration**
### **Method 1: Auto DevOps (Zero-Config)**
GitLab’s built-in Kubernetes deployment.

#### **Setup Steps**
1. **Connect Kubernetes Cluster**:
   - Navigate to **Operations → Kubernetes** in GitLab.
   - Add cluster details (API URL, CA cert, token).

2. **Enable Auto DevOps**:
   ```yaml
   # .gitlab-ci.yml
   include:
     - template: Auto-DevOps.gitlab-ci.yml
   ```

#### **Customizing Auto DevOps**
```yaml
variables:
  KUBE_NAMESPACE: my-app-prod
  HELM_RELEASE_NAME: my-app

stages:
  - build
  - deploy

deploy-to-k8s:
  extends: .auto-deploy
  environment:
    name: production
    url: https://my-app.example.com
```

---

### **Method 2: Manual `kubectl` Deployments**
Full control over Kubernetes deployments.

#### **Example Pipeline**
```yaml
deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl apply -f k8s/deployment.yaml
    - kubectl rollout status deployment/my-app
  only:
    - main
  environment:
    name: production
```

#### **Securing `kubeconfig`**
1. Store `kubeconfig` as a **CI/CD variable** (Settings → CI/CD → Variables).
2. Use it in jobs:
   ```yaml
   deploy:
     script:
       - kubectl get pods --kubeconfig $KUBE_CONFIG
   ```

---

## **4. Real-World Pipeline Example**
### **Full CI/CD with Docker & K8s**
```yaml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  image: python:3.9
  script:
    - pip install -r requirements.txt
    - pytest --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml

build:
  stage: build
  image: docker:24.0
  services:
    - docker:24.0-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/my-app my-app=$DOCKER_IMAGE
    - kubectl rollout status deployment/my-app
  environment:
    name: production
    url: https://my-app.example.com
  only:
    - main
```

---

## **5. Advanced Techniques**
### **1. Multi-Arch Docker Builds**
```yaml
build:
  script:
    - docker buildx create --use
    - docker buildx build --platform linux/amd64,linux/arm64 -t $DOCKER_IMAGE .
```

### **2. Canary Deployments**
```yaml
deploy-canary:
  script:
    - kubectl apply -f k8s/canary/
    - kubectl scale deployment/my-app-canary --replicas=2
```

### **3. Secret Management**
```yaml
variables:
  DB_PASSWORD: $SECRET_DB_PASSWORD  # Defined in CI/CD variables

deploy:
  script:
    - kubectl create secret generic db-creds --from-literal=password=$DB_PASSWORD
```

---

## **6. Troubleshooting Guide**
| Issue                          | Solution                                                                 |
|--------------------------------|-------------------------------------------------------------------------|
| **"docker: not found"**        | Use `image: docker:24.0` or install Docker in `before_script`          |
| **Kubernetes connection fails** | Verify `KUBE_CONFIG` variable and cluster permissions                 |
| **DinD errors**                | Ensure Runner is configured with `privileged = true`                  |
| **Slow builds**                | Enable layer caching: `docker build --cache-from`                     |

---

## **7. GitLab vs Jenkins: Key Differences**
| Feature                | GitLab CI/CD                          | Jenkins                              |
|------------------------|---------------------------------------|--------------------------------------|
| **Configuration**      | Declarative YAML                      | Groovy scripts                       |
| **Native K8s Support** | Built-in (Auto DevOps)                | Requires plugins                     |
| **Secret Management**  | CI/CD variables + Vault               | Credentials Plugin + HashiCorp Vault |
| **Runners**            | Shared or project-specific            | Master/agent architecture            |

---

## **8. Best Practices**
1. **Use `rules` instead of `only/except`** (more flexible control).
2. **Cache dependencies** (e.g., `pip`, `npm`).
3. **Limit `services`** (DinD adds overhead).
4. **Monitor deployments** with GitLab Environments.

---

## **9. Conclusion**
GitLab CI/CD provides a **seamless Docker/Kubernetes integration** with:
✅ **Native Auto DevOps** for zero-config deployments  
✅ **Flexible job definitions** with containerized runners  
✅ **Built-in artifact tracking** and environments  

For production workloads:  
- Use **DinD for secure Docker builds**  
- Leverage **Kubernetes for dynamic scaling**  
- Implement **canary deployments** for safe rollouts  

---
**Further Reading**:  
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)  
- [Auto DevOps Guide](https://docs.gitlab.com/ee/topics/autodevops/)  
- [Kubernetes Integration](https://docs.gitlab.com/ee/user/infrastructure/clusters/)


# **GitLab CI/CD Keywords (Verbs) Explained**

Below is a comprehensive list of all major keywords in GitLab CI/CD (`.gitlab-ci.yml`) with explanations and examples:

---

## **1. Pipeline Structure Keywords**
| Keyword       | Description                                                                 | Example |
|--------------|-----------------------------------------------------------------------------|---------|
| **`stages`** | Defines the order of pipeline stages (e.g., build, test, deploy). | ```yaml<br>stages:<br>  - build<br>  - test<br>``` |
| **`include`** | Includes external YAML files (templates or reusable configs). | ```yaml<br>include:<br>  - local: '/templates/.gitlab-ci.yml'<br>``` |
| **`extends`** | Inherits configuration from another job. | ```yaml<br>.base_job:<br>  script: echo "Hello"<br><br>job:<br>  extends: .base_job<br>``` |

---

## **2. Job Control Keywords**
| Keyword       | Description                                                                 | Example |
|--------------|-----------------------------------------------------------------------------|---------|
| **`script`** | Shell commands executed in the job. | ```yaml<br>script:<br>  - echo "Hello"<br>  - npm install<br>``` |
| **`before_script`** | Commands run before the main `script`. | ```yaml<br>before_script:<br>  - apt-get update<br>``` |
| **`after_script`** | Commands run after the job (even if it fails). | ```yaml<br>after_script:<br>  - echo "Job finished"<br>``` |
| **`rules`** | Conditional job execution (replaces `only/except`). | ```yaml<br>rules:<br>  - if: $CI_COMMIT_BRANCH == "main"<br>``` |
| **`when`** | When to run the job (`on_success`, `on_failure`, `always`, `manual`). | ```yaml<br>when: manual<br>``` |
| **`allow_failure`** | If `true`, pipeline continues even if the job fails. | ```yaml<br>allow_failure: true<br>``` |

---

## **3. Dependency & Artifact Keywords**
| Keyword       | Description                                                                 | Example |
|--------------|-----------------------------------------------------------------------------|---------|
| **`dependencies`** | Artifacts from which jobs to download. | ```yaml<br>dependencies:<br>  - build-job<br>``` |
| **`artifacts`** | Files to pass between jobs. | ```yaml<br>artifacts:<br>  paths:<br>    - dist/<br>``` |
| **`cache`** | Files to reuse across pipelines (e.g., `node_modules/`). | ```yaml<br>cache:<br>  key: $CI_COMMIT_REF_SLUG<br>  paths:<br>    - node_modules/<br>``` |

---

## **4. Environment & Deployment Keywords**
| Keyword       | Description                                                                 | Example |
|--------------|-----------------------------------------------------------------------------|---------|
| **`environment`** | Defines a deployment target (e.g., production). | ```yaml<br>environment:<br>  name: production<br>  url: https://example.com<br>``` |
| **`services`** | Sidecar containers (e.g., databases). | ```yaml<br>services:<br>  - postgres:14<br>``` |
| **`tags`** | Which GitLab Runners to use (by tags). | ```yaml<br>tags:<br>  - docker<br>``` |

---

## **5. Docker & Kubernetes Keywords**
| Keyword       | Description                                                                 | Example |
|--------------|-----------------------------------------------------------------------------|---------|
| **`image`** | Container image for the job. | ```yaml<br>image: node:16<br>``` |
| **`services`** | Additional containers (e.g., Redis, DB). | ```yaml<br>services:<br>  - redis:latest<br>``` |
| **`variables`** | Environment variables. | ```yaml<br>variables:<br>  DOCKER_HOST: tcp://docker:2375<br>``` |

---

## **6. Conditional Execution Keywords**
| Keyword       | Description                                                                 | Example |
|--------------|-----------------------------------------------------------------------------|---------|
| **`only`** / **`except`** | (Deprecated) Limits job execution. | ```yaml<br>only:<br>  - main<br>``` |
| **`rules`** | Modern replacement for `only/except`. | ```yaml<br>rules:<br>  - if: $CI_PIPELINE_SOURCE == "merge_request_event"<br>``` |

---

## **7. Parallelism & Resource Control**
| Keyword       | Description                                                                 | Example |
|--------------|-----------------------------------------------------------------------------|---------|
| **`parallel`** | Runs multiple instances of a job in parallel. | ```yaml<br>parallel: 5<br>``` |
| **`resource_group`** | Limits concurrent jobs (e.g., deployments). | ```yaml<br>resource_group: production<br>``` |

---

## **8. Security & Secrets**
| Keyword       | Description                                                                 | Example |
|--------------|-----------------------------------------------------------------------------|---------|
| **`secrets`** | Pulls secrets from Vault or CI variables. | ```yaml<br>secrets:<br>  DATABASE_PASSWORD:<br>    vault: production/db/password<br>``` |

---

## **9. Full Example**
```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

build:
  stage: build
  image: docker:24.0
  services:
    - docker:24.0-dind
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

test:
  stage: test
  image: python:3.9
  script:
    - pytest tests/
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

deploy:
  stage: deploy
  image: bitnami/kubectl
  script:
    - kubectl apply -f k8s/
  environment:
    name: production
  only:
    - main
```

---

## **10. Key Takeaways**
1. **`stages`** define the pipeline flow.  
2. **`rules`** replace `only/except` for conditional logic.  
3. **`artifacts`** and **`cache`** optimize performance.  
4. **`environment`** tracks deployments.  
5. **`services`** enable Docker/Kubernetes integrations.  

For more details, refer to the [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/yaml/).