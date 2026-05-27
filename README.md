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
├── results
│   ├── alarms.log
│   └── valid_data.csv
├── src
│   └── astralog_mock.py
├── tests
│   └── test_astralog.py
│
├── README.md
├── requirements.txt
└── Singularity.def
```

<br>

## Roles

<br>

## DevOps design choices

<br>

## Difficulties

The main difficulty we had faced was **accessing Galileo100 HPC-cluster**. Each group member managed indeed to authenticate only after repeating [this procedure](https://docs.hpc.cineca.it/general/getting_started.html#get-str-card) multiple times.

Similarly, we spent several hours to fix the workflow inability to authenticate too. The first attempt we made consisted of trying to enter by using the static password we set for our CINECA accounts. However, the error output by GitHub actions

```text
2026/05/25 07:32:54 error copy file to dest: ***, error message: ssh: handshake failed: ssh: unable to authenticate, attempted methods [none publickey], no supported methods remain
drone-scp error: error copy file to dest: ***, error message: ssh: handshake failed: ssh: unable to authenticate, attempted methods [none publickey], no supported methods remain
```

suggested us that Galileo100 probably refuses this type of authentication. We then learnt that CINECA HPC clusters require instead to use the time-limited SSH certificate we generate every time via the smallstep CLI client, and there is no way to bypass such method on the workflow side. 

For this reason, we modified `main.yml` file in order to accomodate the use of the private key and certificate, finally succeeding in verifying our credentials.

<br>

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

However, although Claude mentioned using a virtual environment, the previous definition does not include it. Since CINECA system environment is managed by admins, we thought it could be useful to isolate everything in a safe (and reproducible) way by exploiting `venv`. 






