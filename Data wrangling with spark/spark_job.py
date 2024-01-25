from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession

def start_spark():
    sc = SparkContext('local')
    spark = SparkSession(sc)
    print("Spark job starts")
    return spark


def process_passeger_data(spark, outputdata):
    path = '/Users/hengki.irawan/Documents/Coding practice/FN/etl-engineer/data/resource/passenger_data.csv'
    passenger_data = spark.read.csv(path, header=True)
    
    #create temp view
    passenger_data.createOrReplaceTempView("passenger_data")

    #recreate passenger_data
    print('creating new passenger data')
    new_passenger_data = spark.sql('''
            SELECT  id                                                                         AS id_passenger,
                    TO_TIMESTAMP(date_registered)                                              AS date_registered,
                    CAST(MONTHS_BETWEEN(current_timestamp, date_registered) AS INT)            AS diff_month_to_date,
                    UPPER(CASE WHEN country_code IS NULL THEN 'OTHER' ELSE country_code END)   AS country_code
              FROM  passenger_data
          ''')
    new_passenger_data.createOrReplaceTempView("new_passenger_data")
    new_passenger_data.write.mode("overwrite").csv("{}new passenger data".format(outputdata))


def getting_aggregated(spark, outputdata):
    path = '/Users/hengki.irawan/Documents/Coding practice/FN/etl-engineer/data/resource/booking_data.csv'
    booking_data = spark.read.csv(path, header=True)
    
    #create temp view
    booking_data.createOrReplaceTempView("booking_data")

    print('calculating total new users')
    total_new_customer = spark.sql('''
             SELECT  SUM(CASE WHEN diff_month_to_date < 4 THEN 1 ELSE 0 END) AS total_new_customer
               FROM  new_passenger_data
            ''')
    
#     total_new_customer.write.mode("overwrite").csv("{}total new customer".format(outputdata))
    total_new_customer.write.mode("overwrite").json("{}total new customer".format(outputdata))

    print('getting percentage booking in PL')
    percentage_booking_pl = spark.sql('''
            WITH step_1 AS (
                  SELECT  id  AS id_booking,
                          id_passenger,
                          country_code
                    FROM  booking_data
                    LEFT  JOIN new_passenger_data USING (id_passenger)
            )
            SELECT  ROUND(SUM(CASE WHEN country_code = 'PL' THEN 1 ELSE 0 END)/COUNT(1) * 100, 2) AS percentage_booked_pl
            FROM step_1
            ''')
    # percentage_booking_pl.write.mode("overwrite").csv("{}percentage booking pl".format(outputdata))
    percentage_booking_pl.write.mode("overwrite").json("{}percentage booking pl".format(outputdata))

    print('getting top three countries each year')
    top_booking_countries = spark.sql('''
            WITH registered AS (
                  SELECT  YEAR (date_registered) AS year, 
                          country_code           AS country_code,
                          COUNT(1)               AS total_registration
                    FROM  new_passenger_data
                   GROUP  BY 1,2
            ),
            sorted AS (
                  SELECT  *,
                          ROW_NUMBER() OVER (PARTITION BY year ORDER BY total_registration DESC) AS row_num
                    FROM registered
            )
            SELECT  year, 
                    country_code,
                    total_registration AS num,
                    total_registration-COALESCE(LEAD(total_registration) OVER (PARTITION BY year ORDER BY year), 0) AS diff 
              FROM  sorted 
             WHERE  row_num <= 3
             ORDER  BY 1, 3 DESC  
            ''')
#     top_booking_countries.write.mode("overwrite").csv("{}top booking countries".format(outputdata))
    top_booking_countries.write.mode("overwrite").json("{}top booking countries".format(outputdata))
    print('done')

def main():
    spark = start_spark()
    outputdata = '/Users/hengki.irawan/Documents/Coding practice/FN/etl-engineer/data/result/'
    process_passeger_data(spark, outputdata)    
    getting_aggregated(spark, outputdata)


if __name__ == "__main__":
    main()
    