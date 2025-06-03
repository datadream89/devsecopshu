RUN Rscript -e 'pkgs <- installed.packages(priority = c("base", "recommended")); cat("Installed base/recommended packages:\n"); print(pkgs[, "Package"])'
