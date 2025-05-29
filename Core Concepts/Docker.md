# **Introduction to Advanced Topics in Docker**

## **1. Overview of Docker**
Docker is an open-source platform that automates the deployment, scaling, and management of applications using containerization. Containers allow applications to run in isolated environments with their own dependencies, libraries, and configurations, ensuring consistency across different environments.

Docker uses OS-level virtualization to package and run applications in lightweight, isolated environments called containers. These containers share the host OS kernel but have their own filesystem and resources, enabling efficient and portable application deployment.

### **Key Components of Docker**
- **Docker Engine**: The core runtime that builds and runs containers.
- **Docker Daemon** - The background service running on the host that manages building, running and distributing Docker containers. The daemon is the process that runs in the operating system which clients talk to.
- **Docker Images**: Immutable templates used to create containers.
- **Docker Containers**: Runnable instances of Docker images.
- **Docker Hub/Registry**: Repository for storing and sharing Docker images.
- **Dockerfile**: A script containing instructions to build a Docker image.
- **Docker Compose**: A tool for defining and running multi-container applications.
- **Docker Swarm/Kubernetes**: Orchestration tools for managing containerized applications at scale.

---

## **2. Advanced Docker Concepts**
### **2.1 Multi-Stage Builds**
- Allows the use of multiple `FROM` statements in a single Dockerfile to create smaller and more efficient images.
- Useful for separating build-time dependencies from runtime dependencies.
  $ docker build -t yourusername/catnip .
  $ docker run -p 8888:5000 yourusername/catnip

**Example:**
```dockerfile
# ---- Build Stage ----
FROM python:3.9-slim as builder

# set a directory for the app
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies (cached unless requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.9-alpine

# set a directory for the app
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Set non-root user (security best practice)
RUN adduser -D appuser && chown -R appuser /app
USER appuser

# Activate virtual env from builder
ENV PATH="/opt/venv/bin:$PATH"

# Health check (for Docker/K8s monitoring)
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI app on port 8000
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **2.2 Docker Networking**
The bridge network is the network in which containers are run by default. So that means that when I ran the ES container, it was running in this bridge network.
- **Bridge Network**: Default network for containers (isolated communication).
- **Host Network**: Removes network isolation between container and host.
- **Overlay Network**: Enables communication across multiple Docker hosts (used in Swarm/Kubernetes).
- **Macvlan Network**: Assigns a MAC address to containers, making them appear as physical devices.

**Commands:**
```bash
docker network ls                  # List networks
docker network inspect bridge       # To see which network container is running, open for all
docker network create my-network   # Create a custom network, secure
docker run -d --name es --net foodtrucks-net # for two container to communicate, use 0.0.0.0:port, automatic service discovery
#!/bin/bash
# build the flask container
docker build -t yourusername/foodtrucks-web .
# create the network
docker network create foodtrucks-net
# start the ES continer
docker run -d --name es --net foodtrucks-net -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.3.2
# start the flask app container
docker run -d --net foodtrucks-net -p 5000:5000 --name foodtrucks-web yourusername/foodtrucks-web
docker run --network=my-network my-container
```

### **2.3 Docker Storage & Volumes**
- **Volumes**: Persistent storage managed by Docker (stored in `/var/lib/docker/volumes`).
- **Bind Mounts**: Directly map a host directory into a container.
- **tmpfs Mounts**: Store data in memory (non-persistent).

**Commands:**
```bash
docker volume create my-vol        # Create a volume
docker run -v my-vol:/data my-img # Mount a volume
docker run -v /host/path:/container/path my-img # Bind mount
```

### **2.4 Docker Security Best Practices**
- **Use Minimal Base Images** (e.g., Alpine Linux).
- **Run as Non-Root User** inside containers.
- **Scan Images for Vulnerabilities** using `docker scan`.
- **Limit Resource Usage** (CPU, Memory) with `--cpus`, `--memory`.
- **Enable Content Trust** (`DOCKER_CONTENT_TRUST=1`).

**Example:**
```bash
docker run --user 1000:1000 --memory=512m --cpus=1 my-img
```

### **2.5 Docker Compose for Multi-Container Apps**
- Define services, networks, and volumes in `docker-compose.yml`.
- Simplifies running interconnected containers (e.g., web app + database).

**Example:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: example
```

**Commands:**
```bash
docker-compose up -d    # Start services
docker-compose down    # Stop services
$ ecs-cli up --keypair ecs --capability-iam --size 1 --instance-type t2.medium
$ cd aws-ecs
$ ecs-cli compose up
ecs-cli ps
Name                                      State    Ports                     TaskDefinition
845e2368-170d-44a7-bf9f-84c7fcd9ae29/web  RUNNING  54.86.14.14:80->5000/tcp  ecscompose-foodtrucks:2
845e2368-170d-44a7-bf9f-84c7fcd9ae29/es   RUNNING                            ecscompose-foodtrucks:2
Go ahead and open http://54.86.14.14 in your browser and you should see
ecs-cli down --force
```

