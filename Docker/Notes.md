### Executive Summary

This masterclass delivers a comprehensive, hands-on guide to mastering Docker specifically tailored for data professionals, including **data engineers**, **AI engineers**, **data scientists**, and **analytics engineers**. Driven by the rapid expansion of AI and modern data stack requirements in 2026, Docker has shifted from an optional DevOps skill into an essential core competency for deploying machine learning APIs, automating agentic workflows, and running open-source platforms like Apache Airflow. The course systematically resolves the ubiquitous "it works on my machine" deployment failure by demonstrating how to package ETL scripts, Python runtimes, database dependencies, and REST APIs into portable units. Through five practical projects, learners progress from foundational container concepts to multi-container orchestration with Docker Compose, volume persistence, and image publishing on Docker Hub.

---

### Chronological Chapter-by-Chapter Breakdown (with Timestamps)

#### 1. [00:00] Introduction & Docker's Emergence in the Data Domain
* **Core Relevance**: Explains why Docker is becoming the top requested skill for data professionals in 2026 due to the blend of software engineering and data engineering in AI workflows.

* **Shift in Industry Expectations**: Data engineers previously avoided containerisation, viewing it purely as a CI/CD or DevOps responsibility; now, job postings across top tech companies mandate Docker for building end-to-end data pipelines and serving endpoints.
* **Masterclass Scope**: Covers theoretical fundamentals alongside live hands-on building of Python containers, REST APIs, SQL database integration, custom bridge networks, Docker Compose stacks, and persistent volumes.

#### 2. [08:15] Chapter 1: What is Docker & Why Do Data Professionals Need It?
* **Definition**: Docker is a platform designed to package, distribute, and execute applications inside lightweight, isolated units called **containers**.
* **The "Works on My Machine" Dilemma**: Illustrates a common scenario where a data engineer builds an ETL pipeline (e.g., Python + Apache Spark) in a local development environment that fails upon deployment to QA or Production.
* **Root Causes Solved**: Eliminates environment mismatches caused by conflicting Python versions (e.g., 3.12 vs. 3.10), missing library dependencies (Pandas, PySpark), mismatched Spark runtimes (e.g., 4.1 vs 3.4), or operating system configuration differences.
* **Lift and Shift Capability**: Containerisation packages application code, specific interpreter versions, libraries, runtimes, database connectors, and port mappings into a standardized unit that runs identically across Dev, QA, and Production environments.

#### 3. [22:30] Chapter 2: Deep Dive into Containers vs. Virtual Machines Architecture
* **Container Architecture**: Containers are lightweight, isolated process spaces that share the **Host Operating System Kernel**. They possess their own isolated file systems, dependencies, and process spaces without carrying a dedicated OS kernel.
* **Virtual Machine (VM) Architecture**: A traditional VM runs on top of a Hypervisor (e.g., VMware) and requires an entire **Guest Operating System** (including Guest OS Kernel, virtual RAM, and hardware drivers) for every single instance.
* **Comparative Analogy**: VMs are like fully independent apartments in a building (carrying dedicated utility infrastructure), whereas Docker containers are like private rooms sharing the building's central infrastructure (Host OS Kernel).
* **Performance Impact**: Because containers bypass hypervisor abstraction and guest OS boot cycles, they spin up instantly in seconds and consume significantly fewer CPU/RAM resources than VMs.

#### 4. [38:45] Chapter 3: Docker Images, Layers, and Base Images
* **Docker Image vs. Container**:
  * **Image**: An immutable, read-only package/blueprint containing source code, runtimes, system libraries, and instructions required to run an application (analogous to a recipe).
  * **Container**: The isolated, running instance of a Docker image (analogous to the prepared meal).
* **Image Layering Architecture**:
  * Built sequentially on top of a **Base Image** (e.g., `python:3.8-slim`, `mysql:8.0`) drawn from Docker Hub.
  * Every instruction in a Dockerfile adds a read-only layer to the image stack.
* **Writable Container Layer**: When a container is launched from an image, Docker adds a thin **read-write layer** on top of the immutable read-only image layers. Container modifications happen in this writable layer, preserving the underlying image's immutability.

