# Use your existing R 4.0.5 base image
FROM amazonlinux2-r405-script

# Install required R packages with pinned versions
RUN Rscript -e 'install.packages("remotes", repos="https://cloud.r-project.org")' && \
    Rscript -e ' \
      pkgs <- c( \
        "ggplot2@3.3.3", \
        "dplyr@1.0.5", \
        "tidyr@1.1.3" \
        # Add more like: "stringr@1.4.0", "readr@1.4.0", etc. \
      ); \
      install_version <- function(pv) { \
        parts <- strsplit(pv, "@")[[1]]; \
        remotes::install_version(parts[1], version = parts[2], repos = "https://cloud.r-project.org") \
      }; \
      invisible(lapply(pkgs, install_version))'
