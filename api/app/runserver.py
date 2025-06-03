FROM r405-base  # built from Dockerfile.base

# Install remotes to install specific package versions
RUN Rscript -e 'install.packages("remotes", repos="https://cloud.r-project.org")'

# Install R packages with version
RUN Rscript -e '
  pkgs <- c(
    "ggplot2@3.3.3",
    "dplyr@1.0.5",
    "tidyr@1.1.3"
  );
  install_version <- function(pv) {
    parts <- strsplit(pv, "@")[[1]];
    remotes::install_version(parts[1], version=parts[2], repos="https://cloud.r-project.org")
  };
  invisible(lapply(pkgs, install_version));
  '

# Copy your R scripts
COPY script1.R /opt/r-scripts/
COPY script2.R /opt/r-scripts/
COPY script3.R /opt/r-scripts/

# Run the main script
ENTRYPOINT ["bash", "-l", "-c"]
CMD ["Rscript /opt/r-scripts/script1.R"]
