# Databricks notebook source
print("HEllo")

# COMMAND ----------

#dbutils.fs.mount(
#  source = "wasbs://blobstorage@casestudy2storageacc.blob.core.windows.net",
#  mount_point = "/mnt/casestudy2storageacc/alltimefinalsnow",
#  extra_configs = {"fs.azure.sas.blobstorage.casestudy2storageacc.blob.core.windows.net":"sp=racwdlmeop&st=2023-10-05T10:00:45Z&se=2023-10-05T18:00:45Z&spr=https&sv=2022-11-02&sr=c&sig=6%2FXNi%2B%2FXnLPmEpLB9kDDwbQhq0g8hNHYK74HUwji2yc%3D"})

# COMMAND ----------

# MAGIC %fs ls dbfs:/mnt/
# MAGIC

# COMMAND ----------

# MAGIC %fs ls dbfs:/mnt/casestudy2storageacc/

# COMMAND ----------

# MAGIC %fs ls dbfs:/mnt/casestudy2storageacc/alltimefinalsnow/
# MAGIC

# COMMAND ----------

# MAGIC %fs ls dbfs:/mnt/casestudy2storageacc/alltimefinalsnow/PARENT

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

df=spark.read.option("header",True).option("inferschema",True).csv("dbfs:/mnt/casestudy2storageacc/alltimefinalsnow/PARENT/RAW/CO2 Emissions_Canada.csv")

# COMMAND ----------

df.display()

# COMMAND ----------

df.select([count(when(
    isnan(col(each_col)) | \
    (col(each_col) == "") | \
    isnull(col(each_col)) | \
    (lower(col(each_col)) == "null"), 1 \
)).alias(f"{each_col} -> count") for each_col in df.columns]).display()

# COMMAND ----------

# Dropping Entire rows containing Null  
null_dropped_df=df.na.drop()
null_dropped_df.display()

# COMMAND ----------

#Dropping duplicate values
drop_dup_df=null_dropped_df.dropDuplicates(subset=None)
drop_dup_df.display()

# COMMAND ----------

drop_dup_df=drop_dup_df.withColumnRenamed("Vehicle Class","Vehicle_Class")
drop_dup_df=drop_dup_df.withColumnRenamed("Engine Size(L)","Engine_Size_L")
drop_dup_df=drop_dup_df.withColumnRenamed("Fuel Type","Fuel_Type")
drop_dup_df=drop_dup_df.withColumnRenamed("Fuel Consumption City (L/100 km)","Fuel_Consumption_City_L_100_km")
drop_dup_df=drop_dup_df.withColumnRenamed("Fuel Consumption Hwy (L/100 km)","Fuel_Consumption_Hwy_L_100_km")
drop_dup_df=drop_dup_df.withColumnRenamed("Fuel Consumption Comb (L/100 km)","Fuel_Consumption_Comb_L_100_km")
drop_dup_df=drop_dup_df.withColumnRenamed("Fuel Consumption Comb (mpg)","Fuel_Consumption_Comb_mpg")
drop_dup_df=drop_dup_df.withColumnRenamed("CO2 Emissions(g/km)","CO2_Emissions_g_km")

# COMMAND ----------

drop_dup_df.display()

# COMMAND ----------

#drop_dup_df.write.format("csv").option("header",True).mode("overwrite").option("path","dbfs:/mnt/casestudy2storageacc/alltimefinalsnow/PARENT/STAGING/").saveAsTable("finaldata")

# COMMAND ----------


