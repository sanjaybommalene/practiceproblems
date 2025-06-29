


# Python Scripting for DevOps – 50 Questions with Answers

import os
import shutil
import subprocess
import json
import yaml
import hashlib
import tarfile
from datetime import datetime, timedelta

# 1. List all files in a directory
files = os.listdir('.')
print(files)

# 2. Read log file line by line and search for keyword
with open('/var/log/syslog', 'r') as f:
    for line in f:
        if 'error' in line.lower():
            print(line.strip())

# 3. Archive files older than 7 days
now = datetime.now()
for file in os.listdir('.'):
    if os.path.isfile(file):
        mtime = datetime.fromtimestamp(os.path.getmtime(file))
        if (now - mtime).days > 7:
            shutil.move(file, 'archive/')

# 4. Get file size
print(os.path.getsize('file.txt'))

# 5. Rename all .log files with timestamp
for file in os.listdir('.'):
    if file.endswith('.log'):
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        shutil.move(file, f"{file}.{timestamp}")

# 6. Create directories recursively
os.makedirs('newdir/subdir', exist_ok=True)

# 7. Get and change current directory
print(os.getcwd())
os.chdir('/tmp')

# 8. Get environment variables
print(os.getenv('HOME'))

# 9. Monitor free disk space
total, used, free = shutil.disk_usage('/')
print(f"Free: {free // (2**30)} GB")

# 10. Copy and move files
shutil.copy('file.txt', '/tmp/file.txt')
shutil.move('file.txt', '/tmp/moved_file.txt')

# 11. Execute shell command
subprocess.run(['ls', '-l'])

# 12. Check command success
result = subprocess.run(['ls', '/nonexistent'], capture_output=True)
print(result.returncode == 0)

# 13. Pipe multiple commands
ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
grep = subprocess.Popen(['grep', 'python'], stdin=ps.stdout, stdout=subprocess.PIPE)
output = grep.communicate()[0]
print(output.decode())

# 14. Restart service if down
status = subprocess.run(['systemctl', 'is-active', 'nginx'], capture_output=True, text=True)
if status.stdout.strip() != 'active':
    subprocess.run(['systemctl', 'restart', 'nginx'])

# 15. Monitor process
processes = subprocess.check_output(['ps', 'aux'], text=True)
print('nginx' in processes)

# 16. Update system
subprocess.run(['sudo', 'apt', 'update'])
subprocess.run(['sudo', 'apt', 'upgrade', '-y'])

# 17. Tail log file
with open('/var/log/syslog', 'r') as f:
    f.seek(0, 2) 
    while True:
        line = f.readline()
        if not line:
            break
        print(line.strip())

# 18. Parse df -h
output = subprocess.check_output(['df', '-h'], text=True)
print(output)

# 19. Run command with sudo
subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])

# 20. subprocess.run vs call: run is modern and returns CompletedProcess, call returns exit code.

# 21. Monitor log for error
with open('/var/log/syslog', 'r') as f:
    for line in f:
        if 'ERROR' in line:
            print(line)

# 22. Log rotation
if os.path.getsize('app.log') > 100*1024*1024:
    shutil.copy('app.log', f"app.log.{datetime.now().strftime('%Y%m%d%H%M')}")
    open('app.log', 'w').close()

# 23. Clear log file
open('/var/log/app.log', 'w').close()

# 24. Email last 50 lines (simulated)
with open('/var/log/syslog', 'r') as f:
    lines = f.readlines()
    print(''.join(lines[-50:]))

# 25. Detect log file not updated
mtime = datetime.fromtimestamp(os.path.getmtime('/var/log/syslog'))
if (datetime.now() - mtime).seconds > 300:
    print("Log not updated in last 5 minutes")

# 26. Restart failed service
if check_service('nginx') != 'active':
    subprocess.run(['systemctl', 'restart', 'nginx'])

# 27. Install package
subprocess.run(['sudo', 'apt', 'install', '-y', 'curl'])

# 28. Ping servers
servers = ['google.com', 'yahoo.com']
for s in servers:
    r = subprocess.run(['ping', '-c', '1', s])
    print(f"{s} status: {r.returncode}")

# 29. Patching script
subprocess.run(['sudo', 'apt', 'update'])
subprocess.run(['sudo', 'apt', 'upgrade', '-y'])
subprocess.run(['sudo', 'reboot'])

# 30. Cron-safe backup
if datetime.now().hour == 2:
    shutil.copytree('/data', f"/backup/data_{datetime.now().strftime('%Y%m%d')}" )