### **2.6 Docker Swarm & Kubernetes (Orchestration)**
- **Docker Swarm**: Native clustering for Docker (simpler than Kubernetes).
- **Kubernetes (K8s)**: Advanced orchestration for large-scale deployments.

**Swarm Commands:**
```bash
docker swarm init          # Initialize a Swarm
docker service create --name web --replicas 3 nginx # Scale services
```

### **2.7 Monitoring & Logging**
- **Docker Logs**: `docker logs <container>`
- **Prometheus + Grafana**: For metrics collection and visualization.
- **cAdvisor**: Container monitoring tool by Google.

**Commands:**
```bash
docker stats              # Live container resource usage
docker logs -f my-container # Stream logs
```

---

## **3. Docker in CI/CD Pipelines**
- Integrate Docker with **GitHub Actions, Jenkins, GitLab CI**.
- Build, test, and deploy containers automatically.
  
**Example (GitHub Actions):**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: docker build -t my-app .
      - run: docker run my-app pytest
```

# **Docker in CI/CD Pipelines: GitHub Actions, GitLab CI, and Jenkins Examples**
Below are **real-world examples** of integrating Docker into popular CI/CD platforms with best practices.
## **1. GitHub Actions with Docker**
**Use Case**: Build, test, and push a Docker image to GitHub Container Registry (GHCR).

### **`.github/workflows/docker.yml`**
```yaml
name: Docker Build & Push

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

      - name: Run tests
        run: |
          docker run ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            pytest /app/tests
```

### **Key Features**:
✅ **Automatic versioning** (`:latest` + Git SHA tags)  
✅ **Secure login** using `GITHUB_TOKEN`  
✅ **Conditional push** (only on `main` branch)  
✅ **In-container testing**  

---

## **2. GitLab CI/CD with Docker**
**Use Case**: Build a multi-stage Docker image, run tests, and deploy to GitLab Container Registry.

### **`.gitlab-ci.yml`**
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
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

test:
  stage: test
  image: $DOCKER_IMAGE
  script:
    - pytest /app/tests

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  only:
    - main
  script:
    - kubectl set image deployment/my-app app=$DOCKER_IMAGE --record
```

### **Key Features**:
✅ **Native Docker-in-Docker (dind)** support  
✅ **Auto-login to GitLab Registry**  
✅ **Kubernetes deployment** after testing  
✅ **Multi-stage pipeline**  

---

## **3. Jenkins with Docker**
**Use Case**: Build a Docker image, scan for vulnerabilities, and push to AWS ECR.

### **`Jenkinsfile` (Declarative Pipeline)**
```groovy
pipeline {
  agent {
    docker {
      image 'docker:24.0'
      args '-v /var/run/docker.sock:/var/run/docker.sock'
    }
  }
  environment {
    AWS_ACCOUNT = '123456789012'
    REGION = 'us-east-1'
    REPO = 'my-app'
  }
  stages {
    stage('Build') {
      steps {
        sh '''
          docker build -t $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/$REPO:$BUILD_NUMBER .
        '''
      }
    }
    stage('Scan') {
      steps {
        sh '''
          docker scan --accept-license $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/$REPO:$BUILD_NUMBER
        '''
      }
    }
    stage('Push') {
      steps {
        withAWS(credentials: 'aws-creds', region: "$REGION") {
          sh '''
            aws ecr get-login-password | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com
            docker push $AWS_ACCOUNT.dkr.ecr.$REGION.amazonaws.com/$REPO:$BUILD_NUMBER
          '''
        }
      }
    }
  }
}
```

### **Key Features**:
✅ **Docker socket binding** for DinD-free builds  
✅ **AWS ECR integration** with credentials  
✅ **Vulnerability scanning** (using `docker scan`)  
✅ **Build-number tagging**  

---

## **4. Key Best Practices Across All Platforms**
| Practice                  | GitHub Actions | GitLab CI | Jenkins |
|---------------------------|----------------|-----------|---------|
| **Use official Docker images** | ✅ | ✅ | ✅ |
| **Cache layers**           | ✅ (`cache-from`) | ✅ (`--cache-from`) | ✅ (`docker build --cache-from`) |
| **Scan for vulnerabilities** | ✅ (`docker scan`) | ✅ (Trivy) | ✅ (`docker scan`) |
| **Multi-arch builds**      | ✅ (`buildx`) | ✅ (`docker buildx`) | ✅ (`buildx`) |
| **Secrets management**     | ✅ (GitHub Secrets) | ✅ (CI Variables) | ✅ (Credentials Plugin) |