#### 5. [55:00] Chapter 4: Environment Setup & Docker Desktop with WSL 2
* **Hardware Prerequisites**: Verifying that CPU Virtualization is enabled in Task Manager / BIOS.
* **Windows Configuration**: Enabling **Windows Subsystem for Linux (WSL)** and **Virtual Machine Platform** features via Windows Features control panel, followed by a system reboot.
* **Docker Desktop & WSL 2 Integration**:
  * Installing Docker Desktop and enabling the WSL 2-based engine under *Settings -> Resources*.
  * Running `wsl --install` and installing an Ubuntu Linux distribution (`wsl --install -d Ubuntu`).
  * Verifying active WSL distributions using `wsl -l -v`.
* **Troubleshooting Tip**: Ending frozen background Docker processes via Windows Task Manager or system tray icon if Docker Desktop fails to initialize.

#### 6. [1:15:00] Chapter 5: Project 1 – Containerizing Your First Python Application
* **Project Setup**: Initializing a project directory using modern Python package tools like `uv` (`uv init`) or standard files.
* **Building `app.py`**: Creating a simple Python script executing print statements.
* **Crafting the `Dockerfile`**:
  * `FROM python:3.8-slim`: Utilizing a lightweight (~46MB) official base image rather than a standard full distribution (~300MB).
  * `WORKDIR /app`: Setting the internal container working directory.
  * `COPY . /app`: Copying local files into the image directory.
  * `CMD ["python", "app.py"]`: Defining the container entry execution command formatted as a JSON array.
* **CLI Operations**:
  * Building the image: `docker build -t first-python-app .`.
  * Version tagging: `docker build -t first-python-app:0.1 .`.
  * Running container: `docker run --name first-python-container first-python-app`.
  * Interactive shell inspection: `docker run -it first-python-app bin/sh`.
  * Lifecycle management: Inspecting running containers (`docker ps`, `docker ps -a`), stopping (`docker stop`), removing containers (`docker rm`), and deleting images (`docker rmi`).

#### 7. [1:48:00] Chapter 6: Project 2 – REST API Deployment & Port Mapping with Flask
* **AI Data Engineering Context**: Modern data professionals must deploy API endpoints to trigger ETL scripts and expose data models.
* **Flask REST API (`app.py`)**: Defining routes (`/`, `/about`, `/contact`), binding to host `0.0.0.0` on internal port `5000`.
* **Optimized Dockerfile Steps**:
  * Copying code and installing dependencies via `RUN pip install --no-cache-dir -r requirements.txt`.
* **Core Concept – Port Mapping**:
  * Explain that container internal networks are isolated from `localhost`.
  * To access a containerized service from a browser/host machine, internal container ports must be mapped to host ports using the `-p <host_port>:<container_port>` flag.
  * Execution: `docker run -d -p 5000:5000 --name flask_container flask_image`.

#### 8. [2:18:00] Chapter 7: Project 3 – Multi-Container Systems & Docker Networks
* **The Network Isolation Problem**: By default, containers launch on separate isolated bridge networks and cannot communicate using `localhost`.
* **MySQL Database Container Setup**:
  * Dockerfile based on `mysql:8.0`.
  * Configuring environment variables (`ENV MYSQL_ROOT_PASSWORD=demo_password`, `ENV MYSQL_DATABASE=demo_DB`).
  * Auto-seeding database schemas by copying `init.sql` scripts into the official `/docker-entrypoint-initdb.d/` startup directory.
  * Mapping host port `3307` to container port `3306` (`-p 3307:3306`) to prevent conflicts with local MySQL instances running on the host machine.
* **Docker Custom Bridge Networks**:
  * Creating a custom bridge network: `docker network create an_network`.
  * Attaching containers: Running both MySQL and Flask containers on `an_network`.
* **Internal DNS Resolution**: In custom networks, containers resolve each other using **container names** as hostnames (e.g., `host="mysql_container"`) instead of `localhost` or hardcoded IP addresses.
* **Container CLI Inspection**: Using `docker exec -it mysql_container mysql -u root -p` to query database tables directly inside the running container.

#### 9. [2:55:00] Chapter 8: Project 4 – Microservices Orchestration using Docker Compose
* **Why Docker Compose?**: Manually running multiple `docker run` CLI commands with network connections, environment variables, port mappings, and start-up dependencies is complex and unscalable.
* **Orchestration with `docker-compose.yml`**:
  * Declares multi-container applications in a human-readable YAML configuration file.
  * Configures services (`mysql_container` and `flask_container`), image builds, environment keys, ports, and automatic network creation.
