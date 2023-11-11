library(doremi)
library(splines)
library(deSolve)

test_data <- data.table(activity_8746996449_data[1:3600, ])
athlete_id <- 8746996449
derivative_result <- calculate.glla(test_data$heartrate, test_data$time, 2, 1)

test_data[, c("heartrate_mov_avg", "heartrate_derivate") :=
              .(derivative_result$dsignal[, 1], derivative_result$dsignal[, 2]), by = id]
test_data[, `:=`(power_mov_avg, calculate.glla(test_data$power, time, 2, 1)$dsignal[, 1])]

bs_fit_model <-  lm(heartrate_derivate ~ heartrate_mov_avg + power_mov_avg, data = test_data)

summary(bs_fit_model)
coefficients(bs_fit_model)

lm_regression_result <- summary(bs_fit_model)
residuals <- residuals(bs_fit_model)
fitted <- fitted(bs_fit_model)

residual_data <- data.frame(fitted = fitted, residuals = residuals)

plot <- ggplot(residual_data, aes(x = fitted, y = residuals)) +
  geom_point() +
  geom_hline(yintercept = 0, color = "red", linetype = "dashed") +
  labs(x = "Fitted Values", y = "Residuals") +
  theme_bw()

ggsave("residuals_vs_fitted_plot.png", plot, dpi = 300, width = 8, height = 6)


par(mar = c(0.5, 0.5, 0.5, 0.5))
pdf("RegressionResults_Plot1.pdf", width = 16, height = 12)
plot(bs_fit_model)
dev.off()

estimated_results <- data.table(id = athlete_id,
                         hr_slope = -1 * lm_regression_result$coefficients["heartrate_mov_avg", "Estimate"],
                         intercept = lm_regression_result$coefficients["(Intercept)", "Estimate"])

estimated_results[, `:=`(tau, 1 / hr_slope)]
estimated_results[, `:=`(hr_eq, intercept / hr_slope)]
estimated_results[, `:=`(K_Gain, lm_regression_result$coefficients["power_mov_avg", "Estimate"] * tau)]

tau <- estimated_results[, tau]
k <- estimated_results[, K_Gain]
yeq <- estimated_results[, hr_eq]

ode_params <- c(tau, k, yeq)
HR_0 <- c(y = heartrate_8746996449[1])

ode_model_func <- function(t, state, parameters) {
  with(as.list(c(state, parameters)), {
    u <- test_data[, power][t]
    dy_dt <- (-(1 / tau) * y + k / tau * u + yeq / tau)
    list(dy_dt)
  })
}

ode_output <- as.data.table(ode(y = HR_0, times = test_data[, time], func = ode_model_func, parms = ode_params, method = "euler"))
test_data[, `:=`(estimated_hr,  ode_output$y)]

plot3 <-ggplot2::ggplot( data = test_data) +
  ggplot2::geom_line(ggplot2::aes(time,heartrate, colour = "Actual HeartRate ( in bpm)")) +
  ggplot2::geom_line(ggplot2::aes(time,power, colour = "Power ( in watts)")) +
  ggplot2::geom_line(ggplot2::aes(time,estimated_hr, colour = "Predicted HeartRate ( in bpm)")) +
  ggplot2::labs(x = "Time (in sec.)",
           y = "Signal ( Magnitude )",
           colour = "") +
  ggplot2::theme(plot.title = ggplot2::element_text(hjust = 0.5, face = "bold"),
                 legend.position = "bottom", legend.box = "horizontal")
ggsave("hrVspow2.png", plot3, dpi = 300, width = 8, height = 6)

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

