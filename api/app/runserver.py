FROM amazonlinux:latest

# Install dependencies
RUN yum update -y && yum install -y wget bzip2

# Download and install Miniconda silently
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/miniconda && \
    rm /tmp/miniconda.sh

# Update PATH
ENV PATH="/opt/miniconda/bin:$PATH"

# Verify conda
RUN conda --version