---

## **5. Pro Tips**
1. **Parallelize tests**: Run tests in multiple containers (e.g., `pytest-xdist`).
   ```yaml
   # GitHub Actions
   strategy:
     matrix:
       python-version: ["3.8", "3.9", "3.10"]
   ```

2. **Use BuildKit**: Faster builds with layer caching.
   ```dockerfile
   # Dockerfile (first line)
   # syntax=docker/dockerfile:1.4
   ```

3. **Clean up**: Avoid storage bloat.
   ```yaml
   # GitLab CI
   after_script:
     - docker system prune -f
   ```

4. **Multi-stage in CI**: Reduce final image size.
   ```dockerfile
   FROM python:3.9 as builder
   RUN pip install --user -r requirements.txt

   FROM python:3.9-slim
   COPY --from=builder /root/.local /root/.local
   ```

---

## **6. Choosing Your CI/CD Tool**
- **GitHub Actions**: Best for GitHub repos (native integration).  
- **GitLab CI**: Best for all-in-one DevOps (built-in registry).  
- **Jenkins**: Best for complex on-prem workflows (plugin ecosystem).  


## **4. Emerging Trends**
- **Serverless Containers** (AWS Fargate, Google Cloud Run).
- **Wasm (WebAssembly) Containers** for lightweight execution.
- **eBPF for Container Security** (enhanced observability).

---

## **5. Conclusion**
Advanced Docker topics enable efficient, scalable, and secure containerized applications. Key areas include multi-stage builds, networking, storage, security, orchestration (Swarm/K8s), and CI/CD integration. Mastering these concepts is essential for modern DevOps and cloud-native development.

