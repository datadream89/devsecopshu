# Print locale and session info
print(Sys.getlocale())
print(sessionInfo())

# Load required libraries
library(ggplot2)
library(dplyr)

# Create a simple data frame
df <- data.frame(
  category = c("A", "B", "C"),
  value = c(23, 17, 35)
)

# Transform the data
df <- df %>%
  mutate(percent = value / sum(value) * 100)

print(df)

# Create a simple bar plot
plot <- ggplot(df, aes(x = category, y = value, fill = category)) +
  geom_bar(stat = "identity") +
  labs(title = "Sample Bar Plot", y = "Value") +
  theme_minimal()

# Save the plot
ggsave("/opt/r-scripts/sample_plot.png", plot)

# Done
cat("Sample script completed successfully.\n")
