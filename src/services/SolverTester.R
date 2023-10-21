hr0_ivp<-75
hrt_ivp<-55
K_ivp<-0.05
tau_ivp<-2
pseries_simulated <- numeric(3600)

t <- 0
p0 <- 100 + (30 * t / 180)

for (t in 1:3600) {
  pseries_simulated[t] <- 100 + (30 * floor(t / 180))
}

#plot(1:3600, pseries_simulated, type = "s", xlab = "Time (t)", ylab = "P", main = "Piecewise Constant Plot of Power")

hr_list_simulated <- numeric(length(3599))

hr_list_simulated[1] <- (hrt_ivp + K_ivp*p0) + (exp(-1 / tau_ivp)) * (hr0_ivp - hrt_ivp - K_ivp*p0)

for (i in seq(from =2, to = 3599, by =1)) {   #the lastpoint is 3600/hr0 makes up the entire hr simulated/ loop should be until 3599/array length
  hr_list_simulated[i] <- (hrt_ivp + K_ivp*pseries_simulated[i-1]) + (exp(-1 / tau_ivp)) * (hr_list_simulated[i-1] - hrt_ivp - K_ivp*pseries_simulated[i-1])
}
hr_list_all <- c(hr0_ivp, hr_list_simulated)




C_ <- -hr_list_all

hr_derivative_ivp_test  <- numeric(length(pseries_simulated))

for (i in seq(from = 1, to = 3600, by = 1)) {
    hr_derivative_ivp_test[i] <- (hrt_ivp + K_ivp*pseries_simulated[i]-hr_list_all[i])/tau_ivp
}
A_ivp <- cbind(hr_derivative_ivp_test, pseries_simulated, rep(1, length(hr_derivative_ivp_test)))
solution_ivp_test <- solve(t(A_ivp) %*% A_ivp) %*% t(A_ivp) %*% C_
ivp_results <- list(tau_lsm_ivp = solution_ivp_test[[1]], k_lsm_ivp = -solution_ivp_test[[2]], hreq_lsm_ivp = -solution_ivp_test[[3]])

hr_derivative_basic_test <- diff(hr_list_all)
A_basic <- cbind(hr_derivative_basic_test, pseries_simulated, rep(1, length(hr_derivative_basic_test)))
solution_basic_test <- solve(t(A_basic) %*% A_basic) %*% t(A_basic) %*% C_
basic_results <- list(tau_lsm_basic = solution_basic_test[[1]], k_lsm_basic = -solution_basic_test[[2]], hreq_lsm_basic = -solution_basic_test[[3]])

hr_derivative_savitzy_golay_1 <- calculate.glla(hr_list_all, 1:3600, 2, 1)$dsignal[, 2]
hr_derivative_savitzy_golay_1 <-hr_derivative_savitzy_golay_1[!is.na(hr_derivative_savitzy_golay_1)]
A_s_q1 <- cbind(hr_derivative_savitzy_golay_1, pseries_simulated, rep(1, length(hr_derivative_savitzy_golay_1)))
solution_sq1_test <- solve(t(A_s_q1) %*% A_s_q1) %*% t(A_s_q1) %*% C_
s_g1_results <- list(tau_lsm_sg = solution_sq1_test[[1]], k_lsm_sg = -solution_sq1_test[[2]], hreq_lsm_sg = -solution_sq1_test[[3]])

hr_derivative_savitzy_golay_2 <- savgol(hr_list_all, 3599, forder = 4, dorder = 1)
A_s_q2 <- cbind(hr_derivative_savitzy_golay_2, pseries_simulated, rep(1, length(hr_derivative_savitzy_golay_2)))
solution_sq2_test <- solve(t(A_s_q2) %*% A_s_q2) %*% t(A_s_q2) %*% C_
s_g2_results <- list(tau_lsm_sg = solution_sq2_test[[1]], k_lsm_sg = -solution_sq2_test[[2]], hreq_lsm_sg = -solution_sq2_test[[3]])

cat(paste(ivp_results, collapse = " "))
cat(paste(basic_results, collapse = " "))
cat(paste(s_g1_results, collapse = " "))
cat(paste(s_g2_results, collapse = " "))

HR_0 <- c(y=hr_list_all[1])
exp_hr_new <- numeric(length(pseries_simulated))
time_vector <- seq_along(pseries_simulated)
hr_eq_test <- ivp_results[["hreq_lsm_ivp"]]
k_test <- ivp_results[["k_lsm_ivp"]]
tau_test <- ivp_results[["tau_lsm_ivp"]]

ode_model_func <- function(pow) {
  hr_t <- (hr_eq_test + k_test*pow) + (exp(-1 / tau_test)) * (HR_0 - hr_eq_test - k_test*pow)
  return(hr_t)
}

for (i in seq(from = 1, to = 3600, by = 1)) {
  if (i == 1) {
    exp_hr_new[i] <- HR_0
  } else {
    result <- ode_model_func(pow = pseries_simulated[i])
    exp_hr_new[i] <- result
  }
}


rmse_test <- sqrt(mean((exp_hr_new - hr_list_all)^2))

indices <- seq_along(hr_list_all)


plot <- ggplot() +
  geom_line(data = data.frame(indices, hr_list_all), aes(x = indices, y = hr_list_all, colour = "Actual HeartRate (in bpm)")) +
  geom_line(data = data.frame(indices, pseries_simulated), aes(x = indices, y = pseries_simulated, colour = "Power (in watts)")) +
  geom_line(data = data.frame(indices, exp_hr_new), aes(x = indices, y = exp_hr_new, colour = "Predicted HeartRate (in bpm)")) +
  labs(x = "Time (in sec.)",
       y = "Signal (Magnitude)",
       colour = "") +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "bottom",
    legend.box = "horizontal"
  )
print(plot)

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
