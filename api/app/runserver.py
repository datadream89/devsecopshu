FROM r-base:4.0.5

# Define library path
ENV R_LIBS_USER=/usr/local/lib/R/site-library

# Create library directory
RUN mkdir -p $R_LIBS_USER

# Install unzip utility
RUN apt-get update && apt-get install -y unzip

# Copy your .zip R package into container
COPY mypackage.zip /tmp/mypackage.zip

# Unzip it
RUN unzip /tmp/mypackage.zip -d /tmp/mypackage

# Install the package from unzipped folder
RUN Rscript -e "install.packages('/tmp/mypackage', repos = NULL, type = 'source', lib = Sys.getenv('R_LIBS_USER'))"

# Optional: Add library path permanently (for R sessions)
RUN echo 'R_LIBS_USER=/usr/local/lib/R/site-library' >> /usr/local/lib/R/etc/Renviron
