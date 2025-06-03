FROM amazonlinux:2

# Install dependencies, including Fortran compiler
RUN yum -y update && \
    yum -y install \
        gcc gcc-c++ gcc-gfortran make \
        wget tar gzip \
        libcurl-devel openssl-devel libxml2-devel \
        readline-devel zlib-devel bzip2-devel xz-devel && \
    yum clean all

# Install R 4.0.5
RUN curl -O https://cran.r-project.org/src/base/R-4/R-4.0.5.tar.gz && \
    tar -xf R-4.0.5.tar.gz && \
    cd R-4.0.5 && \
    ./configure --enable-R-shlib --with-x=no && \
    make -j4 && \
    make install

# Test installation
RUN Rscript -e 'version'
