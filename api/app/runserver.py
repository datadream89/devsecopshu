FROM amazonlinux:2

# Set environment variables
ENV R_VERSION=4.0.5
ENV CURL_VERSION=7.88.1
ENV PATH=/opt/curl/bin:$PATH
ENV LD_LIBRARY_PATH=/opt/curl/lib:$LD_LIBRARY_PATH
ENV PKG_CONFIG_PATH=/opt/curl/lib/pkgconfig:$PKG_CONFIG_PATH

# Install base dependencies
RUN yum -y update && \
    yum install -y \
    gcc gcc-c++ gcc-gfortran \
    make wget tar gzip bzip2 \
    readline-devel zlib-devel \
    xz-devel pcre2 pcre2-devel \
    libcurl-devel openssl-devel libxml2-devel \
    which && \
    yum clean all

# Install newer libcurl
RUN cd /usr/local/src && \
    curl -LO https://curl.se/download/curl-${CURL_VERSION}.tar.gz && \
    tar -xzf curl-${CURL_VERSION}.tar.gz && \
    cd curl-${CURL_VERSION} && \
    ./configure --prefix=/opt/curl --with-ssl && \
    make -j$(nproc) && make install

# Download and install R 4.0.5 using the newer libcurl
RUN cd /usr/local/src && \
    curl -LO https://cran.r-project.org/src/base/R-4/R-${R_VERSION}.tar.gz && \
    tar -xzf R-${R_VERSION}.tar.gz && \
    cd R-${R_VERSION} && \
    ./configure --enable-R-shlib --with-libcurl=/opt/curl --with-x=no && \
    make -j$(nproc) && make install

# Install R packages (specific versions)
RUN Rscript -e 'install.packages(c("ggplot2", "dplyr", "tidyr"), repos="https://cloud.r-project.org")'

# Create script directory and copy R scripts
RUN mkdir -p /opt/r-scripts
COPY script1.R /opt/r-scripts/
COPY script2.R /opt/r-scripts/
COPY script3.R /opt/r-scripts/

# Set default working directory
WORKDIR /opt/r-scripts

# Run script1.R (which can source others)
ENTRYPOINT ["bash", "-l", "-c"]
CMD ["Rscript /opt/r-scripts/script1.R"]
