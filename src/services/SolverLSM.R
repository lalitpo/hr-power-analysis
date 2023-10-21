test_data_small <- data.table(activity_8752058834_data[1:3600, ])

hr_derivative_diff_lsm <- diff(test_data_small$heartrate)
#matrices
A <- cbind(hr_derivative_diff_lsm, test_data_small$power, rep(1, length(hr_derivative_diff_lsm)))
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

#residual_square_lsq <- sqrt(mean((C - estimated_hr)^2))


piecewise_pow_data <- rep(test_data_small$power, each = 1)

plot(seq(1, 10, by = 1), piecewise_pow_data[1:10], type = 's',
     xlab = 'Time (seconds)', ylab = 'Value', main = 'Piecewise Constant Representation of Power')


ode_params <- c(tau, k, hr_eq)
HR_0 <- c(y = test_data_small$heartrate[1])
exp_hr <- numeric(length(test_data_small$time))


ode_model_func <- function(pow, t) {
    hr_t <- (hr_eq + k*pow) + (exp(-t / tau)) * (HR_0 - hr_eq - k*pow)
    return(hr_t)
}

for (i in seq_along(test_data_small$time)) {
  if (i == 1) {
    exp_hr[i] <- HR_0
   } else {
    exp_hr[i] <- ode_model_func(pow = test_data_small$power[i], t = i)
   }
}


rmse_lsm <- sqrt(mean((exp_hr - test_data_small$heartrate)^2))



