# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %run "/Workspace/optum/Prod/connectors_prod"

# COMMAND ----------

# MAGIC %run "/Workspace/optum/Prod/Generic_Prod"

# COMMAND ----------

adls_connect()

# COMMAND ----------

hos_df = read_bronze_csv("Hospital")

# COMMAND ----------

hos_df = hos_df.replace("NaN",None)   #correction

# COMMAND ----------

hos_df.show()
hos_df = hos_df.dropDuplicates()
hos_df = hos_df.drop("Unnamed: 0)

# COMMAND ----------

hos_df = hos_df.fillna({"State":"UT"})   #transformation
hos_df = hos_df.replace("New Delhi","Delhi")

# COMMAND ----------

write2silver(hos_df,"Hospital_S.csv")