# 31. Check CPU, memory, disk
subprocess.run(['top', '-b', '-n', '1'])

# 32. CPU cores
os.cpu_count()

# 33. Memory stats
with open('/proc/meminfo') as f:
    print(f.readline())

# 34. Count Docker containers
output = subprocess.check_output(['docker', 'ps', '-q'], text=True)
print(len(output.strip().splitlines()))

# 35. Service uptime
output = subprocess.check_output(['systemctl', 'show', 'nginx', '--property=ActiveEnterTimestamp'], text=True)
print(output)

# 36. Read/write JSON
with open('conf.json') as f:
    conf = json.load(f)
conf['version'] = '2.0'
with open('conf.json', 'w') as f:
    json.dump(conf, f, indent=4)

# 37. Read/update YAML
with open('conf.yaml') as f:
    conf = yaml.safe_load(f)
conf['enabled'] = True
with open('conf.yaml', 'w') as f:
    yaml.dump(conf, f)

# 38. Validate JSON
try:
    json.load(open('conf.json'))
    print("Valid JSON")
except json.JSONDecodeError:
    print("Invalid JSON")

# 39. Update YAML from CLI
import sys
with open('file.yaml') as f:
    y = yaml.safe_load(f)
y['key'] = sys.argv[1]
with open('file.yaml', 'w') as f:
    yaml.dump(y, f)

# 40. Update nested config
conf['database']['host'] = '127.0.0.1'

# 41. Create tarball
with tarfile.open('backup.tar.gz', 'w:gz') as tar:
    tar.add('dir_to_backup')

# 42. Check backup existence
for i in range(7):
    d = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
    print(f"backup_{d}.tar.gz exists: {os.path.exists(f'backup_{d}.tar.gz')}")

# 43. Compare config files
with open('a.json') as fa, open('b.json') as fb:
    print(json.load(fa) == json.load(fb))

# 44. Rsync (via subprocess)
subprocess.run(['rsync', '-av', '/src/', 'user@host:/dest/'])

# 45. Check file permissions
for f in os.listdir('.'):
    mode = oct(os.stat(f).st_mode)[-3:]
    if mode > '755':
        print(f"{f} is too permissive: {mode}")

# 46. SHA256 checksum
with open('file.txt', 'rb') as f:
    print(hashlib.sha256(f.read()).hexdigest())

# 47. Secure password input
import getpass
password = getpass.getpass("Enter password: ")

# 48. Check SSL expiry (requires openssl and timeout)
subprocess.run(['echo', '|', 'openssl', 's_client', '-connect', 'google.com:443'])

# 49. Get pod names using kubectl
output = subprocess.check_output(['kubectl', 'get', 'pods', '-n', 'default', '-o', 'name'], text=True)
print(output)

# 50. Argparse for CLI tool
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--service')
args = parser.parse_args()
print(args.service)


Below is a curated list of **50 commonly asked Python scripting questions** tailored for a DevOps role, focusing on the key concepts discussed earlier: **automation**, **patching**, **OS/file management**, and other **DevOps-related scripting tasks**. Each question is accompanied by a brief explanation of why it’s relevant and a concise example answer or code snippet to demonstrate how to approach it. These questions align with the technical demands of a DevOps role and are designed to help you prepare for your interview in three days. I’ve also ensured this complements your previous inquiries about Kubernetes and scripting.

---

## File and OS Management (15 Questions)

1. **How do you read a file line by line in Python?**
   - **Why**: DevOps scripts often parse logs or configuration files.
   - **Answer**:
     ```python
     with open("log.txt", "r") as file:
         for line in file:
             print(line.strip())
     ```

2. **Write a script to find all files with a specific extension in a directory.**
   - **Why**: Useful for log management or cleanup tasks.
   - **Answer**:
     ```python
     import os
     def find_files(directory, extension):
         return [f for f in os.listdir(directory) if f.endswith(extension)]
     print(find_files("/var/log", ".log"))
     ```

3. **How do you create a directory if it doesn’t exist?**
   - **Why**: Common in scripts that organize logs or backups.
   - **Answer**:
     ```python
     import os
     os.makedirs("/path/to/dir", exist_ok=True)
     ```

