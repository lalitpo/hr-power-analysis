
test_data_small <- data.table(activity_8752058834_data[1:3600, ])

hr_derivative_values <- diff(test_data_small$heartrate)
#matrices
A <- cbind(hr_derivative_values, test_data_small$power, rep(1, length(hr_derivative_values)))
C <- -test_data_small$heartrate

 #################################
# Least Square Solver - Two different ways for Ax=C
 #1 : Use Linear Regression model formula
  # result_lm <- lm.fit(A, C)
 #result_lm$coefficients
 #################################
# use qr package because solve method only works for square matrices
 #qr.solve(A, C)
 #################################
#Least Square Solver -> https://cran.r-project.org/web/packages/Matrix/vignettes/Comparisons.pdf
solution <- solve(t(A) %*% A) %*% t(A) %*% C


tau <- solution[[1]]
k <- -solution[[2]]
hr_eq <- -solution[[3]]

estimated_hr <- A %*% solution
residuals <- C - estimated_hr
rmse <- sqrt(mean(residuals^2))

hr_tree <- rpart(test_data_small$heartrate ~ test_data_small$time,
              data=test_data_small)
power_tree <- rpart(test_data_small$power ~ test_data_small$time,
                    data=test_data_small)

# plot_tree <- function(tree, x, y, ylab) {
#   s <- seq(1, nrow(test_data_small), by=1)
#   plot(x, y, type = "n", xlab = "time", ylab = ylab)
#   lines(s, predict(tree, data.frame(x=s)))
# }
# plot_tree(hr_tree, test_data_small$time, test_data_small$heartrate, "heartrate")
# plot_tree(power_tree, test_data_small$time, test_data_small$power, "power")
#

# Create data frames for predictions
predictions_hr <- data.frame(time = test_data_small$time, heartrate = predict(hr_tree))
predictions_power <- data.frame(time = test_data_small$time, power = predict(power_tree))

# Create a blank plot
ggplot() +
  geom_blank(data = test_data_small, aes(x = time, y = heartrate)) +
  geom_blank(data = test_data_small, aes(x = time, y = power)) +
  labs(title = "Heart Rate and Power Over Time", x = "Time", y = "Values") +

  # Add lines for predictions
  geom_line(data = predictions_hr, aes(x = time, y = heartrate), color = "red", size = 1.25) +
  geom_line(data = predictions_power, aes(x = time, y = power), color = "blue", size = 1.25)



ode_params <- c(tau, k, hr_eq)
HR_0 <- c(y = test_data_small$heartrate[1])

ode_model_func <- function(t, state, parameters) {
  with(as.list(c(state, parameters)), {
    u <- predictions_power$power[t]
    dy_dt <- (-(1 / tau) * y + k / tau * u + hr_eq / tau)
    list(dy_dt)
  })
}

ode_output <- as.data.table(ode(y = HR_0,
                                times = test_data_small[, time],
                                func = ode_model_func,
                                parms = ode_params,
                                method = "euler"))
test_data_small[, `:=`(estimated_hr,  ode_output$y)]


plot3 <-ggplot2::ggplot( data = test_data_small) +
  ggplot2::geom_line(ggplot2::aes(time,predictions_hr$heartrate, colour = "Actual HeartRate ( in bpm)")) +
  ggplot2::geom_line(ggplot2::aes(time,estimated_hr, colour = "Predicted HeartRate ( in bpm)")) +
  ggplot2::labs(x = "Time (in sec.)",
                y = "Signal ( Magnitude )",
                colour = "") +
  ggplot2::theme(plot.title = ggplot2::element_text(hjust = 0.5, face = "bold"),
                 legend.position = "bottom", legend.box = "horizontal")
ggsave("../../Piecewise Predicted HR_HR_only.jpeg", plot3, dpi = 300, width = 8, height = 6)

complete_study_result <- list(data = test_data,
                              athlete_id = athlete_id,
                              estimated_results = estimated_results,
                              regression_results = lm_regression_result,
                              error = test_data$heartrate - test_data$estimated_hr)

estimated_results$R2 <- test_data[, 1 - sum((heartrate - estimated_hr) ^ 2, na.rm = T) / sum((heartrate - mean(heartrate, na.rm = T)) ^ 2, na.rm = T)]

#Can R2 be negative -> if numerator is greater than denominator

rmse <- sqrt(mean((complete_study_result$error)^2))
cat("R2 : ", estimated_results$R2)
cat(",       RMSE :", rmse)


plot3 <-ggplot2::ggplot( data = test_data_small) +
  ggplot2::geom_line(ggplot2::aes(time,heartrate, colour = "Actual HeartRate ( in bpm)")) +
  ggplot2::geom_line(ggplot2::aes(time,power, colour = "Power ( in watts)")) +
  ggplot2::geom_line(ggplot2::aes(time,estimated_hr, colour = "Predicted HeartRate ( in bpm)")) +
  ggplot2::labs(x = "Time (in sec.)",
                y = "Signal ( Magnitude )",
                colour = "") +
  ggplot2::theme(plot.title = ggplot2::element_text(hjust = 0.5, face = "bold"),
                 legend.position = "bottom", legend.box = "horizontal")
ggsave("../../Piecewise Predicted HR.jpeg", plot3, dpi = 300, width = 8, height = 6)


plot3 <- ggplot2::ggplot(data = test_data_small) +
  ggplot2::geom_point(ggplot2::aes(x = power, y = heartrate), color = "blue") +
  ggplot2::theme(
    plot.title = ggplot2::element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom",
    legend.box = "horizontal",
    panel.background = ggplot2::element_rect(fill = "white"),
    plot.background = ggplot2::element_rect(fill = "white")
  )

ggsave("../../Piecewise Predicted HR.jpeg", plot3, dpi = 300, width = 8, height = 6)


#hr over t
#p over t





step1 <- svd(A)
adiag <- diag(1/step1$d)
solution <- step1$v %*% adiag %*% t(step1$u) %*% C
solution

check <- A %*% solution
 #################################

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

