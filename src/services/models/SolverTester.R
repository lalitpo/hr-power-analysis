hr0_ivp<-75
hrt_ivp<-55
K_ivp<-0.05
tau_ivp<-2
pseries_simulated <- numeric(3600)

t <- 0
p0 <- 100 + (30 * t / 180)

#power calculated/simulated at the start of every second for piece wise constant.
for (t in 1:3600) {
  pseries_simulated[t] <- 100 + (30 * floor(t / 180))
}

#plot(1:3600, pseries_simulated, type = "s", xlab = "Time (t)", ylab = "P", main = "Piecewise Constant Plot of Power")

hr_list_simulated <- numeric(length(3599))

hr_list_simulated[1] <- (hrt_ivp + K_ivp*p0) + (exp(-1 / tau_ivp)) * (hr0_ivp - hrt_ivp - K_ivp*p0)

#heart rate calculated at start of the time data point.
#calculating it for 3600 would mean hr from 3600 to 3601 time data point.
for (i in 2:3599) {   #the lastpoint is 3600/hr0 makes up the entire hr simulated/ loop should be until 3599/array length
  hr_list_simulated[i] <- (hrt_ivp + K_ivp*pseries_simulated[i-1]) + (exp(-1 / tau_ivp)) * (hr_list_simulated[i-1] - hrt_ivp - K_ivp*pseries_simulated[i-1])
}



hr_list_all <- c(hr0_ivp, hr_list_simulated)
C_ <- -hr_list_simulated

 hr_derivative_ivp_test  <- numeric(length(hr_list_simulated))

 for (i in 1:3599) {
     hr_derivative_ivp_test[i] <- (hrt_ivp + K_ivp*pseries_simulated[i]-hr_list_simulated[i])/tau_ivp
 }
 A_ivp <- cbind(hr_derivative_ivp_test, pseries_simulated[1:3599], rep(1, length(hr_derivative_ivp_test)))
 solution_ivp_test <- solve(t(A_ivp) %*% A_ivp) %*% t(A_ivp) %*% C_
 ivp_results <- list(
   tau_lsm_ivp = format(solution_ivp_test[[1]], nsmall = 15),
   k_lsm_ivp = format(-solution_ivp_test[[2]], nsmall = 15),
   hreq_lsm_ivp = format(-solution_ivp_test[[3]], nsmall = 15)
 )

#TODO : diff returns -1 length, but how matrix solving returned non-NA value of coefficients??
# Add hr0 in the list of values for differentiation, to get 3599 values
 hr_derivative_basic_test <- diff(hr_list_all)
 A_basic <- cbind(hr_derivative_basic_test, pseries_simulated[1:3599], rep(1, length(hr_derivative_basic_test)))
 solution_basic_test <- solve(t(A_basic) %*% A_basic) %*% t(A_basic) %*% C_
 basic_results <- list(
   tau_lsm_basic = solution_basic_test[[1]],
   k_lsm_basic = -solution_basic_test[[2]],
   hreq_lsm_basic = -solution_basic_test[[3]]
 )

#TODO : what was the length of derivative in calculate.glla too?
# ANS : 3599
# Add hr0 in the list of values for differentiation, to get 3599 values
 hr_derivative_glla <- calculate.glla(hr_list_all, 1:3600, 2, 1)$dsignal[, 2]
 hr_derivative_glla <- hr_derivative_glla[!is.na(hr_derivative_glla)]
 A_s_q1 <- cbind(hr_derivative_glla, pseries_simulated[1:3599], rep(1, length(hr_derivative_glla)))
 solution_sq1_test <- solve(t(A_s_q1) %*% A_s_q1) %*% t(A_s_q1) %*% C_
 s_g1_results <- list(
   tau_lsm_sg = solution_sq1_test[[1]],
   k_lsm_sg = -solution_sq1_test[[2]],
   hreq_lsm_sg = -solution_sq1_test[[3]]
 )

#TODO : what was the length of derivative in sg too?
# ANS : 3599
hr_derivative_savitzy_golay <-  numeric(length(hr_list_all))
 hr_derivative_savitzy_golay <- savgol(hr_list_all, 3599, forder = 2, dorder = 1)
 A_s_q2 <- cbind(hr_derivative_savitzy_golay, pseries_simulated[1:3600], rep(1, length(hr_derivative_savitzy_golay)))
 solution_sq2_test <- solve(t(A_s_q2) %*% A_s_q2) %*% t(A_s_q2) %*% -hr_list_all
 s_g2_results <- list(
   tau_lsm_sg = solution_sq2_test[[1]],
   k_lsm_sg = -solution_sq2_test[[2]],
   hreq_lsm_sg = -solution_sq2_test[[3]]
 )
cat(paste(s_g2_results, collapse = " "))

 cat(paste(ivp_results, collapse = " "))
 cat(paste(basic_results, collapse = " "))
 cat(paste(s_g1_results, collapse = " "))

#HR_0 <- c(y=hr_list_all[1])
#exp_hr_new <- numeric(length(pseries_simulated))
#time_vector <- seq_along(pseries_simulated)
options(digits=15)
est_hr <- numeric(3599)

tau_test <- as.double(s_g2_results$tau_lsm_sg)
k_test <- as.double(s_g2_results$k_lsm_sg)
hr_eq_test <- as.double(s_g2_results$hreq_lsm_sg)
hr0 <- hr0_ivp


predict_hr <- function(pow, t, hr) {
  hr_t <- (hr_eq_test + k_test*pow) + (exp(-t / tau_test)) * (hr - hr_eq_test - k_test*pow)
  return(hr_t)
}

est_hr[1]<- predict_hr(p0, 1, hr0_ivp)

for (i in 2:3599) {
  est_hr[i] <- predict_hr(pow = pseries_simulated[i-1], t = 1, hr = est_hr[i-1])
}

matrix <- cbind( hr_list_simulated, est_hr, pseries_simulated)
rmse_test <- sqrt(mean((est_hr - hr_list_simulated)^2))
print(rmse_test)


indices <- seq_along(hr_list_simulated)

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
  )+
  geom_text(aes(x = max(indices) * 0.7, y = max(hr_list_all) * 2.5, label = paste("RMSE = ", rmse_test)))

ggsave("../../../sav_gol.png", plot, dpi = 300, width = 12, height = 6)

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
