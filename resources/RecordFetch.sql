SELECT activity_id, activity_date, activity_distance, activity_duration, "elevation_gain (in m)", distance,\
\ heartrate, "Power (in watts)", "Power_Calc(in watts)", "altitude (in m)", cadence, "time", temp\
\ FROM public."athletic-data" WHERE heartrate is not null AND "Power (in watts)" is not null;