* **Startup Dependencies & Health Checks**:
  * Adding a `healthcheck` (`mysqladmin ping`) to ensure MySQL is fully initialized before the API attempts connection.
  * Enforcing start sequence using `depends_on: { mysql_container: { condition: service_healthy } }`.
* **Stack Management Commands**: Launching the full stack with `docker-compose up -d`, rebuilding with `docker-compose up --build -d`, and tearing down resources with `docker-compose down`.

#### 10. [3:28:00] Chapter 9: Project 5 – Persistent Data Storage with Volumes & Bind Mounts
* **The Ephemeral Container Problem**: Standard container filesystems are temporary; when a database container is removed or updated, all stored database records are lost.
* **Docker Storage Mechanisms**:
  * **Bind Mounts**: Directly mounting a specific host machine folder/file into the container path (e.g., mounting `./mysql/init.sql` to `/docker-entrypoint-initdb.d/init.sql`). Ideal for live code development and local configuration scripts.
  * **Named Volumes**: Persistent storage areas created and managed entirely by Docker on the host filesystem (`/var/lib/docker/volumes/`) decoupled from the container lifecycle.
* **Data Persistence Workflow**:
  * Creating and mounting a volume (`-v an_volume:/var/lib/mysql`).
  * Inserting SQL database records, completely destroying the MySQL container, launching an entirely new container connected to `an_volume`, and confirming that all data remains intact.

#### 11. [3:50:00] Chapter 10: Publishing Custom Images to Docker Hub & Next Steps
* **Distributing Data Images**: Pushing custom pre-configured container images to **Docker Hub** enables seamless deployment across cloud instances and team members without sharing underlying source code.
* **Publishing Steps**:
  * Tagging image with Docker Hub username: `docker build -t <username>/<repository>:<tag> .`.
  * Authenticating via CLI: `docker login`.
  * Pushing image: `docker push <username>/<repository>:<tag>`.
* **Pulling Remote Images**: Demonstrating how anyone can run `docker run -d -p 5000:5000 <username>/<repository>:<tag>` to execute the container instantly from anywhere.
* **Next Steps for AI Data Engineers**: Mastering Python core concepts, Git/GitHub version control, and orchestrating workflow pipelines with Apache Airflow.

---

### Core Concepts & Data Domain Applications

```
+-----------------------------------------------------------------------------------+
|                                  DOCKER ENGINE                                    |
|                                                                                   |
|  +-------------------------------+             +-------------------------------+  |
|  |       FLASK_CONTAINER         |             |        MYSQL_CONTAINER        |  |
|  |  +-------------------------+  |             |  +-------------------------+  |  |
|  |  | Writable Layer (App)    |  |             |  | Writable Layer (DB)     |  |  |
|  |  +-------------------------+  |   Internal  |  +-------------------------+  |  |
|  |  | Read-Only Image Layers  |  |<----------->|  | Read-Only Image Layers  |  |  |
|  |  | (Python 3.8 Slim, App)  |  | DNS Name:   |  | (MySQL 8.0 Base Image)  |  |  |
|  |  +-------------------------+  | "mysql_ctn" |  +-------------------------+  |  |
|  +--------------+----------------+             +--------------+----------------+  |
|                 | Port 5000                                   | Port 3306         |
|                 |                                             |                   |
|                 |          CUSTOM BRIDGE NETWORK              |                   |
|                 +---------------------------------------------+                   |
+-----------------------------------------+-----------------------------------------+
                                          |                                |
                        Port Mapping      | Host Port                      | Named Volume
                       (-p 5000:5000)     | Mapping (-p 3307:3306)         | (-v an_volume:/var/lib/mysql)
                                          v                                v
+-----------------------------------------------------------------------------------+
|                                HOST MACHINE (LOCAL)                               |
|  Browser Access: http://localhost:5000      MySQL Workbench: localhost:3307       |
|  Persistent Volume Location: /var/lib/docker/volumes/an_volume/_data             |
+-----------------------------------------------------------------------------------+
```

#### 1. Containers vs. Virtual Machines
* **Explanation**: Containers share the Host OS Kernel and run isolated processes in user space, whereas VMs require hypervisors and complete Guest Operating Systems.
* **Data Domain Application**: Enables rapid startup of lightweight, disposable execution environments for running ETL scripts, PySpark jobs, or isolated database instances without the heavy resource overhead of full virtual machines.

