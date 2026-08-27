# Databricks notebook source
# MAGIC %run "/Workspace/optum/Prod/connectors_prod"

# COMMAND ----------

# MAGIC %run "/Workspace/optum/Prod/Generic_Prod"

# COMMAND ----------

adls_connect()

# COMMAND ----------

dis_df = read_bronze_csv("disease")

# COMMAND ----------

write2silver(dis_df,"Disease_S.csv")