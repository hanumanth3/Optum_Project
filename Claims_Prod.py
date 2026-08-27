# Databricks notebook source
# MAGIC %run "/Workspace/optum/Prod/connectors_prod"

# COMMAND ----------

# MAGIC %run "/Workspace/optum/Prod/Generic_Prod"

# COMMAND ----------

adls_connect()

# COMMAND ----------

claims_df = read_bronze_json("Claims")

# COMMAND ----------

claims_df = claims_df.drop("_id")

# COMMAND ----------

claims_df = claims_df.replace("NaN",None)
claims_df = claims_df.fillna({"Claim_Or_Rejected":"N"})

# COMMAND ----------

write2silver(claims_df,"Claims_S.csv")