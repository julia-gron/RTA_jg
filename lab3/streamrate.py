## uruchom przez spark-submit streamrate.py

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("StreamingDemo").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = (spark.readStream
      .format("rate")
      .option("rowsPerSecond", 1)
      .load()
)
# nie ma transformacji 
# ukryta transformacja - df_transform = df lub df = 1* df

query = (df.writeStream 
    .format("console") 
    #.outputMode("append") - to jest automatycznie ustawione na append dlatego nie musimy pisać
    .option("truncate", False) 
    .start()
) 

query.awaitTermination() #jak piszemy skrypt w notatniku to musimy to dać na końcu
