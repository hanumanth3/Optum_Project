# Databricks notebook source
# MAGIC %run "/Workspace/optum/Prod/connectors_prod"

# COMMAND ----------

# MAGIC %run "/Workspace/optum/Prod/Generic_Prod"

# COMMAND ----------

adls_connect()

# COMMAND ----------

grp_df = read_bronze_csv("group")

# COMMAND ----------

# DBTITLE 1,mean
mean_value = grp_df.select(avg("premium_written")).first()[0]
grp_df = grp_df.fillna({"premium_written": mean_value})

# COMMAND ----------

# DBTITLE 1,Mode
mode_value = (
    grp_df.filter(col("city").isNotNull()).groupBy("city").count().orderBy(col("count").desc()).first()[0]
)

grp_df = grp_df.fillna({"city": mode_value})

# COMMAND ----------

write2silver(grp_df,"group.csv")