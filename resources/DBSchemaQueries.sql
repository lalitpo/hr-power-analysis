CREATE TABLE IF NOT EXISTS public."athlete-info"(
athlete_id character varying COLLATE pg_catalog."default" NOT NULL,
athlete_name text COLLATE pg_catalog."default" NOT NULL,
location character varying COLLATE pg_catalog."default",
activities_ids bigint[] NOT NULL,
CONSTRAINT "athlete-info_pkey" PRIMARY KEY (athlete_id));

CREATE TABLE IF NOT EXISTS public."athletic-data"(
activity_id bigint NOT NULL,
activity_date DATE,
activity_distance numeric(10,2),
activity_duration TIME,
elevation integer,
distance numeric(10,2)[],
heartrate integer[],
watts integer[],
watts_calc integer[],
altitude numeric(6,2)[],
cadence integer[],
time integer[],
temp integer[],
CONSTRAINT "athletic-data_pkey" PRIMARY KEY (activity_id));