4. **Write a script to delete files older than N days.**
   - **Why**: Essential for log rotation and cleanup.
   - **Answer**:
     ```python
     import os
     import time
     def delete_old_files(directory, days=7):
         threshold = time.time() - days * 86400
         for file in os.listdir(directory):
             file_path = os.path.join(directory, file)
             if os.path.isfile(file_path) and os.path.getmtime(file_path) < threshold:
                 os.remove(file_path)
                 print(f"Deleted: {file_path}")
     delete_old_files("/var/log")
     ```

5. **How do you execute a system command in Python?**
   - **Why**: DevOps scripts often run commands like `kubectl` or `df`.
   - **Answer**:
     ```python
     import subprocess
     result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
     print(result.stdout)
     ```

6. **How do you check if a file exists?**
   - **Why**: Prevents errors in file operations.
   - **Answer**:
     ```python
     import os
     if os.path.exists("config.yaml"):
         print("File exists")
     ```

7. **Write a script to copy a directory recursively.**
   - **Why**: Used for backups or deployments.
   - **Answer**:
     ```python
     import shutil
     shutil.copytree("/source/dir", "/backup/dir", dirs_exist_ok=True)
     ```

8. **How do you get the size of a file?**
   - **Why**: Useful for monitoring disk usage.
   - **Answer**:
     ```python
     import os
     size = os.path.getsize("log.txt") / (1024 * 1024)  # Size in MB
     print(f"File size: {size:.2f} MB")
     ```

9. **How do you parse a CSV file?**
   - **Why**: Common for processing metrics or configuration data.
   - **Answer**:
     ```python
     import csv
     with open("data.csv", "r") as file:
         reader = csv.DictReader(file)
         for row in reader:
             print(row)
     ```

10. **Write a script to count error lines in a log file.**
    - **Why**: Helps in monitoring application health.
    - **Answer**:
      ```python
      def count_errors(log_file):
          error_count = 0
          with open(log_file, "r") as f:
              for line in f:
                  if "ERROR" in line.upper():
                      error_count += 1
          return error_count
      print(count_errors("app.log"))
      ```

11. **How do you change file permissions?**
    - **Why**: Required for securing files in production.
    - **Answer**:
      ```python
      import os
      os.chmod("script.sh", 0o755)  # Owner: rwx, Others: rx
      ```

12. **How do you handle large files without loading them into memory?**
    - **Why**: Efficient log processing is critical in DevOps.
    - **Answer**:
      ```python
      with open("large.log", "r") as file:
          for line in file:
              process_line(line)  # Process line by line
      ```

13. **Write a script to monitor disk usage.**
    - **Why**: Critical for system health checks.
    - **Answer**:
      ```python
      import psutil
      disk = psutil.disk_usage("/")
      print(f"Free disk: {disk.free / (1024**3):.2f} GB")
      ```

14. **How do you zip a directory?**
    - **Why**: Used for backups or data transfer.
    - **Answer**:
      ```python
      import shutil
      shutil.make_archive("backup", "zip", "/var/app/data")
      ```

15. **How do you run a command and handle errors?**
    - **Why**: Ensures robust script execution.
    - **Answer**:
      ```python
      import subprocess
      try:
          result = subprocess.run(["ping", "-c", "1", "google.com"], capture_output=True, text=True, check=True)
          print(result.stdout)
      except subprocess.CalledProcessError as e:
          print(f"Command failed: {e.stderr}")
      ```

---

## Automation (15 Questions)

16. **How do you make an HTTP request in Python?**
    - **Why**: DevOps scripts often interact with APIs (e.g., Kubernetes, AWS).
    - **Answer**:
      ```python
      import requests
      response = requests.get("https://api.example.com/health")
      print(response.json())
      ```

17. **Write a script to check the health of an API endpoint.**
    - **Why**: Common for monitoring services.
    - **Answer**:
      ```python
      import requests
      def check_api(url):
          try:
              response = requests.get(url, timeout=5)
              return response.status_code == 200
          except requests.RequestException:
              return False
      print(check_api("https://api.example.com/health"))
      ```

18. **How do you parse JSON data from an API response?**
    - **Why**: APIs often return JSON, used in automation.
    - **Answer**:
      ```python
      import requests
      response = requests.get("https://api.example.com/data")
      data = response.json()
      print(data["key"])
      ```

19. **Write a script to automate EC2 instance start/stop.**
    - **Why**: Common in cloud automation.
    - **Answer**:
      ```python
      import boto3
      def start_ec2(instance_id, region="us-east-1"):
          ec2 = boto3.client("ec2", region_name=region)
          ec2.start_instances(InstanceIds=[instance_id])
          print(f"Started instance: {instance_id}")
      start_ec2("i-1234567890abcdef0")
      ```

