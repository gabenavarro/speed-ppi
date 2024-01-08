# Arguments for Tensorflow and CUDA versions
ARG CUDA=11.1
ARG TENSORFLOW=2.12.0
# Pull image
FROM tensorflow/tensorflow:${TENSORFLOW}-gpu
# Restate 
ARG CUDA
ARG TENSORFLOW

# OS dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        build-essential \
        wget \
        git \
        openssh-server && \
    CUDA_VERSION=$(echo $CUDA | tr '.' '-') && \
    apt-get install --no-install-recommends -y cuda-command-line-tools-$CUDA_VERSION

# Install HHBlits
RUN mkdir /opt/hh-suite \
    && wget https://github.com/soedinglab/hh-suite/releases/download/v3.3.0/hhsuite-3.3.0-AVX2-Linux.tar.gz -P /opt/hh-suite \
    && tar xvfz /opt/hh-suite/hhsuite-3.3.0-AVX2-Linux.tar.gz -C /opt/hh-suite \
    && rm /opt/hh-suite/hhsuite-3.3.0-AVX2-Linux.tar.gz
ENV PATH="/opt/hh-suite/bin:/opt/hh-suite/scripts:${PATH}"

# Install AlphaFold2 parameters
RUN mkdir /opt/data /opt/data/params \
    && wget https://storage.googleapis.com/alphafold/alphafold_params_2021-07-14.tar \
    && mv alphafold_params_2021-07-14.tar /opt/data/params \
    && tar -xf /opt/data/params/alphafold_params_2021-07-14.tar \
    && mv params_model_1.npz /opt/data/params \
    && rm /opt/data/params/alphafold_params_2021-07-14.tar

# Install required python packages
COPY /assets/requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir \
    -r /app/requirements.txt

# Install source code
COPY /src /app/src/
COPY /alphafold /app/alphafold/
COPY /cpu_hhblits.py /app/
COPY /gpu_dockfold.py /app/
WORKDIR /app
