library(doremi)
library(splines)

dermethod <- "glla"
derivative_method <- get(paste0("calculate.", dermethod))
sample_data <- setDT(copy(activity_8746996449_data[1:3600, ]))
sample_data[, `:=`(heartrate_rollmean, derivative_method(heartrate, time, 3, 1)$dsignal[, 1]), by = id]
sample_data[, `:=`(heartrate_derivate, derivative_method(heartrate, time, 3, 1)$dsignal[, 2]), by = id]
sample_data[, `:=`(time_derivate, derivative_method(heartrate, time, 3, 1)$dtime), by = id]

sample_data[, `:=`((paste0("power", "_rollmean")), lapply(.SD, function(x) {
      x[] <- derivative_method(x, time, 3)$dsignal[, 1]
      x
    })), .SDcols = "power", by = id]


bs_fit_model <-  lm(heartrate_derivate ~ heartrate_rollmean + power_rollmean, data = sample_data)

summary <- summary(bs_fit_model)
regression <- summary
summary(bs_fit_model)
resultmean <- data.table(id = "All",
                         gamma = -1 * summary$coefficients["heartrate_rollmean", "Estimate"],
                         gamma_stde = summary$coefficients["heartrate_rollmean", "Std. Error"],
                         yeqgamma = summary$coefficients["(Intercept)", "Estimate"],
                         yeqgamma_stde = summary$coefficients["(Intercept)", "Std. Error"])
resultmean[, `:=`(tau, 1 / gamma)]
resultmean[, `:=`(yeq, yeqgamma / gamma)]

resultid <- NULL
sample_data[, `:=`(totalexc, 0)]
sample_data[, `:=`(totalexcroll, 0)]


        resultmean[, `:=`(paste0("power", "_kgamma"), summary$coefficients[paste0("power", "_rollmean"), "Estimate"])]
        resultmean[, `:=`(paste0("power", "_kgamma_stde"), summary$coefficients[paste0("power", "_rollmean"), "Std. Error"])]
        resultmean[, `:=`(paste0("power", "_k"), get(paste0("power", "_kgamma")) * tau)]
        sample_data[, `:=`(totalexc,
                       totalexc + summary$coefficients[paste0("power", "_rollmean"), "Estimate"] * resultmean[, tau] * get("power"))]
        sample_data[, `:=`(totalexcroll,
                       totalexcroll + summary$coefficients[paste0("power", "_rollmean"), "Estimate"] * resultmean[, tau] * get(paste0("power", "_rollmean")))]


sample_data[, `:=`(heartrate_estimated, generate.1order(time = sample_data[, time],
                                                        excitation = sample_data[, power],
                                                        y0 = heartrate_rollmean[1],
                                                        t0 = sample_data[, time][1],
                                                        tau = resultmean[, tau],
                                                        k = resultmean[, power_k],
                                                        yeq = resultmean[, yeq])$y)]


if (!(is.na(resultmean[, tau]) | is.na(resultmean[, yeq]))) {
    resultmean$R2 <- sample_data[, 1 - sum((heartrate - heartrate_estimated) ^ 2, na.rm = T) / sum((heartrate - mean(heartrate, na.rm = T)) ^ 2, na.rm = T)]
  } else {
    resultmean$R2 <- nan
  }
  resultmean[R2 < 0, `:=`(R2, 0)]
  if (!is.null(resultid)) {
    resultid[, `:=`(id, NULL)]
   }
  res <- list(data = sample_data,
              resultid = resultid,
              resultmean = resultmean,
              regression = regression,
              dermethod = dermethod,
              derparam = 3,
              str_time = "time",
              str_exc = "power",
              str_signal = "heartrate",
              str_id = "id")

  class(res) <- "doremi"


ggplot2::ggplot( data = sample_data) +
  ggplot2::geom_line(ggplot2::aes(time,heartrate, colour = "Actual HeartRate ( in bpm)")) +
  ggplot2::geom_line(ggplot2::aes(time,power, colour = "Power ( in watts)")) +
  ggplot2::geom_line(ggplot2::aes(time,heartrate_estimated, colour = "Predicted HeartRate ( in bpm)")) +
  ggplot2::labs(x = "Time (in sec.)",
           y = "Signal ( Magnitude )",
           colour = "") +
  ggplot2::ggtitle("Heartrate Prediction with respect to Variation in Power") +
  ggplot2::theme(plot.title = ggplot2::element_text(hjust = 0.5, face = "bold"))

summary(res)

result_set <- data.frame(
  time = sample_data$time,
  power = sample_data$power,
  heartrate = sample_data$heartrate,
  heartrate_estimated = sample_data$heartrate_estimated,
  error = sample_data$heartrate - sample_data$heartrate_estimated
)
rmse <- sqrt(mean((result_set$error)^2))

print("RMSE : ", rmse)

