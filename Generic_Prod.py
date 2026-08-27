# Databricks notebook source
import pyspark
from pyspark.sql.functions import *

# COMMAND ----------

def rows_columns_count(df):
    return df.count(), len(df.columns)


# COMMAND ----------

def display_data(df):
    return display(df.limit(5))

# COMMAND ----------

def check_missing_values(df,lst_cl):
    missing_values = {}
    for i in lst_cl:
        a = df.filter(col(i).isNull()).count()
        missing_values[i] = a
    return missing_values


# COMMAND ----------

def check_missing_values_percent(df,lst_cl):   ## takes long time dont run
    missing_value_percent ={}
    b = df.count()
    for i in lst_cl:
        a = df.filter(col(i).isNull()).count()
        c = (a/b) * 100 
        missing_value_percent[i] = c
    return missing_value_percent

# COMMAND ----------

def check_missing_values_percent_v2(df,lst_cl):
    global missing_values_percent_more_than_75
    global missing_values_percent_less_than_75
    missing_values_percent_more_than_75 = {}
    missing_values_percent_less_than_75 = {}
    b = df.count()
    for i in lst_cl:
        a = df.filter(col(i).isNull()).count()
        c = (a/b) * 100
        if c >= 75:
            missing_values_percent_more_than_75[i] = c
        else:
            missing_values_percent_less_than_75[i] = c
    return({"missing_values_percent_more_than_75: ":missing_values_percent_more_than_75, \
             "missing_values_percent_less_than_75: ":missing_values_percent_less_than_75})

# COMMAND ----------

def drop_columns(df,lst_col):
    for i in lst_col:
        df = df.drop(i)
        print("Column dropped: ",i)
    return df

# COMMAND ----------

def check_duplicates(df,cl):
    a = df.select(cl).distinct().count()
    b = df.select(cl).count()
    if a == b:
        print("No duplicates: ")
    else:
        c = b - a
        print("There are",c,"duplicates")
    return

# COMMAND ----------

def check_string_as_Nan(df):
    results = {}
    for i in df.columns:
        results[i] = df.filter(col(i).like("%NaN%")).count()
    return results