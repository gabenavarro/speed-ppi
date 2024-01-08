# NVIDA Drivers

## Prerequisite

* Ubuntu 22.04
* Docker

*WSL Only*

* Docker Desktop
* wsl2
* Windows NVIDA Drivers

## Install

1. (WSL Only) Enable Docker on Ubuntu 22.04

Go to setting, resources, WSL integration, then enable integration for `Ubuntu-22.04` and hit refresh.


2. Install CUDA drivers on Linux
```bash
sudo apt-key del 7fa2af80 # Remove old key
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-3
```

3. Install NVIDIA container tool kit

Configure the production repository

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

Update the packages list from the repository

```bash
sudo apt-get update
```

Install the NVIDIA Container Toolkit packages

```bash
sudo apt-get install -y nvidia-container-toolkit
```

Configure the container runtime by using the nvidia-ctk command

```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

Restart windows docker.

4. Test installation

```bash
sudo docker run --rm --gpus all ubuntu nvidia-smi
```

Output should be the following if successful

```bash
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.86.10    Driver Version: 535.86.10    CUDA Version: 12.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
| N/A   34C    P8     9W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```


## Resources:
* https://docs.nvidia.com/cuda/wsl-user-guide/index.html 
* https://docs.nvidia.com/ai-enterprise/deployment-guide-vmware/0.1.0/docker.html#testing-docker-and-nvidia-container-runtime 
