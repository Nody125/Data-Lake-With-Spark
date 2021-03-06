import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from sql_query import Select_Songs_Table, Select_Artists_Table, staging_events_query, Load_users_data, dateandtime_query, filteredsongplays_query

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    creating a session with Spark
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    reading the songs files from S3 and processing them with Spark
    
    Args:
        spark (:obj:`SparkSession`): Spark session. 
        input_data (:obj:`str`): Directory where JSON files stored in it.
        output_data (:obj:`str`): Directory where parquet files stored in it.
    """
    # get filepath to song data file
    song_data = input_data + "song_data/*/*/*"
    
    # read song data fileS
    df = spark.read.json(song_data)
    df.createOrReplaceTempView("songs")
    
    # extract columns to create songs table
    songs_table = spark.sql(Select_Songs_Table).dropDuplicates(['song_id','title'])
	
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist_id").parquet(path = output_data + "/songs/songs.parquet", mode = "overwrite")

    # extract columns to create artists table
    artists_table = spark.sql(Select_Artists_Table).dropDuplicates(['artist_id','artist_name'])
    # write artists table to parquet files
    artists_table.write.parquet(path = output_data + "/artists/artists.parquet", mode = "overwrite")


def process_log_data(spark, input_data, output_data):
    """
    reading the logs files from S3 and processing them with Spark
    Args:
        spark (:obj:`SparkSession`): Spark session. 
        input_data (:obj:`str`): Directory where input files stored in it.
        output_data (:obj:`str`): Directory where parquet files stored .
    """
    # get filepath to log data file
    log_data = input_data + "log_data/*"
    
    # read log data file
    df = spark.read.json(log_data)
    
    df.createOrReplaceTempView("staging_events")
    # filter by actions for song plays
    df = spark.sql(staging_events_query)
    
    df.createOrReplaceTempView("staging_events")
    # extract columns for users table
    users_table = spark.sql(Load_users_data).dropDuplicates(['userId', 'level'])
    # write users table to parquet files
    users_table.write.parquet(path = output_data + "/users/users.parquet", mode = "overwrite")
    
    # extract columns to create time table
    time_table = spark.sql(dateandtime_query)
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet(path = output_data + "/time/time.parquet", mode = "overwrite")
    
    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data + "/songs/songs.parquet")
    song_df.createOrReplaceTempView("songs")
    
    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql(filteredsongplays_query).dropDuplicates('songplay_id')
    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet(path = output_data + "/songplays/songplays.parquet", mode = "overwrite")


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()