activity_df <- read.csv("/Users/lalitpoddar/Desktop/Uni/MS Project Thesis/codebase/hr-power-analysis/src/services/activity_data.csv",
                        stringsAsFactors = FALSE)
#TODO: The data frame should be of type activity_info where element  at index 1 indicates all info about activity  1
#activity_info = {{activityid : 312313123. heartrate : 123131312312331313, power: 123123123}, {activityid : 312313123. heartrate : 123131312312331313, power: 123123123}}


# Convert list columns to integer lists
for (col in colnames(activity_df)) {
  if (startsWith(col, "heartrate")) {
    activity_df[[col]] <- lapply(activity_df[[col]], function(x) {
      values <- strsplit(x, ",")[[1]]
      values <- values[values != ""]  # Remove empty strings
      values <- suppressWarnings(as.integer(values))
      values[!is.na(values)]
    })
  }

  if (startsWith(col, "power")) {
    activity_df[[col]] <- lapply(activity_df[[col]], function(x) {
      values <- strsplit(x, ",")[[1]]
      values <- values[values != ""]  # Remove empty strings
      values <- suppressWarnings(as.integer(values))
      values[!is.na(values)]
    })
  }
}

activity_8752058834_data <- data.frame(power = unlist(activity_df[activity_df$activity_id == 8752058834, ]$power),
heartrate = unlist(activity_df[activity_df$activity_id == 8752058834, ]$heartrate))
activity_8752058834_data$id <- 2
activity_8752058834_data$time <- seq(from = 1, to = length(activity_8752058834_data$power))

activity_8746996449 <- activity_df[activity_df$activity_id == 8746996449, ]

# Create a new dataframe with values as columns
activity_8746996449_data <- data.frame(power = unlist(activity_df[activity_df$activity_id == 8746996449, ] $power),
                                       heartrate = unlist(activity_df[activity_df$activity_id == 8746996449, ] $heartrate))

activity_8746996449_data$id <- 1
activity_8746996449_data$time <- seq(from = 1, to = length(activity_8746996449_data$power))


#--------------------------#

# Create a new dataframe with values as columns


#--------------------------#
#--------------------------#
activity_8758003008 <- activity_df[activity_df$activity_id == 8758003008, ]
# Convert lists to vectors
power_8758003008 <- unlist(activity_8758003008$power)
heartrate_8758003008 <- unlist(activity_8758003008$heartrate)

# Create a new dataframe with values as columns
activity_8758003008_data <- data.frame(power = power_8758003008, heartrate = heartrate_8758003008)

time_8758003008 <- seq(from = 1, to = length(activity_8758003008_data$power))
activity_8758003008_data$id <- 3
activity_8758003008_data$time <- time_8758003008

#--------------------------#
#--------------------------#
activity_8763450311 <- activity_df[activity_df$activity_id == 8763450311, ]
# Convert lists to vectors
power_8763450311 <- unlist(activity_8763450311$power)
heartrate_8763450311 <- unlist(activity_8763450311$heartrate)

# Create a new dataframe with values as columns
activity_8763450311_data <- data.frame(power = power_8763450311, heartrate = heartrate_8763450311)

time_8763450311 <- seq(from = 1, to = length(activity_8763450311_data$power))
activity_8763450311_data$id <- 4
activity_8763450311_data$time <- time_8763450311



activity_data_all_4 <- rbind(activity_8746996449_data,
                             activity_8763450311_data,
                             activity_8752058834_data,
                             activity_8758003008_data)