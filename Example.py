import os
import tarfile
import time
from datetime import datetime, timedelta
import boto3
import paramiko
from stat import S_ISREG

# Configurations
DIR_TO_SCAN = "/path/to/your/directory"  # Change this
S3_BUCKET = "your-s3-bucket"             # Change this
EC2_HOST = "ec2-xx-xx-xx-xx.compute-1.amazonaws.com"  # Change this
EC2_USER = "ec2-user"                    # Change this
SSH_KEY_PATH = "~/.ssh/your-key.pem"     # Change this


def find_old_files(directory, days=7):
    """Find files older than `days` days."""
    old_files = []
    cutoff_time = time.time() - (days * 86400)
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mtime < cutoff_time:
                old_files.append(file_path)
    
    return old_files

def create_tar(files, output_name="old_files.tar.gz"):
    """Create a tar.gz archive of files."""
    with tarfile.open(output_name, "w:gz") as tar:
        for file in files:
            tar.add(file, arcname=os.path.basename(file))
    return output_name

def upload_to_s3(file_path, bucket):
    """Upload file to S3."""
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, os.path.basename(file_path))
    print(f"Uploaded {file_path} to S3://{bucket}/{os.path.basename(file_path)}")

def send_to_ec2_via_ssh(local_file, ec2_host, ec2_user, ssh_key_path):
    """Transfer file to EC2 via SCP."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_host, username=ec2_user, key_filename=os.path.expanduser(ssh_key_path))
    
    # SCP Transfer
    scp = ssh.open_sftp()
    scp.put(local_file, f"/home/{ec2_user}/{os.path.basename(local_file)}")
    scp.close()
    ssh.close()
    print(f"Transferred {local_file} to EC2 at {ec2_host}:/home/{ec2_user}/")


if __name__ == "__main__":
    # Step 1: Find files older than 7 days
    old_files = find_old_files(DIR_TO_SCAN, days=7)
    if not old_files:
        print("No files older than 7 days found.")
        exit()
    
    # Step 2: Create a tar.gz archive
    tar_name = create_tar(old_files)
    print(f"Created archive: {tar_name}")
    
    # Step 3: Upload to S3
    upload_to_s3(tar_name, S3_BUCKET)
    
    # Step 4: Share with EC2 via SSH
    send_to_ec2_via_ssh(tar_name, EC2_HOST, EC2_USER, SSH_KEY_PATH)
    
    # Cleanup (optional)
    os.remove(tar_name)


import logging
import yaml
from jinja2 import Template
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_k8s_manifests(app_name, namespace, image, replicas, port):
    """Generate Kubernetes Deployment and Service YAML using Jinja2 template."""
    template = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ app_name }}
  namespace: {{ namespace }}
spec:
  replicas: {{ replicas }}
  selector:
    matchLabels:
      app: {{ app_name }}
  template:
    metadata:
      labels:
        app: {{ app_name }}
    spec:
      containers:
      - name: {{ app_name }}
        image: {{ image }}
        ports:
        - containerPort: {{ port }}
---
apiVersion: v1
kind: Service
metadata:
  name: {{ app_name }}-service
  namespace: {{ namespace }}
spec:
  selector:
    app: {{ app_name }}
  ports:
    - protocol: TCP
      port: {{ port }}
      targetPort: {{ port }}
  type: ClusterIP
"""
    try:
        rendered = Template(template).render(
            app_name=app_name,
            namespace=namespace,
            image=image,
            replicas=replicas,
            port=port
        )
        manifests = yaml.safe_load_all(rendered)
        with open(f"{app_name}_manifest.yaml", "w") as f:
            yaml.safe_dump_all(manifests, f)
        logger.info(f"Generated manifest: {app_name}_manifest.yaml")
        return list(manifests)
    except Exception as e:
        logger.error(f"Error generating manifests: {e}")
        raise

def apply_k8s_manifests(manifests, namespace):
    """Apply Kubernetes manifests to the cluster."""
    try:
        # Load kubeconfig or in-cluster config
        config.load_kube_config()  # Use config.load_incluster_config() for in-cluster
        v1 = client.CoreV1Api()
        apps_v1 = client.AppsV1Api()

        for manifest in manifests:
            kind = manifest.get('kind')
            metadata = manifest.get('metadata', {})
            name = metadata.get('name')

            if kind == 'Deployment':
                try:
                    apps_v1.create_namespaced_deployment(namespace=namespace, body=manifest)
                    logger.info(f"Created Deployment {name} in namespace {namespace}")
                except ApiException as e:
                    if e.status == 409:  # Conflict, update instead
                        apps_v1.replace_namespaced_deployment(name=name, namespace=namespace, body=manifest)
                        logger.info(f"Updated Deployment {name} in namespace {namespace}")
                    else:
                        raise
            elif kind == 'Service':
                try:
                    v1.create_namespaced_service(namespace=namespace, body=manifest)
                    logger.info(f"Created Service {name} in namespace {namespace}")
                except ApiException as e:
                    if e.status == 409:  # Conflict, update instead
                        v1.replace_namespaced_service(name=name, namespace=namespace, body=manifest)
                        logger.info(f"Updated Service {name} in namespace {namespace}")
                    else:
                        raise
    except Exception as e:
        logger.error(f"Error applying manifests: {e}")
        raise

def main(app_name, namespace, image, replicas, port):
    """Main function to generate and apply Kubernetes manifests."""
    try:
        manifests = generate_k8s_manifests(app_name, namespace, image, replicas, port)
        apply_k8s_manifests(manifests, namespace)
        logger.info(f"Successfully deployed {app_name} to namespace {namespace}")
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        raise

if __name__ == "__main__":
    app_name = "my-app"
    namespace = "default"
    image = "myregistry.com/my-app:latest"
    replicas = 3
    port = 8080
    main(app_name, namespace, image, replicas, port)






pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'myregistry.com'
        DOCKER_IMAGE = "${DOCKER_REGISTRY}/my-app:${env.BUILD_NUMBER}"
        K8S_NAMESPACE = 'default'
        K8S_APP_NAME = 'my-app'
        K8S_PORT = '8080'
        DOCKER_CREDENTIALS_ID = 'docker-registry-credentials'
        KUBE_CONFIG_CREDENTIALS_ID = 'kubeconfig'
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/user/my-repo.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin $DOCKER_REGISTRY
                        docker push $DOCKER_IMAGE
                    """
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: env.KUBE_CONFIG_CREDENTIALS_ID, variable: 'KUBECONFIG')]) {
                    sh """
                        export KUBECONFIG=$KUBECONFIG
                        python3 deploy_to_kubernetes.py
                    """
                }
            }
        }
    }
    post {
        always {
            sh 'docker logout $DOCKER_REGISTRY'
        }
        success {
            echo 'Deployment to Kubernetes completed successfully!'
        }
        failure {
            echo 'Deployment failed. Check logs for details.'
        }
    }
}