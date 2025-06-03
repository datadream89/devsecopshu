FROM amazonlinux:2

RUN yum -y update && \
    yum -y install gcc gcc-c++ make libcurl-devel openssl-devel libxml2-devel \
                   wget tar which unzip less && \
    yum clean all

# Install R 4.0.5 manually
RUN curl -O https://cran.r-project.org/src/base/R-4/R-4.0.5.tar.gz && \
    tar -xf R-4.0.5.tar.gz && \
    cd R-4.0.5 && ./configure --with-x=no --enable-R-shlib && make -j4 && make install

# Install R packages
RUN Rscript -e 'install.packages(c("ggplot2", "dplyr"), repos="https://cloud.r-project.org")'
