# Databricks notebook source
# MAGIC %run "/Workspace/optum/Prod/connectors_prod"

# COMMAND ----------

# MAGIC %run "/Workspace/optum/Prod/Generic_Prod"

# COMMAND ----------

adls_connect()

# COMMAND ----------

subgrp_df = read_bronze_csv("subgroup")

# COMMAND ----------

subgrp_df = subgrp_df.withColumn("subgrp_id",split("subgrp_id",","))

# COMMAND ----------

subgrp_df = subgrp_df.withColumn("subgrp_id",explode(col("subgrp_id")))

# COMMAND ----------

write2silver(subgrp_df,"SubGroup_S.csv")