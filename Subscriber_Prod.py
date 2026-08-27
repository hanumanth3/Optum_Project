# Databricks notebook source
# MAGIC %run "/Workspace/optum/Prod/connectors_prod"

# COMMAND ----------

# MAGIC %run "/Workspace/optum/Prod/Generic_Prod"

# COMMAND ----------

adls_connect()

# COMMAND ----------

sub_df = read_bronze_csv("subscriber")

# COMMAND ----------

sub_df = sub_df.drop("Phone")
sub_df = sub_df.fillna({"first_name":"Vistitor/NA","Elig_ind":"N"})
sub_df = sub_df.withColumn("subsribers_age",(months_between(current_date(), col("Birth_date")) / 12).cast("integer"))
sub_df = sub_df.drop("Birth_date")

# COMMAND ----------

sub_df = sub_df.withColumn("Subgrp_id", when(
                                            (col("Subgrp_id").isNull()) & (col("sub_id")=="SUBID10022"),"S110")
                                        .when(
                                            (col("Subgrp_id").isNull()) & (col("sub_id")=="SUBID10049"),"S107"
                                            )
                                        .otherwise(col("Subgrp_id"))                                        )

# COMMAND ----------

write2silver(sub_df,"subscriber_S.csv")