20. **How do you schedule a task in Python?**
    - **Why**: Used for recurring tasks like backups.
    - **Answer**:
      ```python
      import schedule
      import time
      def job():
          print("Running task...")
      schedule.every(10).seconds.do(job)
      while True:
          schedule.run_pending()
          time.sleep(1)
      ```

21. **Write a script to update a YAML configuration file.**
    - **Why**: Common for managing app configurations.
    - **Answer**:
      ```python
      import yaml
      def update_yaml(file_path, key, value):
          with open(file_path, "r") as f:
              config = yaml.safe_load(f)
          config[key] = value
          with open(file_path, "w") as f:
              yaml.dump(config, f)
      update_yaml("config.yaml", "replicas", 3)
      ```

22. **How do you interact with a Kubernetes cluster using Python?**
    - **Why**: Kubernetes automation is critical for DevOps.
    - **Answer**:
      ```python
      from kubernetes import client, config
      config.load_kube_config()
      v1 = client.CoreV1Api()
      pods = v1.list_pod_for_all_namespaces()
      for pod in pods.items:
          print(pod.metadata.name)
      ```

23. **Write a script to restart failed Kubernetes pods.**
    - **Why**: Automates recovery in Kubernetes environments.
    - **Answer**:
      ```python
      from kubernetes import client, config
      def restart_failed_pods(namespace="default"):
          config.load_kube_config()
          v1 = client.CoreV1Api()
          pods = v1.list_namespaced_pod(namespace)
          for pod in pods.items:
              if pod.status.phase == "Failed":
                  v1.delete_namespaced_pod(pod.metadata.name, namespace)
                  print(f"Restarted: {pod.metadata.name}")
      restart_failed_pods()
      ```

24. **How do you handle environment variables in Python?**
    - **Why**: Securely manage secrets and configurations.
    - **Answer**:
      ```python
      import os
      db_password = os.getenv("DB_PASSWORD", "default_password")
      print(db_password)
      ```

25. **Write a script to automate Docker container cleanup.**
    - **Why**: Manages containerized environments.
    - **Answer**:
      ```python
      import docker
      def cleanup_containers():
          client = docker.from_env()
          for container in client.containers.list(all=True, filters={"status": "exited"}):
              container.remove()
              print(f"Removed: {container.id}")
      cleanup_containers()
      ```

26. **How do you send an email alert in Python?**
    - **Why**: Used for monitoring and alerting.
    - **Answer**:
      ```python
      import smtplib
      from email.mime.text import MIMEText
      def send_alert(to, message):
          msg = MIMEText(message)
          msg["Subject"] = "Alert"
          msg["From"] = "alert@devops.com"
          msg["To"] = to
          with smtplib.SMTP("smtp.gmail.com", 587) as server:
              server.starttls()
              server.login("user", "password")
              server.send_message(msg)
      send_alert("admin@devops.com", "Server down!")
      ```

27. **How do you use SSH in Python for remote execution?**
    - **Why**: Automates tasks on remote servers.
    - **Answer**:
      ```python
      import paramiko
      def run_remote_command(host, username, command):
          client = paramiko.SSHClient()
          client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
          client.connect(host, username=username, key_filename="~/.ssh/id_rsa")
          stdin, stdout, stderr = client.exec_command(command)
          print(stdout.read().decode())
          client.close()
      run_remote_command("server.example.com", "user", "uptime")
      ```

28. **Write a script to monitor memory usage.**
    - **Why**: Critical for system health checks.
    - **Answer**:
      ```python
      import psutil
      memory = psutil.virtual_memory()
      print(f"Used memory: {memory.used / (1024**3):.2f} GB")
      ```

29. **How do you parse command-line arguments?**
    - **Why**: Scripts need flexible inputs.
    - **Answer**:
      ```python
      import argparse
      parser = argparse.ArgumentParser()
      parser.add_argument("--path", required=True)
      args = parser.parse_args()
      print(args.path)
      ```

30. **Write a script to trigger a Jenkins job.**
    - **Why**: Automates CI/CD pipelines.
    - **Answer**:
      ```python
      from jenkinsapi.jenkins import Jenkins
      def trigger_job(server_url, username, password, job_name):
          jenkins = Jenkins(server_url, username=username, password=password)
          job = jenkins[job_name]
          job.invoke()
          print(f"Triggered job: {job_name}")
      trigger_job("http://jenkins:8080", "user", "pass", "build-job")
      ```

