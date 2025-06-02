# sample_script.R
library(ggplot2)
library(dplyr)

df <- data.frame(x = 1:10, y = (1:10)^2)
print("Sample dataframe:")
print(df)

ggplot(df, aes(x, y)) + geom_line() + ggtitle("Sample Plot")

cat("R 4.0.5 setup completed successfully!\n")
