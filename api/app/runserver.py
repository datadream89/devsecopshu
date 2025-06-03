FROM amazonlinux:2

RUN yum -y update && \
    yum -y install gcc gcc-c++ make wget tar gzip \
                   libcurl-devel openssl-devel libxml2-devel && \
    yum clean all

# Download and install R
RUN curl -O https://cran.r-project.org/src/base/R-4/R-4.0.5.tar.gz && \
    tar -xf R-4.0.5.tar.gz && \
    cd R-4.0.5 && ./configure --with-x=no --enable-R-shlib && \
    make -j4 && make install
