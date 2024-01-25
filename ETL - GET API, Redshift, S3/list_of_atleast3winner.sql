--Create a SQL query that will output all the teams that have won at least 3 times the Premier League since 2000-08-19.

SELECT team_name AS winner_name,
       COUNT(1)  AS total_win
  FROM seasons
  LEFT JOIN teams ON winner_id=team_id
 WHERE DATE_TRUNC('month', start_date::DATE) >= '2000-08-01'
 GROUP BY 1
HAVING COUNT(1)>=3