---

## Patching and System Updates (10 Questions)

31. **How do you automate system patching with `apt`?**
    - **Why**: Ensures systems are secure.
    - **Answer**:
      ```python
      import subprocess
      def apply_patches():
          subprocess.run(["apt-get", "update"], check=True)
          subprocess.run(["apt-get", "upgrade", "-y"], check=True)
          print("Patches applied")
      ```

32. **Write a script to check for available updates.**
    - **Why**: Helps plan maintenance windows.
    - **Answer**:
      ```python
      import subprocess
      def check_updates():
          result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True)
          print(result.stdout)
      check_updates()
      ```

33. **How do you handle patch failures?**
    - **Why**: Ensures robust patching.
    - **Answer**:
      ```python
      import subprocess
      try:
          subprocess.run(["apt-get", "upgrade", "-y"], check=True)
      except subprocess.CalledProcessError as e:
          print(f"Patch failed: {e.stderr}")
      ```

34. **Write a script to back up critical files before patching.**
    - **Why**: Prevents data loss during updates.
    - **Answer**:
      ```python
      import shutil
      shutil.copy("/etc/config.conf", "/etc/config.conf.bak")
      ```

35. **How do you verify a patch was applied?**
    - **Why**: Ensures system integrity.
    - **Answer**:
      ```python
      import subprocess
      def verify_patch(package):
          result = subprocess.run(["dpkg", "-l", package], capture_output=True, text=True)
          print(result.stdout)
      verify_patch("nginx")
      ```

36. **Write a script to rollback a failed patch.**
    - **Why**: Critical for recovery.
    - **Answer**:
      ```python
      import shutil
      if os.path.exists("config.conf.bak"):
          shutil.move("config.conf.bak", "config.conf")
          print("Restored backup")
      ```

37. **How do you schedule patching with Python?**
    - **Why**: Automates maintenance.
    - **Answer**:
      ```python
      import schedule
      def patch_system():
          subprocess.run(["apt-get", "upgrade", "-y"])
      schedule.every().sunday.at("02:00").do(patch_system)
      ```

38. **How do you log patching activities?**
    - **Why**: Tracks maintenance history.
    - **Answer**:
      ```python
      import logging
      logging.basicConfig(filename="patch.log", level=logging.INFO)
      logging.info("Patching started")
      ```

39. **Write a script to check package versions.**
    - **Why**: Verifies installed software.
    - **Answer**:
      ```python
      import subprocess
      def check_version(package):
          result = subprocess.run(["dpkg", "-l", package], capture_output=True, text=True)
          print(result.stdout)
      check_version("python3")
      ```

40. **How do you handle dependencies during patching?**
    - **Why**: Prevents broken packages.
    - **Answer**:
      ```python
      import subprocess
      subprocess.run(["apt-get", "install", "-f"], check=True)  # Fix dependencies
      ```

---

## General DevOps Scripting (10 Questions)

41. **How do you handle secrets in Python scripts?**
    - **Why**: Security is critical in DevOps.
    - **Answer**:
      ```python
      from dotenv import load_dotenv
      import os
      load_dotenv()
      api_key = os.getenv("API_KEY")
      ```

42. **Write a script to monitor a process.**
    - **Why**: Ensures critical services are running.
    - **Answer**:
      ```python
      import psutil
      def is_process_running(name):
          for proc in psutil.process_iter(["name"]):
              if proc.info["name"] == name:
                  return True
          return False
      print(is_process_running("nginx"))
      ```

43. **How do you parse a log file for specific patterns?**
    - **Why**: Used in monitoring and debugging.
    - **Answer**:
      ```python
      import re
      def find_pattern(log_file, pattern):
          with open(log_file, "r") as f:
              for line in f:
                  if re.search(pattern, line):
                      print(line.strip())
      find_pattern("app.log", r"ERROR.*database")
      ```

44. **Write a script to rotate logs.**
    - **Why**: Prevents disk space issues.
    - **Answer**:
      ```python
      import shutil
      import os
      def rotate_log(log_file):
          if os.path.exists(log_file):
              shutil.move(log_file, f"{log_file}.1")
              open(log_file, "w").close()  # Create new empty log
      rotate_log("app.log")
      ```

45. **How do you handle timeouts in API calls?**
    - **Why**: Ensures robust automation.
    - **Answer**:
      ```python
      import requests
      try:
          response = requests.get("https://api.example.com", timeout=5)
      except requests.Timeout:
          print("Request timed out")
      ```

