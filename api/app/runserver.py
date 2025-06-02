FROM amazonlinux2-r405-script

# Install R packages you need
RUN Rscript -e 'install.packages(c("ggplot2", "dplyr", "tidyr"), repos="https://cloud.r-project.org")'

# Copy your R scripts
COPY script1.R /opt/r-scripts/
COPY script2.R /opt/r-scripts/
COPY script3.R /opt/r-scripts/

# Run main script that sources others
ENTRYPOINT ["bash", "-l", "-c"]
CMD ["Rscript /opt/r-scripts/script1.R"]
