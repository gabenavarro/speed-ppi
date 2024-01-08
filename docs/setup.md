# Setup Guide for Dockerized SpeedPPI 

Welcome to the setup guide for dockerized `speed-ppi`. This guide will walk you through the steps to get SpeedPPI running in a Docker container for jupyter notebook purposes or to use as part of a kubeflow pipeline.

## 1. Prerequisite

Before proceeding, ensure you have the following installed:
- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/downloads)
- [NVIDIA Drivers](/docs/wsl2_gpu.md)

If hosting on cloud server, such as AWS, GPC, or Azure, please make an account and make sure you have all the appropriate permissions. 

## 2. Local Development

### Setup

* Clone repository to your local drive

```bash
# Clone repository
git clone git@github.com:gabenavarro/speed-ppi.git
# Jump into repository
cd ./speed-ppi
```

* Build docker image from docker file

```bash
# Build image
docker build -f Dockerfile.dev -t speed-ppi:dev .
```

* Download sequence database for MSA

```bash
bash ./assets/dockfold_uniclust_setup.sh `$LOCAL_UNICLUST_DIR`
```

`LOCAL_UNICLUST_DIR`: local directory to download sequence database. For example `/home/$USER/data/uniclust30`. This directory will be mounted to the docker container in the following step.

* Run the docker container from docker image

```bash
# Run container
docker run -d \
  --gpus all \
  --name speed-ppi-dev \
  -v $(pwd)/:/app/ \
  -v `$LOCAL_UNICLUST_DIR`/:/opt/uniclust30_2018_08/ \
  -v `$LOCAL_MSA_DIR`/:/opt/msa/ \
  -v `$LOCAL_PDB_DIR`/:/opt/pdb/ \
  -v `$LOCAL_PQS_DIR`/:/opt/pqs/ \
  speed-ppi:dev
```

`LOCAL_MSA_DIR`: local directory to download sequence database. For example `/home/$USER/data/dockfold_msa`. This directory will be mounted to the docker container during local development and could be synced with cloud storage.

`LOCAL_PDB_DIR`: local directory to download pdb database. For example `/home/$USER/data/dockfold_pdb`. This directory will be mounted to the docker container during local development and could be synched with cloud storage.

`LOCAL_PRQ_DIR`: local directory to save dockfold result tables as a parquet. For example `/home/$USER/data/dockfold_pqs`. This directory will be mounted to the docker container during local development and could be synched with cloud storage.

Make sure that `LOCAL_UNICLUST_DIR` corresponds to the download directory of the uniclust30 database. This is where HHblits will be looking for sequences for MSA within the docker container. An example for how this command looks for my personal profile:

```bash
docker run -d \
  --gpus all \
  --name speed-ppi-dev \
  -v $(pwd)/:/app/ \
  -v /home/gnava/data/uniclust30/:/opt/uniclust30_2018_08/ \
  -v /home/gnava/data/dockfold_msa/:/opt/msa/ \
  -v /home/gnava/data/dockfold_pdb/:/opt/pdb/ \
  -v /home/gnava/data/dockfold_pqs/:/opt/pqs/ \
  speed-ppi:dev
```


## 3. GCP Deployment

### Prerequisite

1. Access to Google Cloud Artifact Registry. 

This allows your local computer to access and deposite docker images to GCP to create Kubernete containers during pipeline run.

Install Google Cloud SDK.

```bash
curl https://sdk.cloud.google.com | bash
```
 
After installing, restart shell and initialize GCP credentials.
```bash
gcloud init
```

Lastly, configure docker to have access to GCP project registry. This configuration is zone specific and each intended working zone needs to be added.

```bash
gcloud auth configure-docker `$GCP_ARTIFACT_REGION`
```

* `GCP_ARTIFACT_REGION` is where Google's cloud artifact repositories are hosted. Examples: 
    * `us-central1-docker.pkg.dev`
    * `us-west1-docker.pkg.dev`

2. Download sequence databased on to cloud buckets. 

This is required for the cloud environemnt to have access to sequence database for multiple sequence alignemnt.

```bash
bash ./assets/dockfold_uniclust_setup.sh `$LOCAL_UNICLUST_DIR` `$CLOUD_BUCKET`
```

* `LOCAL_UNICLUST_DIR`: local directory to download sequence database. Ideally this is the same directory that will be used for docker container volume mount. For example `/home/$USER/data/uniclust30`
* `CLOUD_BUCKET`: gs:// formatted gcp bucket directory to deposit sequence database too. Location will be important to direct cloud based 

### Setup

* Clone repository to your local drive

```bash
# Clone repository
git clone git@github.com:gabenavarro/speed-ppi.git
# Jump into repository
cd ./speed-ppi
```

* Build docker production image from docker file and push image to Google's artifact registry

```bash 
bash ./assets/artifact_registry.sh \
  `$DOCKER_IMAGE_NAME` \
  `$GCP_ARTIFACT_REGION/$PROJECT_ID/$REPOSITORY/$DOCKER_IMAGE_NAME` 
```

* `DOCKER_IMAGE_NAME`: name of docker image to build locally. For example `speed-ppi:prod`
* `GCP_ARTIFACT_REGION` is where Google's cloud artifact repositories are hosted. Examples: 
    * `us-central1-docker.pkg.dev`
    * `us-west1-docker.pkg.dev`
* `PROJECT_ID`: Google account project id. Keep in mind there can be many different project id's per account.
* `REPOSITORY`: Artifact registry repository name. 

For my personal setting, it is:

```bash 
bash ./assets/artifact_registry.sh \
  speed-ppi:prod \
  us-central1-docker.pkg.dev/noble-office-299208/mercy-of-toren/speed-ppi:prod
```