46. **Write a script to check network connectivity.**
    - **Why**: Common for troubleshooting.
    - **Answer**:
      ```python
      import socket
      def check_connectivity(host="8.8.8.8", port=53):
          try:
              socket.create_connection((host, port), timeout=5)
              return True
          except socket.error:
              return False
      print(check_connectivity())
      ```

47. **How do you generate a random password for automation?**
    - **Why**: Used in user management or testing.
    - **Answer**:
      ```python
      import secrets
      import stringeibcccujevecbbbikrgebtnjhulkgjvuvtjnbfcgrufe
      
      def generate_password(length=12):
          chars = string.ascii_letters + string.digits + string.punctuation
          return "".join(secrets.choice(chars) for _ in range(length))
      print(generate_password())
      ```

48. **Write a script to validate a configuration file.**
    - **Why**: Ensures correct configurations.
    - **Answer**:
      ```python
      import yaml
      def validate_yaml(file_path):
          try:
              with open(file_path, "r") as f:
                  yaml.safe_load(f)
              return True
          except yaml.YAMLError:
              return False
      print(validate_yaml("config.yaml"))
      ```

49. **How do you profile a Python script for performance?**
    - **Why**: Optimizes scripts for production.
    - **Answer**:
      ```python
      import cProfile
      cProfile.run("my_function()")
      ```

50. **Write a script to sync files to an S3 bucket.**
    - **Why**: Common for backups or deployments.
    - **Answer**:
      ```python
      import boto3
      def sync_to_s3(local_path, bucket, s3_path):
          s3 = boto3.client("s3")
          s3.upload_file(local_path, bucket, s3_path)
          print(f"Uploaded {local_path} to s3://{bucket}/{s3_path}")
      sync_to_s3("app.log", "my-bucket", "logs/app.log")
      ```

---

## Preparation Tips for Interview
- **Practice Coding Live**: Use platforms like HackerRank or LeetCode to simulate coding under pressure.
- **Focus on Error Handling**: Always include `try-except` blocks to show robustness.
- **Explain Your Code**: Be ready to walk through your logic and justify design choices.
- **Test Scripts**: Run your scripts locally to ensure they work as expected.
- **Review Kubernetes Context**: Since you mentioned Kubernetes previously, be prepared for questions combining Python with `kubectl` or the Kubernetes API.

---

## Study Plan for 3 Days
- **Day 1**: Focus on file/OS management (Q1–15). Write 5–7 scripts for log parsing, file operations, and system commands.
- **Day 2**: Cover automation (Q16–30). Practice API calls, Kubernetes interactions, and cloud automation (e.g., `boto3`).
- **Day 3**: Study patching and general DevOps tasks (Q31–50). Practice patching scripts, monitoring, and S3 operations. Review all scripts and simulate interview questions.



Below are **solutions for all 50 Python scripting questions** for DevOps roles, organized by category. Each solution includes **runnable code** and explanations.

---

## **1. File & OS Operations**  
### **Q1. List all files recursively**  
```python
import os

def list_files_recursive(path):
    for root, _, files in os.walk(path):
        for file in files:
            print(os.path.join(root, file))

list_files_recursive("/tmp")
```

### **Q2. Delete files older than X days**  
```python
import os
import time

def delete_old_files(path, days=7):
    cutoff = time.time() - (days * 86400)
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.getmtime(filepath) < cutoff:
                os.remove(filepath)
```

### **Q3. Read/write YAML/JSON**  
```python
import yaml
import json

# JSON
# YAML
with open("config.yml") as f:
    yaml_data = yaml.safe_load(f)

with open("data.json", "w") as f:
    json.dump({"key": "value"}, f)
```

### **Q4. Replace string in multiple files**  
```python
import os
import re

def replace_in_files(directory, old, new):
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, "r+") as f:
                content = f.read()
                f.seek(0)
                f.write(content.replace(old, new))
                f.truncate()
```

### **Q5. Check if file exists**  
```python
import os

if os.path.exists("/path/to/file"):
    print("File exists!")
```

### **Q6. Monitor log file for new entries**  
```python
import time

def tail_log(logfile):
    with open(logfile, "r") as f:
        f.seek(0, 2)  # Go to end 
        while True:
            line = f.readline()
            if line:
                print(line.strip())
            time.sleep(0.1)
```

