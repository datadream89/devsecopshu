FROM r-base:4.0.5

# Define custom writable R library path
ENV R_LIB_PATH=/opt/r/custom-lib

# Create the directory and make sure it's writable
RUN mkdir -p $R_LIB_PATH && chmod -R 777 $R_LIB_PATH

# Set this path as default for R
ENV R_LIBS_USER=$R_LIB_PATH

# Install unzip utility
RUN apt-get update && apt-get install -y unzip

# Copy your R package (.zip) into the container
COPY mypackage.zip /tmp/mypackage.zip

# Unzip the package
RUN unzip /tmp/mypackage.zip -d /tmp/mypackage

# Install to the custom lib path
RUN Rscript -e "install.packages('/tmp/mypackage', repos=NULL, type='source', lib=Sys.getenv('R_LIBS_USER'))"

# Optional: Ensure the lib path is active for R sessions
RUN echo "R_LIBS_USER=$R_LIB_PATH" >> /usr/local/lib/R/etc/Renviron
