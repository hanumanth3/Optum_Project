# Databricks notebook source
# MAGIC %run "/Workspace/optum/Prod/connectors_prod"

# COMMAND ----------

adls_connect()

# COMMAND ----------

pat_df = read_silver_csv("Patient_S")
hos_df = read_silver_csv("Hospital_S")
claims_df = read_silver_csv("Claims_S")
dis_df = read_silver_csv("Disease_S")
grp_df = read_silver_csv("group")
subgrp_df = read_silver_csv("SubGroup_S")
subscr_df = read_silver_csv("subscriber_S")

# COMMAND ----------

final_df = claims_df.join(pat_df,claims_df["patient_id"]==pat_df["Patient_id"],"left") \
                    .join(hos_df,pat_df["hospital_id"] == hos_df["Hospital_id"],"left") \
                    .join(subscr_df,claims_df["SUB_ID"]==subscr_df["sub_id"],"left") \
                    .join(dis_df,claims_df["disease_name"]==dis_df["disease_name"],"left")  \
                    .join(subgrp_df,subscr_df["Subgrp_id"]==subgrp_df["subgrp_sk"],"left") \
                    .join(grp_df,subgrp_df["subgrp_id"] == grp_df["grp_id"],"left")
         

# COMMAND ----------

final_df = claims_df.join(
    subscr_df,
    claims_df.SUB_ID == subscr_df.sub_id,
    "left"
).drop(subscr_df.sub_id)

# COMMAND ----------

from pyspark.sql.types import StringType, NumericType

string_columns = [
    field.name
    for field in final_df.schema.fields
    if isinstance(field.dataType, StringType)
]

numeric_columns = [
    field.name
    for field in final_df.schema.fields
    if isinstance(field.dataType, NumericType)
]
final_df = (
    final_df
    .fillna("N/A",subset=string_columns)
    .fillna(0,subset=numeric_columns)
)


# COMMAND ----------

write2gold(final_df,"Optum_G.csv")
write2database(final_df,"Optum_Tb")