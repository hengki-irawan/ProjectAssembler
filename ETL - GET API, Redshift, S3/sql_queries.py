import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('/Users/hengki.irawan/Documents/Coding practice/CH/config.cfg')

# DROP TABLES
staging_table_drop = "DROP TABlE IF EXISTS staging_table CASCADE;"
seasons_drop       = "DROP TABLE IF EXISTS seasons       CASCADE;"
teams_drop         = "DROP TABLE IF EXISTS teams         CASCADE;"

# CREATE TABLES
staging_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_table(
    match_id          VARCHAR,
    start_date        VARCHAR,
    end_date          VARCHAR,
    current_match     VARCHAR,
    winner            VARCHAR
);
""")

seasons_create = ("""
CREATE TABLE IF NOT EXISTS seasons(
    match_id          VARCHAR,
    start_date        VARCHAR,
    end_date          VARCHAR,
    winner_id         VARCHAR
)
DISTSTYLE KEY
DISTKEY (match_id)
SORTKEY (match_id);
""")

teams_create = ("""
CREATE TABLE IF NOT EXISTS teams(
    team_id      VARCHAR,
    team_name    VARCHAR
)
DISTSTYLE KEY
DISTKEY (team_id)
SORTKEY (team_id);
""")

# STAGING TABLES
staging_table = ("""
    TRUNCATE TABLE staging_table;
    COPY staging_table 
    FROM {}
    CREDENTIALS 'aws_iam_role={}'
    CSV 
    DELIMITER ','
    IGNOREHEADER 1
    REGION 'eu-west-1';
""").format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE','ARN'))


# FINAL TABLES
seasons_insert = ("""
INSERT  INTO seasons (match_id, start_date, end_date, winner_id)
SELECT  stg.match_id,
        stg.start_date,
        stg.end_date,
        REGEXP_SUBSTR(winner, ' [^,]*') AS winner_id
  FROM  staging_table stg
 WHERE  winner IS NOT NULL;
""")

teams_insert = ("""
INSERT  INTO teams
SELECT  NULLIF(REGEXP_SUBSTR(winner, ' [^,]*'),'')                                        AS team_id,
        REPLACE(SPLIT_PART(REGEXP_SUBSTR(winner, ', [^,]+'), ': ',2), chr(39),'')         AS team_name
  FROM  staging_table
 WHERE  winner_id IS NOT NULL
 GROUP  BY 1,2;
""")


# QUERY LISTS
drop_table_queries = [staging_table_drop, seasons_drop, teams_drop]
create_table_queries = [staging_table_create, seasons_create, teams_create]
copy_table_queries = [staging_table]
insert_table_queries = [seasons_insert, teams_insert]
