# Install Miniconda if not already installed
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

# Create R 4.0.5 environment with HTTPS support
conda create -n r405 r-base=4.0.5 -c conda-forge
conda activate r405
R