#### 2. Docker Images & Layer Architecture
* **Explanation**: Read-only, immutable templates composed of stacked instructions (`FROM`, `WORKDIR`, `COPY`, `RUN`).
* **Data Domain Application**: Locks and version-controls exact environment specifications (e.g., Python 3.8 + Pandas + PySpark) across Dev, QA, and Production pipelines, preventing execution drift.

#### 3. Dockerfile
* **Explanation**: Text blueprint containing sequential commands used by Docker Engine to assemble custom container images.
* **Data Domain Application**: Codifies data pipeline setup—installing exact package manifests (`pip install -r requirements.txt`) and copying ETL scripts so jobs execute reproducibly anywhere.

#### 4. Port Mapping / Forwarding
* **Explanation**: Exposing isolated container internal network ports to host machine network interfaces using `-p host_port:container_port`.
* **Data Domain Application**: Allows data engineers to access containerized Flask/FastAPI REST endpoints via web browsers or connect local tools (e.g., MySQL Workbench, DBeaver) to containerized databases on custom ports.

#### 5. Docker Networks
* **Explanation**: Isolated virtual bridge networks enabling containers attached to the same network to communicate seamlessly.
* **Data Domain Application**: Enables secure container-to-container communication (e.g., Flask ingestion API sending data to a MySQL database) using container names as hostnames via Docker's internal DNS.

#### 6. Docker Compose
* **Explanation**: Declarative YAML tool for defining, configuring, and orchestrating multi-container stacks, startup ordering, health checks, and networks.
* **Data Domain Application**: Simplifies management of complex modern data stacks (e.g., pairing Apache Airflow Webserver/Scheduler, PostgreSQL metadata DB, and Redis queues into a single command setup).

#### 7. Volumes & Bind Mounts
* **Explanation**: Persistence mechanisms that decouple stored data from container lifecycles. Bind mounts point directly to host paths, while Named Volumes are managed by Docker.
* **Data Domain Application**: Prevents catastrophic data loss by persisting database storage (`/var/lib/mysql`), mounting SQL initialization scripts, and feeding large CSV/Parquet datasets into containers without increasing image sizes.

---

### Hands-on Command Reference & Code Snippets

#### 1. Essential Docker CLI Commands

* **Environment & Verification**:
  * `wsl --install`: Installs Windows Subsystem for Linux.
  * `wsl -l -v`: Lists installed WSL distributions and their running versions.
  * `wsl --install -d Ubuntu`: Installs Ubuntu distribution for WSL 2 backend.

* **Image Management**:
  * `docker pull <image_name>:<tag>`: Downloads base image from Docker Hub.
  * `docker image ls`: Lists all locally available images.
  * `docker rmi <image_id_or_name>`: Deletes a local image.
  * `docker build -t <image_name>:<tag> <context_path>`: Builds image from Dockerfile (e.g., `docker build -t first-python-app:0.1 .`).

* **Container Operations**:
  * `docker run [flags] <image_name>`: Instantiates and launches a container.
    * `-d`: Detached mode (runs container in background).
    * `-p <host_port>:<container_port>`: Maps host port to container port.
    * `--name <container_name>`: Assigns a custom name to container.
    * `-it`: Launches interactive terminal shell.
    * `--network <network_name>`: Attaches container to specified network.
    * `-v <volume_name>:<container_path>`: Mounts persistent volume.
  * `docker ps`: Lists running containers.
  * `docker ps -a`: Lists all containers (running and stopped).
  * `docker stop <container_id_or_name>`: Gracefully stops container.
  * `docker rm <container_id_or_name>`: Removes a stopped container.
  * `docker exec -it <container_name> <command>`: Executes command inside a running container (e.g., `docker exec -it mysql_container mysql -u root -p`).

* **Networking & Volumes**:
  * `docker network create <network_name>`: Creates custom bridge network.
  * `docker network ls`: Lists networks.
  * `docker network rm <network_name>`: Removes network.
  * `docker volume ls`: Lists Docker volumes.

* **Docker Compose & Hub**:
  * `docker-compose up -d`: Launches all services in detached mode.
  * `docker-compose up --build -d`: Rebuilds images and launches services.
  * `docker-compose down`: Stops and destroys all stack containers and networks.
  * `docker login`: Authenticates CLI with Docker Hub.
  * `docker push <username>/<repository>:<tag>`: Uploads custom image to Docker Hub.

