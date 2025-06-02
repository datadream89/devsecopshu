FROM amazonlinux:2

# Install system dependencies
RUN yum update -y && \
    yum install -y wget bzip2 git make gcc which

# Install Miniconda (silent)
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh

# Set conda in PATH
ENV PATH="/opt/conda/bin:$PATH"

# Init Conda for bash
RUN /opt/conda/bin/conda init bash

# Create Conda env with R 4.0.5 and packages
RUN conda create -y -n r_env -c conda-forge \
    r-base=4.0.5 \
    r-essentials \
    r-tidyverse \
    r-data.table \
    r-devtools \
    r-curl \
    r-ggplot2 \
    r-readr \
    r-dplyr

# Use bash shell for all following instructions
SHELL ["/bin/bash", "-c"]

# Auto-activate env in bash
RUN echo "conda activate r_env" >> ~/.bashrc

# Create directory for scripts
RUN mkdir -p /opt/r-scripts

# Add sample R script
COPY sample_script.R /opt/r-scripts/sample_script.R

# Run sample script during build to validate packages
RUN source ~/.bashrc && \
    conda activate r_env && \
    Rscript /opt/r-scripts/sample_script.R

# Set working directory
WORKDIR /opt/r-scripts

# Start container in bash with R env active
CMD ["bash", "-c", "source ~/.bashrc && R"]
