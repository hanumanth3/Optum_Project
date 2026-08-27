# Databricks notebook source
# MAGIC %run "/Workspace/optum/Prod/connectors_prod"

# COMMAND ----------

# MAGIC %run "/Workspace/optum/Prod/Generic_Prod"

# COMMAND ----------

adls_connect()

# COMMAND ----------

pat_df = read_bronze_csv("Patient_records")

# COMMAND ----------

pat_df = pat_df.fillna({"Patient_name":"Vistitor/NA"})

# COMMAND ----------

pat_df = pat_df.withColumn(
    "patient_phone",
    concat(
        substring(col("patient_phone"), 1, 6),
        lit("******"),
        substring(col("patient_phone"), -2,2)
    )
)

# COMMAND ----------

pat_df = pat_df.withColumn("patient_age",(months_between(current_date(), col("patient_birth_date")) / 12).cast("integer"))

# COMMAND ----------

pat_df = pat_df.drop("patient_birth_date")

# COMMAND ----------

write2silver(pat_df,"Patient_S.csv")