---

#### 2. Complete Code Snippets & Dockerfiles

##### A. Project 1: Basic Python Script Dockerfile (`Dockerfile`)
```dockerfile
# Pull official lightweight Python base image from Docker Hub
FROM python:3.8-slim

# Set internal working directory in image
WORKDIR /app

# Copy host files into container working directory
COPY . /app

# Execution command when container starts
CMD ["python", "app.py"]
```

##### B. Project 2: Flask REST API Dockerfile (`Dockerfile`)
```dockerfile
# Base Python runtime
FROM python:3.8-slim

# Working directory setup
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies without caching build files
RUN pip install --no-cache-dir -r requirements.txt

# Run Flask REST API
CMD ["python", "app.py"]
```

##### C. Project 3: MySQL Database Dockerfile (`Dockerfile`)
```dockerfile
# Pull official MySQL 8.0 base image
FROM mysql:8.0

# Set environment variables for default root credentials & DB
ENV MYSQL_ROOT_PASSWORD=demo_password
ENV MYSQL_DATABASE=demo_DB

# Copy schema setup SQL script into entrypoint auto-execution folder
COPY init.sql /docker-entrypoint-initdb.d/

# Document internal database port
EXPOSE 3306
```

##### D. Project 4 & 5: Microservices Orchestration (`docker-compose.yml`)
```yaml
version: '3.1' # Specification format version

services:
  # Database Service Configuration
  mysql_container:
    image: mysql:8.0 # Pull base image directly
    container_name: mysql_container
    restart: always
    command: --default-authentication-plugin=mysql_native_password
    environment:
      MYSQL_ROOT_PASSWORD: demo_password
      MYSQL_DATABASE: demo_DB
    ports:
      - "3307:3306" # Map host port 3307 to internal port 3306
    volumes:
      - an_volume:/var/lib/mysql # Persistent volume mount
      - ./mysql/init.sql:/docker-entrypoint-initdb.d/init.sql # Bind mount script
    healthcheck: # Ensure DB is ready before starting dependent app
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p$$MYSQL_ROOT_PASSWORD"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Flask REST API Service Configuration
  flask_container:
    build: ./flask # Path to Flask Dockerfile
    container_name: flask_container
    restart: always
    ports:
      - "5000:5000" # Map API port
    depends_on:
      mysql_container:
        condition: service_healthy # Wait for DB healthcheck pass

# Persistent Volume Definitions
volumes:
  an_volume:
```

---

### Key Takeaways & Best Practices

* **Opt for Slim Base Images**: Always choose slim base image variants (e.g., `python:3.8-slim`) over standard distributions to reduce overall image footprints from ~300MB+ down to ~45MB, accelerating build times and deployment speed.
* **Leverage `--no-cache-dir` in Pip**: When installing Python packages in Dockerfiles (`RUN pip install --no-cache-dir -r requirements.txt`), include `--no-cache-dir` to prevent storing transient wheel packages, keeping image layers lightweight.
* **Avoid Hardcoded `localhost` for Inter-Container Calls**: Containers cannot reach other services on `localhost`. Always run multi-container applications on custom bridge networks and reference target containers by their **container names** via Docker's internal DNS.
* **Always Persist Database State with Volumes**: Never store database records on local container filesystems. Attach **Named Volumes** to data directories (e.g., `/var/lib/mysql`) so data persists across container destruction and restarts.
* **Prevent Port Collisions**: When running local databases on host machines (e.g., local MySQL on 3306), map container database ports to alternative host ports (e.g., `-p 3307:3306`) to avoid host port binding conflicts.
* **Implement Startup Healthchecks in Compose**: Database containers report as "running" before the database server is ready to handle queries. Always pair `healthcheck` ping commands with `depends_on: { condition: service_healthy }` in `docker-compose.yml` to prevent connection errors during app startup.
* **Tag Images Explicitly**: Avoid relying on implicit `latest` image tags in production workflows. Tag images explicitly with version numbers (e.g., `v0.0.1`) to ensure full auditability and deployment rollback capabilities.
* **Use Detached Mode for Background Services**: Use the detached flag (`-d` or `-dp`) for background services (APIs, databases) to maintain an interactive and clean terminal shell.

---
