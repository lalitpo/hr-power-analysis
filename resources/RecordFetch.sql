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
FROM public."activity-data"
WHERE ACTIVITY_ID IN (SELECT unnest(INFO.activities_ids)
                      FROM "athlete-info" AS INFO
                      WHERE athlete_id = (athlete_id)
                        AND heartrate is not null
  AND watts is not null
  AND distance is not null
                        AND time is not null
                        AND EXTRACT(YEAR FROM activity_date) = (year)