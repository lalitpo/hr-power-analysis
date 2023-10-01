library(doremi)
library(splines)
library(deSolve)

test_data_small <- data.table(activity_8746996449_data[1:3600, ])

linearMod <- lm(test_data_small$heartrate ~ test_data_small$power, data=test_data_small)
summary(linearMod)

coefficients(linearMod)
n<- length(residuals(linearMod))
cor(residuals(linearMod)[-1], residuals(linearMod)[-n])
# library(ggplot2)  # Make sure you have the ggplot2 library loaded
#
# # Assuming 'heartrate' and 'power' are columns in 'test_data_small'
# # Create a scatter plot of these variables
# plot <- ggplot(data = test_data_small, aes(x = power, y = heartrate)) +
#   geom_point() +
#   labs(x = "Power", y = "Heart Rate") +
#   theme_bw()
#
# # Save the plot to a file
# ggsave("scatter_plot.png", plot, dpi = 300, width = 8, height = 6)

hr_derivative_values <- diff( test_data_small$heartrate)
A <- cbind(hr_derivative_values, test_data_small$power, rep(1, length(hr_derivative_values)))
C <- -test_data_small$heartrate

# Sample variable names
qr.solve(A, C)

asvd <- svd(A)
adiag <- diag(1/asvd$d)
adiag
solution <- asvd$v %*% adiag %*% t(asvd$u) %*% C
solution

check <- A %*% solution

linearMod1 <- lm(A ~ C)
summary(linearMod1)

coefficients(linearMod1)
# Initialize a list to store the solutions
solutions <- list()

# Loop through each variable and solve for it
for (variable_name in variable_names) {
  # Create a copy of matrix B with the current variable's coefficient
  B_copy <- matrix(0, nrow = length(variable_names), ncol = 1)
  B_copy[variable_name == variable_names, 1] <- 1

  # Solve the equation A * B + C = 0 for the current variable
  solution <- solve(A %*% B_copy + C)

  # Store the solution
  solutions[[variable_name]] <- solution
}

# Print the solutions for each variable
for (variable_name in variable_names) {
  cat(variable_name, ":", solutions[[variable_name]], "\n")
}

