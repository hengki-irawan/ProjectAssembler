WITH data AS (
    SELECT DATE_PART('year', start_date::date) AS start_date,
           DATE_PART('year', end_date::date)   AS end_date,
           team_name
      FROM seasons
      LEFT JOIN teams ON winner_id = team_id
     WHERE team_name IS NOT NULL
),
step1 AS (
    SELECT  t1.team_name,
            t3.start_date sn_b,
            t1.start_date,
            t2.start_date sn_t,
            t1.end_date,
            CASE
                WHEN t3.start_date IS NULL AND t2.start_date IS NULL THEN 'not_consecutive'
                WHEN t3.start_date IS NULL THEN 'start'
                WHEN t2.start_date IS NULL THEN 'end'
            END                                                                        AS marker
      FROM  data t1
      LEFT  JOIN data t2 ON t1.start_date = t2.start_date-1 AND t1.team_name = t2.team_name
      LEFT  JOIN data t3 ON t1.start_date = t3.start_date+1 AND t1.team_name = t3.team_name
),
step2 AS (
    SELECT  team_name,
            start_date,
            end_date,
            marker,
            LEAD(start_date) OVER (PARTITION BY team_name ORDER BY start_date ASC) lead_s
      FROM  step1
     WHERE  marker IS NOT NULL
)
SELECT  start_date                                                       AS start_year,
        CASE WHEN marker = 'start' THEN lead_s + 1 ELSE end_date END     AS end_year,
        team_name
  FROM  step2
 WHERE  marker = 'start' OR marker = 'not_consecutive'
 ORDER  BY 1,2;