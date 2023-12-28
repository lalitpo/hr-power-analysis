SELECT activity_id,
       activity_date,
       activity_distance,
       activity_duration,
       elevation,
       distance,
       heartrate,
       watts,
       watts_calc,
       altitude,
       cadence,
       time,
       temp
FROM public."athletic-data"
WHERE heartrate is not null
  AND watts is not null
  AND distance is not null
  AND time is not null;
--SELECT activity_id, activity_date, activity_distance, activity_duration, "elevation_gain (in m)", distance, heartrate, "Power (in watts)", "Power_Calc(in watts)", "altitude (in m)", cadence, "time", temp FROM public."athletic-data" WHERE heartrate is not null AND "Power (in watts)" is not null;
