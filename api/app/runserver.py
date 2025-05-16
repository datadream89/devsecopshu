FROM amazonlinux:2023

# Install build tools and dependencies
RUN yum groupinstall -y "Development Tools" && \
    yum install -y \
    gcc gcc-c++ gcc-gfortran \
    readline-devel \
    zlib-devel \
    bzip2-devel \
    xz-devel \
    libcurl-devel \
    libpng-devel \
    libjpeg-devel \
    cairo-devel \
    pango-devel \
    freetype-devel \
    tcl-devel \
    tk-devel \
    texinfo \
    tar \
    curl \
    make \
    openssl-devel \
    libX11-devel \
    libXt-devel

# Download and install R from source
ENV R_VERSION=4.3.1
RUN curl -O https://cran.r-project.org/src/base/R-4/R-${R_VERSION}.tar.gz && \
    tar -xzf R-${R_VERSION}.tar.gz && \
    cd R-${R_VERSION} && \
    ./configure --enable-R-shlib && \
    make && make install && \
    cd .. && rm -rf R-${R_VERSION}*

# Install a sample R package
RUN Rscript -e "install.packages('ggplot2', repos='https://cloud.r-project.org')"

# Default command
CMD ["Rscript", "-e", "print('Hello from R on Amazon Linux!')"]