---
**Further Learning:**
- [Docker Official Documentation](https://docs.docker.com)
- Kubernetes: [https://kubernetes.io/](https://kubernetes.io/)
- Docker Security Best Practices: [https://docs.docker.com/engine/security/](https://docs.docker.com/engine/security/)

# **Advanced Docker Compose & Dockerfile Example**

Below is a **real-world example** of a `docker-compose.yml` file and a **multi-stage** `Dockerfile` that demonstrates **networking, volumes, environment variables, health checks, resource limits, and security best practices**.

---

## **1. Advanced `Dockerfile` (Multi-Stage Build)**
This example builds a **Python FastAPI** application with:
- **Build stage** (installs dependencies)
- **Runtime stage** (minimal Alpine-based image)
- **Non-root user** for security
- **Optimized caching** for faster builds

```dockerfile
# ---- Build Stage ----
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies (cached unless requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.9-alpine

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Set non-root user (security best practice)
RUN adduser -D appuser && chown -R appuser /app
USER appuser

# Activate virtual env from builder
ENV PATH="/opt/venv/bin:$PATH"

# Health check (for Docker/K8s monitoring)
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI app on port 8000
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## **2. Advanced `docker-compose.yml`**
This file defines:
- **Multiple services** (FastAPI + PostgreSQL + Redis)
- **Custom networks** (isolated backend/frontend)
- **Persistent volumes** (for database)
- **Environment variables & secrets**
- **Resource limits & restart policies**
- **Health checks & dependency management**

```yaml
version: '3.8'

# Define secrets (external file or inline)
secrets:
  db_password:
    file: ./secrets/db_password.txt
  redis_password:
    external: true  # Uses `docker secret create`

# Define networks (isolated communication)
networks:
  backend:
    driver: bridge
    attachable: true
  frontend:
    driver: bridge

# Services
services:
  # FastAPI App
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fastapi_app
    networks:
      - backend
      - frontend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://appuser:${DB_PASSWORD}@db:5432/mydb
      - REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
  server:
    build:
      context: .
      target: build-base
    ports:
      - "1313:1313"
    entrypoint: ["hugo", "server", "--bind", "0.0.0.0"]
    develop:
      watch:
        - action: sync
          path: .
          target: /project

  # PostgreSQL Database
  db:
    image: postgres:14-alpine
    container_name: postgres_db
    networks:
      - backend
    volumes:
      - pg_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: appuser
      POSTGRES_DB: mydb
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 1G

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: redis_cache
    networks:
      - backend
    command: redis-server --requirepass $${REDIS_PASSWORD}
    environment:
      REDIS_PASSWORD_FILE: /run/secrets/redis_password
    secrets:
      - redis_password
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s

# Persistent volumes
volumes:
  pg_data:
    driver: local
  redis_data:
    driver: local
```

---

## **3. Key Concepts Demonstrated**
### **Dockerfile**
✅ **Multi-stage builds** → Smaller final image  
✅ **Non-root user** → Security best practice  
✅ **Efficient caching** → Faster builds  
✅ **Health checks** → Container monitoring  

### **Docker Compose**
✅ **Multiple services** (App + DB + Redis)  
✅ **Custom networks** (Isolated backend/frontend)  
✅ **Secrets management** (Secure credentials)  
✅ **Resource limits** (CPU/Memory constraints)  
✅ **Health checks & dependencies** (Auto-recovery)  
✅ **Persistent volumes** (Data survives container restarts)  

---

## **4. How to Run**
1. **Create secrets** (required for DB/Redis passwords):
   ```bash
   echo "mysecretdbpass" > secrets/db_password.txt
   docker secret create redis_password ./secrets/redis_password.txt
   ```

2. **Build and run**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Verify services**:
   ```bash
   docker-compose ps
   curl http://localhost:8000
   ```

---

## **5. Further Improvements**
- **Add Traefik/Nginx** for reverse proxying  
- **Integrate Prometheus** for monitoring  
- **Use Kubernetes** (`kompose convert` to generate K8s manifests)  

This setup is **production-ready** and covers most advanced Docker features. 🚀

# **Docker: Entrypoint vs CMD, ContainerPort vs HostPort Explained**

## **1. `ENTRYPOINT` vs `CMD` in Docker**
Both define what command runs when a container starts, but they interact differently:

| Feature          | `ENTRYPOINT`                          | `CMD`                              |
|------------------|---------------------------------------|------------------------------------|
| **Purpose**      | Defines the main executable           | Provides default arguments         |
| **Override**     | Hard to override (requires `--entrypoint`) | Easily overridden at runtime      |
| **Combination**  | `CMD` arguments are appended to `ENTRYPOINT` | Ignored if `ENTRYPOINT` exists   |
| **Best Use**     | For fixed commands (e.g., `python`)   | For default arguments (e.g., `--help`) |

### **Example:**
```dockerfile
# Dockerfile
FROM alpine
ENTRYPOINT ["echo"]
CMD ["Hello, Docker!"]
```
- **Default Run**:  
  ```bash
  docker run my-image
  # Output: Hello, Docker!
  ```
- **Override `CMD`**:  
  ```bash
  docker run my-image "Override!"
  # Output: Override!
  ```
- **Override `ENTRYPOINT`**:  
  ```bash
  docker run --entrypoint sh my-image
  # Starts a shell instead of running `echo`.
  ```

---

## **2. `ContainerPort` vs `HostPort`**
Both relate to network ports but serve different roles:

| Feature         | **ContainerPort**                     | **HostPort**                        |
|-----------------|---------------------------------------|-------------------------------------|
| **Definition**  | Port exposed inside the container     | Port mapped on the host machine     |
| **Visibility**  | Only accessible within Docker network | Accessible from outside the host    |
| **Syntax**      | Defined in `Dockerfile` (`EXPOSE`)    | Mapped in `docker run -p` or `docker-compose` |
| **Use Case**    | Documentation/internal networking     | External access to the container    |

### **Example:**
```dockerfile
# Dockerfile
FROM nginx
EXPOSE 80  # ContainerPort (informational)
```
- **Run with HostPort mapping**:  
  ```bash
  docker run -p 8080:80 nginx
  # HostPort:8080 → ContainerPort:80
  ```
- **In `docker-compose.yml`**:  
  ```yaml
  services:
    web:
      ports:
        - "8080:80"  # HostPort:ContainerPort
  ```

### **Key Notes:**
- If only `ContainerPort` is exposed (`EXPOSE 80`), the service is **not accessible from the host** unless mapped.
- Use `-p <HostPort>:<ContainerPort>` to make it publicly available.

---

## **3. Summary Table**
| Concept          | Key Difference                                                                 |
|------------------|--------------------------------------------------------------------------------|
| **ENTRYPOINT**   | Main command (hard to override).                                               |
| **CMD**          | Default arguments (easy to override).                                          |
| **ContainerPort**| Port inside the container (`EXPOSE` in Dockerfile).                            |
| **HostPort**     | Port on the host machine (`-p` flag in `docker run`).                          |

---

## **4. Practical Tips**
1. **Use `ENTRYPOINT` for executables** (e.g., `python`, `node`).  
2. **Use `CMD` for default args** (e.g., `app.py`, `--debug`).  
3. **Always map `HostPort`** if external access is needed.  
4. **`EXPOSE` is optional** but good for documentation.  

Example combining both:
```dockerfile
FROM python:3.9
ENTRYPOINT ["python"]  # Fixed executable
CMD ["app.py"]         # Default argument
EXPOSE 5000            # ContainerPort
```
Run with:
```bash
docker build -t myapp .
docker run -p 8000:5000 myapp          # Uses default CMD
docker run -p 8000:5000 myapp server.py # Overrides CMD
```