### **Q7. Compress/uncompress files**  
```python
import gzip
import shutil

# Compress
with open("file.txt", "rb") as f_in:
    with gzip.open("file.txt.gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

# Uncompress
with gzip.open("file.txt.gz", "rb") as f_in:
    with open("file.txt", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
```

### **Q8. Compare two directories**  
```python
import filecmp

diff = filecmp.dircmp("dir1", "dir2")
diff.report()  # Prints differences
```

### **Q9. Change file permissions**  
```python
import os
import stat

os.chmod("script.sh", stat.S_IRWXU)  # 700 permissions
```

### **Q10. Search for file by name**  
```python
import os

def find_file(start_dir, filename):
    for root, _, files in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None
```

---

## **2. Automation & Subprocess**  
### **Q11. Run shell commands**  
```python
import subprocess

# Safe way (recommended)
subprocess.run(["ls", "-l"], check=True)

# Unsafe (shell injection risk)
subprocess.run("ls -l", shell=True)
```

### **Q12. Docker container cleanup**  
```python
import subprocess

def clean_docker():
    subprocess.run(["docker", "system", "prune", "-f"], check=True)
```

### **Q13. Schedule Python script**  
```python
# Linux cron: Add to crontab -e
# * * * * * /usr/bin/python3 /path/to/script.py
```

### **Q14. Check disk space**  
```python
import shutil

total, used, free = shutil.disk_usage("/")
print(f"Used: {used / (2**30):.2f} GB")
```

### **Q15. Parallelize tasks**  
```python
from multiprocessing import Pool

def process_item(item):
    return item * 2

with Pool(4) as p:
    results = p.map(process_item, [1, 2, 3])
```

### **Q16. Restart failed service**  
```python
import subprocess

def restart_service(service):
    subprocess.run(["systemctl", "restart", service], check=True)
```

### **Q17. SSH with Python (Paramiko)**  
```python
import paramiko

ssh = paramiko.SSHClient()
ssh.connect("host", username="user", password="pass")
stdin, stdout, stderr = ssh.exec_command("ls")
print(stdout.read().decode())
```

### **Q18. Deploy Kubernetes pod**  
```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
pod = client.V1Pod(metadata=client.V1ObjectMeta(name="nginx"), ...)
v1.create_namespaced_pod(namespace="default", body=pod)
```

### **Q19. Parse CLI arguments**  
```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args = parser.parse_args()
print(args.input)
```

### **Q20. Ping multiple servers**  
```python
import subprocess

servers = ["google.com", "github.com"]
for server in servers:
    result = subprocess.run(["ping", "-c", "1", server], capture_output=True)
    print(f"{server}: {'UP' if result.returncode == 0 else 'DOWN'}")
```

---

## **3. Patching & System Management**  
### **Q21. Check for OS updates**  
```python
import subprocess

def check_updates():
    subprocess.run(["sudo", "apt", "update"])
    result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True)
    print(result.stdout)
```

### **Q22. Automate patch deployment**  
```python
import subprocess

def apply_updates():
    subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)
```

### **Q23. Install packages from file**  
```python
with open("packages.txt") as f:
    packages = f.read().splitlines()

subprocess.run(["sudo", "apt", "install", "-y"] + packages)
```

### **Q24. Validate kernel parameters**  
```python
with open("/proc/sys/kernel/pid_max") as f:
    print(f"Max PID: {f.read()}")
```

### **Q25. Enforce password policies**  
```python
import subprocess

def set_password_policy():
    subprocess.run(["sudo", "passwd", "-x", "90", "user"])
```

---

## **4. APIs & Cloud Integrations**  
### **Q26. Call REST APIs**  
```python
import requests

response = requests.get("https://api.github.com")
print(response.json())
```

### **Q27. List EC2 instances (Boto3)**  
```python
import boto3

ec2 = boto3.client("ec2")
instances = ec2.describe_instances()
for reservation in instances["Reservations"]:
    for instance in reservation["Instances"]:
        print(instance["InstanceId"])
```

### **Q28. Manage Kubernetes resources**  
```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
print(v1.list_pod_for_all_namespaces())
```

### **Q29. Upload to S3**  
```python
import boto3

s3 = boto3.client("s3")
s3.upload_file("file.txt", "my-bucket", "key")
```

### **Q30. Handle API rate limiting**  
```python
import time
from requests.exceptions import RequestException

def call_api(url, retries=3):
    for i in range(retries):
        try:
            return requests.get(url).json()
        except RequestException:
            if i == retries - 1:
                raise
            time.sleep(2 ** i)  # Exponential backoff
```

