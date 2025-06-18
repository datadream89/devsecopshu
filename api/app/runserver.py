FROM r-base:4.0.5

# Create a custom library path with proper ownership
ENV R_LIB_PATH=/opt/r/custom-lib

# Create the lib directory and give ownership to root (or to a safer user later)
RUN mkdir -p $R_LIB_PATH && chown root:staff $R_LIB_PATH

# Set R to use this custom path
ENV R_LIBS_USER=$R_LIB_PATH

# Install unzip utility
RUN apt-get update && apt-get install -y unzip

# Copy and unzip the R package
COPY mypackage.zip /tmp/mypackage.zip
RUN unzip /tmp/mypackage.zip -d /tmp/mypackage

# Check DESCRIPTION file exists to ensure it's a valid source package
RUN test -f /tmp/mypackage/DESCRIPTION

# Install it using base R tools (no devtools needed)
RUN Rscript -e "install.packages('/tmp/mypackage', lib=Sys.getenv('R_LIBS_USER'), repos=NULL, type='source')"

# Optional: persist lib path
RUN echo "R_LIBS_USER=$R_LIB_PATH" >> /usr/local/lib/R/etc/Renviron
