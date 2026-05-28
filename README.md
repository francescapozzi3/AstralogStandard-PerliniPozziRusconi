### Software Engineering for HPC - A.Y. 2025/2026

**Authors**: Micaela Perlini, Francesca Marina Pozzi, Martina Rusconi.  
**Track name**: Standard.

<br>

# AstraLog-HPC

This repository provides a mock environment for the telemetry analysis software used in the *"Software Engineering for HPC"* course. More information can be retrieved [here](instructions/README.md).

## Repository Structure

<!-- Use 'tree' command from terminal to get folder structure. -->

```text
.
├── input
│   ├── rules.json
│   └── telemetry_cleaned.csv
├── instructions
│   └── README.md
├── logs
│   ├── 20522389_error.log
│   └── 20522389_output.log
├── results
│   ├── alarms.log
│   └── valid_data.csv
├── src
│   └── astralog_mock.py
├── tests
│    └── test_astralog.py
├── README.md
├── requirements.txt
├── Singularity.def
└── job.sh
```

## Roles

<br>

## DevOps design choices

### CI/CD Pipeline

- The pipeline is triggered on every `push`.

- All necessary dependencies are installed via `pip install -r requirements.txt`.

- The test suite is executed with `python3 -m pytest -v`.

### Containerization 

- The `%files` section packages `src/`, `input/`, and `requirements.txt` into the image, and the `%runscript` one makes the container directly executable with `"$@"`, forwarding all arguments through (such syntax means exactly "*pass along whatever arguments the user provides*"). 

- **Reproducibility** means that *anyone who builds this container at any point in time gets the exact same environment*. This is achieved in three ways: the base image is pinned to `python:3.11-slim` (a specific, well-known version rather than just "latest"), the Apptainer build tool is locked to version `1.3.6` in CI, and `--no-cache-dir` ensures `pip` always fetches fresh, consistent packages rather than reusing potentially cached ones. 

- The virtual environment inside the container is slightly redundant, but it keeps Python environment tidy.

### HPC Execution

- The application runs inside the container via `singularity run`, meaning the job always executes inside the container, fully isolated from whatever Python version or libraries happen to be installed on the cluster nodes.

- The `--bind` flags create a **bridge** between the cluster's filesystem and the container's internal filesystem, keeping the data outside the image, so the same container can be reused with different datasets without rebuilding.

- Logs are separated into `stdout`/`stderr` files and namespaced by SLURM job ID (`%j`), so concurrent runs never overwrite each other.

### Automation

The `deploy-and-run` job transfers the SIF file, `job.sh`, and the `input/` directory to the cluster via `scp` with certificate-based SSH authentication, whose credentials are stored as GitHub Actions secrets. It then opens an SSH session, moves files into the repo directory, clears old logs, and calls `sbatch job.sh`. The full chain from `push` to running HPC job is automated with no manual steps.

### Application and tests implementation

The application source code and test suite are unchanged from the provided template, since the focus of the project was entirely on the surrounding infrastructure.

## Difficulties

The main difficulty we had faced was **accessing Galileo100 HPC-cluster**. Each group member managed indeed to authenticate only after repeating [this procedure](https://docs.hpc.cineca.it/general/getting_started.html#get-str-card) multiple times.

Similarly, we spent several hours to fix the workflow inability to authenticate too. The first attempt we made consisted of trying to enter by using the static password we set for our CINECA accounts. However, the error output by GitHub actions

```text
2026/05/25 07:32:54 error copy file to dest: ***, error message: ssh: handshake failed: ssh: unable to authenticate, attempted methods [none publickey], no supported methods remain
drone-scp error: error copy file to dest: ***, error message: ssh: handshake failed: ssh: unable to authenticate, attempted methods [none publickey], no supported methods remain
```

suggested us that Galileo100 probably refuses this type of authentication. We then learnt that CINECA HPC clusters require instead to use the time-limited SSH certificate we generate every time via the `smallstep` CLI client, and there is no way to bypass such method on the workflow side. 

For this reason, we modified `main.yml` file in order to accomodate the use of the private key and certificate, finally succeeding in verifying our credentials.

## AI Tools usage

The first version of our Singularity container was simple:

```text
Bootstrap: docker
From: python:3.11-slim
    
%post
    pip install --no-cache-dir -r /app/requirements.txt 
    
%environment
    export PYTHONPATH=/app

%files
    src /app/src
    input /app/input
    tests /opt/astralog/tests
    requirements.txt /app/requirements.txt
    
%runscript
    cd /app
    exec python -m src.astralog_mock "$@
```

<br>

We therefore asked **Claude AI** if such definition was enough for HPC usage. The answer read:

> *For an HPC cluster, no, important things are missing:* 
>- *No* `build-essential` *— if any package in* `requirements.txt` *compiles C/C++ code (e.g., numpy, pandas), the build fails.*
>- *No* `venv` *— on HPC, system's Python environment can be managed/modified by the admin.*
>- *Outdated* `pip` *— Older versions of* `pip` *may not resolve dependencies correctly.*
>- *Missing* `PYTHONUNBUFFERED=1` *— On clusters, logs are written to files. Without this variable, the output may be lost or appear out of order.*
>
> *Minimal but robust version:*
>
> ```text
>Bootstrap: docker
>From: python:3.11-slim
>
>%environment
>    export PYTHONUNBUFFERED=1
>    export PYTHONDONTWRITEBYTECODE=1
>    export PYTHONPATH=/app
>
>%post
>    apt-get update && apt-get install -y -no-install-recommends 
>        build-essential \
>    && rm -rf /var/lib/apt/lists/*
>    pip install --no-cache-dir --upgrade pip
>    pip install --no-cache-dir -r /app/requirements.txt
>
>%files
>    src /app/src
>    input /app/input
>    requirements.txt /app/requirements.txt
>
>%runscript
>    cd /app
>    exec python -m src.astralog_mock "$@"
>```

We then decided to integrate this new version, in order to correctly package the application and its dependencies. Here, **reproducibility** is granted since:
- The base image uses a precise version.
- The latest version of `pip` is ensured.
- Container dimension is small.

<br>

However, although Claude mentioned using a virtual environment, the previous definition does not include it. Since CINECA system environment is managed by admins, we thought it could be useful to isolate everything even more in a safe (and reproducible) way by exploiting `venv`. 