---

## **5. Log Parsing & Monitoring**  
### **Q31. Parse Nginx logs for 5xx errors**  
```python
with open("/var/log/nginx/access.log") as f:
    for line in f:
        if " 500 " in line or " 503 " in line:
            print(line)
```

### **Q32. Tail log file in real-time**  
```python
import time

def tail_log(file):
    with open(file) as f:
        f.seek(0, 2)  # Go to end
        while True:
            line = f.readline()
            if line:
                print(line.strip())
            time.sleep(0.1)
```

### **Q33. Aggregate logs from multiple servers**  
```python
import paramiko

servers = ["server1", "server2"]
for server in servers:
    ssh = paramiko.SSHClient()
    ssh.connect(server)
    stdin, stdout, stderr = ssh.exec_command("cat /var/log/syslog")
    print(f"--- {server} ---")
    print(stdout.read().decode())
```

### **Q34. Extract metrics from logs**  
```python
import re

latencies = []
with open("app.log") as f:
    for line in f:
        match = re.search(r"latency=(\d+)ms", line)
        if match:
            latencies.append(int(match.group(1)))

print(f"Avg latency: {sum(latencies)/len(latencies)}ms")
```

### **Q35. Alert on log patterns**  
```python
def monitor_logs(logfile, pattern):
    with open(logfile) as f:
        for line in f:
            if pattern in line:
                send_alert(f"Found '{pattern}' in logs")

def send_alert(message):
    print(f"ALERT: {message}")
```

---

## **6. Infrastructure as Code (IaC)**  
### **Q36. Generate Terraform files**  
```python
import json

tf = {
    "resource": {
        "aws_instance": {
            "example": {
                "ami": "ami-123456",
                "instance_type": "t2.micro"
            }
        }
    }
}

with open("main.tf.json", "w") as f:
    json.dump(tf, f)
```

### **Q37. Validate Terraform syntax**  
```python
subprocess.run(["terraform", "validate"], check=True)
```

### **Q38. Deploy CloudFormation stacks**  
```python
import boto3

cf = boto3.client("cloudformation")
cf.create_stack(StackName="mystack", TemplateBody=open("template.yml").read())
```

### **Q39. Check IaC drift**  
```python
subprocess.run(["terraform", "plan"], check=True)
```

### **Q40. Manage secrets with Vault**  
```python
import hvac

client = hvac.Client(url="http://vault:8200")
secret = client.read("secret/data/myapp")
print(secret["data"]["password"])
```

---

## **7. Error Handling & Best Practices**  
### **Q41. Handle secrets securely**  
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file
password = os.getenv("DB_PASSWORD")
```

### **Q42. Retry flaky APIs**  
```python
import requests
from time import sleep

def get_with_retry(url, retries=3):
    for i in range(retries):
        try:
            return requests.get(url).json()
        except requests.exceptions.RequestException:
            if i == retries - 1:
                raise
            sleep(2 ** i)
```

### **Q43. Log to file and console**  
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logging.info("Hello world")
```

### **Q44. Idempotent script**  
```python
import os

if not os.path.exists("output.txt"):
    with open("output.txt", "w") as f:
        f.write("Data")
```

### **Q45. Profile script performance**  
```python
import cProfile

def slow_function():
    sum(range(10**6))

cProfile.run("slow_function()")
```

---

## **8. Networking & Security**  
### **Q46. Check open ports**  
```python
import socket

def is_port_open(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex((host, port)) == 0
```

### **Q47. Validate SSL expiry**  
```python
import ssl
import socket
from datetime import datetime

def check_cert(hostname):
    cert = ssl.get_server_certificate((hostname, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    expiry = x509.get_notAfter().decode("ascii")
    print(f"Expires on: {datetime.strptime(expiry, '%Y%m%d%H%M%SZ')}")
```

### **Q48. Block IPs in iptables**  
```python
subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", "1.2.3.4", "-j", "DROP"])
```

### **Q49. Encrypt/decrypt files**  
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
encrypted = cipher.encrypt(b"Secret data")

# Decrypt
decrypted = cipher.decrypt(encrypted)
```

### **Q50. Monitor network latency**  
```python
import subprocess

def ping_host(host):
    result = subprocess.run(["ping", "-c", "1", host], capture_output=True)
    if result.returncode == 0:
        time_line = [line for line in result.stdout.decode().split("\n") if "time=" in line][0]
        return float(time_line.split("time=")[1].split(" ")[0])
    return None
```

---