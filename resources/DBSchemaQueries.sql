CREATE TABLE IF NOT EXISTS public."athlete-info"(
                                                    athlete_id   bigint NOT NULL,
                                                    athlete_name text   NOT NULL,
                                                    location     text COLLATE pg_catalog."default",
activities_ids bigint[] NOT NULL,
CONSTRAINT "athlete-info_pkey" PRIMARY KEY (athlete_id));

CREATE TABLE IF NOT EXISTS public."activity-data"
(
activity_id bigint NOT NULL,
activity_date DATE,
activity_distance numeric(10,2),
activity_duration TIME,
average_power          integer,
max_power              integer,
weighted_average_power integer,
average_speed          numeric(3, 1),
max_speed              numeric(3, 1),
average_heart_rate     integer,
max_heart_rate         integer,
average_cadence        integer,
max_cadence            integer,
elevation integer,
distance numeric(10,2)[],
heartrate integer[],
watts integer[],
watts_calc integer[],
altitude numeric(6,2)[],
cadence integer[],
time integer[],
temp integer[],
CONSTRAINT "activity-data_pkey" PRIMARY KEY (activity_id)
);