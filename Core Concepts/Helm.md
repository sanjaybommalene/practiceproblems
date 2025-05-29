# Helm Comprehensive Notes: From Introduction to Advanced, with Kubernetes and Jenkins Integration

## Introduction to Helm

### What is Helm?
Helm is a package manager for Kubernetes, designed to simplify the deployment, management, and scaling of applications on Kubernetes clusters. It abstracts the complexity of managing Kubernetes resources by packaging them into reusable units called **Helm charts**. Helm is a Cloud Native Computing Foundation (CNCF) graduated project, widely adopted for its ability to streamline application deployment and ensure consistency across environments.[](https://helm.sh/)

### Why Use Helm?
- **Simplified Deployment**: Helm allows you to deploy complex applications with a single command, reducing the need for manual `kubectl` commands and YAML file management.
- **Reusability**: Helm charts are reusable templates, enabling consistent deployments across different environments (e.g., development, staging, production).
- **Versioning**: Helm supports versioning of charts, allowing easy upgrades and rollbacks to previous releases.
- **Dependency Management**: Helm charts can include dependencies, simplifying the deployment of applications with multiple components.
- **Community and Ecosystem**: Helm’s ArtifactHub provides access to a vast repository of pre-built charts for popular applications like Jenkins, MySQL, and Prometheus.[](https://dev.to/bravinsimiyu/how-to-setup-jenkins-on-kubernetes-cluster-with-helm-5an)

### Core Components of Helm
- **Helm CLI**: The command-line tool used to interact with Helm charts and Kubernetes clusters.
- **Charts**: Packages containing pre-configured Kubernetes resources (e.g., deployments, services, ingress) defined in YAML templates.
- **Release**: A specific instance of a chart deployed to a Kubernetes cluster with a given configuration.
- **Repository**: A storage location (e.g., ArtifactHub, ChartMuseum) for hosting and sharing Helm charts.
- **Values**: Customizable configuration files (`values.yaml`) that allow users to override default chart settings.

### Helm Installation
To use Helm, you need a Kubernetes cluster and the Helm CLI installed. Here’s how to install Helm on Linux:
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
Verify installation:
```bash
helm version
```
For other operating systems, refer to the official Helm installation guide.[](https://medium.com/%40cldop.com/deploying-jenkins-on-local-kubernetes-with-helm-chart-and-argocd-part-1-a-step-by-step-guide-4250149424d2)

## Helm Charts and Templates

### Structure of a Helm Chart
A Helm chart is a directory containing:
- **`Chart.yaml`**: Metadata about the chart (name, version, description).
- **`values.yaml`**: Default configuration values that can be overridden.
- **`templates/`**: Directory containing Kubernetes manifest templates (e.g., `deployment.yaml`, `service.yaml`).
- **`charts/`**: Directory for dependent charts.
- **Other files**: Optional files like `README.md`, `LICENSE`, or `templates/helpers.tpl` for reusable template logic.

Example chart structure:
```
mychart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── _helpers.tpl
├── charts/
```

### Creating a Helm Chart
Create a new chart using:
```bash
helm create mychart
```
This generates a boilerplate chart with default templates for a basic application. Customize the `values.yaml` file and templates to match your application’s needs.[](https://dev.to/oloruntobiolurombi/deploying-jenkins-on-kubernetes-using-helm-3g6p)

### Templating in Helm
Helm uses Go templating to render Kubernetes manifests dynamically. Key features include:
- **Variables**: Access values from `values.yaml` using `{{ .Values.key }}`.
- **Built-in Objects**: Access metadata like `{{ .Release.Name }}` (release name) or `{{ .Chart.Version }}` (chart version).
- **Control Structures**: Use `if`, `range`, and `with` for conditional logic and iteration.
- **Helper Templates**: Define reusable snippets in `_helpers.tpl`.

Example `deployment.yaml` template:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-app
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: {{ .Values.service.port }}
```

### Customizing Charts
Override default values by creating a custom `values.yaml` or passing values via the command line:
```bash
helm install myrelease ./mychart --set replicaCount=3
```

## Helm Repositories and Chart Management

### Adding a Repository
Helm charts are stored in repositories. Add the official Jenkins repository:
```bash
helm repo add jenkinsci https://charts.jenkins.io
helm repo update
```
Search for available charts:
```bash
helm search repo jenkinsci
```

### Managing Charts
- **Install a Chart**:
  ```bash
  helm install myjenkins jenkinsci/jenkins --namespace jenkins
  ```
- **Upgrade a Release**:
  ```bash
  helm upgrade myjenkins jenkinsci/jenkins --namespace jenkins -f custom-values.yaml
  ```
- **Rollback a Release**:
  ```bash
  helm rollback myjenkins 1 --namespace jenkins
  ```
- **Uninstall a Release**:
  ```bash
  helm uninstall myjenkins --namespace jenkins
  ```

### Hosting Charts
Use **ChartMuseum** to host private Helm charts:
```bash
helm repo add myrepo http://mychartmuseum:8080
```
Push charts to the repository:
```bash
helm push mychart myrepo
```

## Advanced Helm Features

### Helm Hooks
Hooks allow you to execute scripts or jobs at specific points in a release lifecycle (e.g., `pre-install`, `post-upgrade`). Example:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ .Release.Name }}-pre-install
  annotations:
    "helm.sh/hook": pre-install
spec:
  template:
    spec:
      containers:
      - name: setup
        image: busybox
        command: ["/bin/sh", "-c", "echo Running pre-install hook"]
      restartPolicy: Never
```

### Chart Dependencies
Manage dependencies in `Chart.yaml`:
```yaml
dependencies:
  - name: mysql
    version: "8.8.0"
    repository: "https://charts.bitnami.com/bitnami"
```
Update dependencies:
```bash
helm dependency update mychart
```

### Helmfile for Multi-Environment Deployments
Helmfile simplifies managing multiple charts across environments. Example `helmfile.yaml`:
```yaml
releases:
  - name: myjenkins
    chart: jenkinsci/jenkins
    namespace: jenkins
    values:
      - dev-values.yaml
```
Apply with:
```bash
helmfile apply
```

### Testing Charts
Use `helm test` to run integration tests:
```bash
helm test myjenkins --namespace jenkins
```

## Helm Integration with Kubernetes

### How Helm Interacts with Kubernetes
Helm CLI communicates with the Kubernetes API server to apply chart templates as Kubernetes resources. It uses the same `kubeconfig` context as `kubectl`. Key interactions:
- **Installation**: Helm renders templates and applies them via the Kubernetes API.
- **Upgrades and Rollbacks**: Helm tracks releases and updates resources or reverts to previous states.
- **RBAC**: Helm requires appropriate Role-Based Access Control (RBAC) permissions to manage resources. Example RBAC configuration:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: jenkins
  name: jenkins-role
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["create", "update", "delete"]
```

### Persistent Storage
For stateful applications like Jenkins, Helm charts can configure **PersistentVolumes** (PVs) to ensure data persistence across pod restarts. Example:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: jenkins-pv
  namespace: jenkins
spec:
  storageClassName: jenkins-pv
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 10Gi
  hostPath:
    path: /data/jenkins-volume/
```

### Jenkins Helm Chart on Kubernetes
The official Jenkins Helm chart (`jenkinsci/jenkins`) simplifies deploying Jenkins on Kubernetes. Steps to deploy:
1. Create a namespace:
   ```bash
   kubectl create namespace jenkins
   ```
2. Install the chart:
   ```bash
   helm install myjenkins jenkinsci/jenkins --namespace jenkins
   ```
3. Retrieve the admin password:
   ```bash
   printf $(kubectl get secret --namespace jenkins myjenkins -o jsonpath="{.data.jenkins-admin-password}" | base64 --decode); echo
   ```
4. Access Jenkins via a `NodePort` or `LoadBalancer` service:
   ```bash
   kubectl get svc -n jenkins
   ```

Customize the deployment using a `values.yaml` file:
```yaml
controller:
  replicaCount: 1
  serviceType: LoadBalancer
persistence:
  enabled: true
  storageClass: jenkins-pv
  size: 10Gi
```

## Helm Integration with Jenkins

### Why Integrate Helm with Jenkins?
Integrating Helm with Jenkins enables automated CI/CD pipelines for Kubernetes applications. Benefits include:
- **Automation**: Automate chart installation, upgrades, and rollbacks in CI/CD workflows.
- **Scalability**: Use Kubernetes pods as dynamic Jenkins agents for elastic build environments.
- **Consistency**: Ensure consistent deployments using Helm charts across environments.[](https://dzone.com/articles/easily-automate-your-cicd-pipeline-with-jenkins-he)

### Prerequisites
- A running Kubernetes cluster (e.g., Minikube, EKS, GKE).
- Helm CLI installed.
- Jenkins installed on Kubernetes using the Helm chart.
- Jenkins Kubernetes Plugin installed to provision dynamic agents.[](https://medium.com/%40cldop.com/deploying-jenkins-on-local-kubernetes-cluster-with-helm-chart-and-argocd-part-2-how-to-setup-d7ffb3170f43)

### Setting Up Jenkins on Kubernetes with Helm
1. **Install Jenkins**:
   ```bash
   helm repo add jenkinsci https://charts.jenkins.io
   helm repo update
   helm install myjenkins jenkinsci/jenkins --namespace jenkins -f values.yaml
   ```
   Example `values.yaml`:
   ```yaml
   controller:
     installPlugins:
       - kubernetes:1.31.2
       - workflow-aggregator:2.6
       - git:4.8.2
     serviceType: LoadBalancer
   persistence:
     enabled: true
     size: 10Gi
   ```

2. **Configure Kubernetes Plugin**:
   - Navigate to `Manage Jenkins > Manage Nodes and Clouds > Configure Clouds > Add a new cloud > Kubernetes`.
   - Set the Kubernetes URL (use default if Jenkins is in-cluster).
   - Test the connection to ensure Jenkins can communicate with the Kubernetes API.

3. **Define Pod Templates**:
   In the Kubernetes cloud configuration, define a pod template for agents:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     labels:
       app: jenkins-agent
   spec:
     containers:
     - name: jnlp
       image: jenkins/inbound-agent:latest
     - name: helm
       image: alpine/helm:latest
       command:
       - cat
       tty: true
   ```

### Creating a Jenkins Pipeline with Helm
Create a Jenkins pipeline to automate Helm chart deployments. Example `Jenkinsfile`:
```groovy
pipeline {
    agent {
        kubernetes {
            label 'helm-agent'
            yamlFile 'jenkins-pod.yaml'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-repo/your-app.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                container('helm') {
                    sh 'docker build -t your-repo/your-app:${BUILD_NUMBER} .'
                    sh 'docker push your-repo/your-app:${BUILD_NUMBER}'
                }
            }
        }
        stage('Deploy with Helm') {
            steps {
                container('helm') {
                    sh 'helm upgrade --install myapp ./helm/myapp --set image.tag=${BUILD_NUMBER} --namespace dev'
                }
            }
        }
    }
}
```
Corresponding `jenkins-pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: helm-agent
spec:
  containers:
  - name: helm
    image: alpine/helm:latest
    command:
    - cat
    tty: true
```

### Multi-Environment Deployments
To deploy to multiple environments (e.g., dev, staging, prod), use conditional logic in the pipeline:
```groovy
pipeline {
    agent {
        kubernetes {
            label 'helm-agent'
            yamlFile 'jenkins-pod.yaml'
        }
    }
    stages {
        stage('Deploy') {
            steps {
                container('helm') {
                    script {
                        if (env.GIT_BRANCH == 'origin/master') {
                            sh 'helm upgrade --install myapp ./helm/myapp -f values.dev.yaml --namespace dev'
                        } else if (env.GIT_BRANCH == 'origin/staging') {
                            sh 'helm upgrade --install myapp ./helm/myapp -f values.staging.yaml --namespace staging'
                        } else {
                            sh 'helm upgrade --install myapp ./helm/myapp -f values.prod.yaml --namespace prod'
                        }
                    }
                }
            }
        }
    }
}
```

### Advanced Integration: GitOps with ArgoCD
Combine Helm, Jenkins, and ArgoCD for GitOps workflows:
1. Deploy Jenkins using Helm as described above.
2. Install ArgoCD:
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```
3. Define an ArgoCD application to monitor a Helm chart repository:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: Application
   metadata:
     name: myapp
     namespace: argocd
   spec:
     project: default
     source:
       repoURL: https://github.com/your-repo/helm-charts.git
       path: myapp
       targetRevision: HEAD
     destination:
       server: https://kubernetes.default.svc
       namespace: dev
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
   ```
4. Configure Jenkins to push chart updates to the Git repository, triggering ArgoCD to apply changes.[](https://medium.com/%40cldop.com/deploying-jenkins-on-local-kubernetes-with-helm-chart-and-argocd-part-1-a-step-by-step-guide-4250149424d2)

## Best Practices
- **Version Control Charts**: Store Helm charts in a Git repository for versioning and collaboration.
- **Use Namespaces**: Deploy applications in separate namespaces for isolation.
- **Secure Helm**: Configure RBAC and service accounts to restrict Helm’s access to Kubernetes resources.
- **Backup Jenkins Data**: Use PersistentVolumes for Jenkins data and configure backups via the Helm chart.[](https://octopus.com/blog/jenkins-helm-install-guide)
- **Monitor and Scale**: Use tools like Prometheus and Grafana to monitor Jenkins and scale agents dynamically.
- **Test Charts**: Validate charts with `helm lint` and `helm template` before deployment.
- **Automate with CI/CD**: Integrate Helm with Jenkins pipelines for fully automated deployments.

## Troubleshooting
- **Connection Issues**: Ensure Jenkins has the correct `kubeconfig` and RBAC permissions.
- **Chart Errors**: Use `helm template` to debug rendered manifests.
- **Plugin Dependencies**: Verify Jenkins plugin versions in the Helm chart to avoid compatibility issues.[](https://medium.com/%40timhberry/deploy-jenkins-to-google-kubernetes-engine-with-helm-60e0a4d7de93)
- **Rollback Failures**: Check release history with `helm history myrelease` to identify rollback points.

## Conclusion
Helm is a powerful tool for managing Kubernetes applications, offering simplicity, reusability, and automation. When integrated with Jenkins, it enables robust CI/CD pipelines for deploying containerized applications to Kubernetes. By leveraging Helm charts, Jenkins pipelines, and tools like ArgoCD, you can achieve scalable, automated, and consistent deployments in modern cloud-native environments. For further learning, explore the official Helm documentation, Jenkins Kubernetes Plugin, and ArtifactHub for pre-built charts.[](https://helm.sh/)[](https://plugins.jenkins.io/kubernetes)[](https://github.com/jenkinsci/helm-charts)