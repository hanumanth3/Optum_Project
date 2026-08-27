# Databricks notebook source
def adls_connect():
    spark.conf.set(
        "fs.azure.account.key.adlsoptum.dfs.core.windows.net",
        dbutils.secrets.get(scope="optumdbxscope", key="adlskey")
    )
    return "ADLS Connected"

# COMMAND ----------

def list_bronze_files():
    display(dbutils.fs.ls("abfss://optum@adlsoptum.dfs.core.windows.net/bronze/"))
    return "Bronze Files Listed"

# COMMAND ----------

def list_silver_files():
    display(dbutils.fs.ls("abfss://optum@adlsoptum.dfs.core.windows.net/silver/"))
    return "Silver Files Listed"

# COMMAND ----------

def list_gold_files():
    display(dbutils.fs.ls("abfss://optum@adlsoptum.dfs.core.windows.net/gold/"))
    return "Gold Files Listed"

# COMMAND ----------

def read_bronze_csv(file_name):
    data = spark.read.csv("abfss://optum@adlsoptum.dfs.core.windows.net/bronze/"+file_name+".csv",header=True,inferSchema=True)
    return data

# COMMAND ----------

def read_bronze_json(file_name):
    data = spark.read.json("abfss://optum@adlsoptum.dfs.core.windows.net/bronze/"+file_name+".json")
    return data

# COMMAND ----------

def read_silver_csv(file_name):
    data = spark.read.csv("abfss://optum@adlsoptum.dfs.core.windows.net/silver/"+file_name+".csv",header=True,inferSchema=True)
    return data

# COMMAND ----------

def read_gold_csv(file_name):
    data = spark.read.csv("abfss://optum@adlsoptum.dfs.core.windows.net/gold/"+file_name+".csv",header=True,inferSchema=True)
    return data

# COMMAND ----------

def write2database(df,tablename):
    Hostname = dbutils.secrets.get(scope="optumdbxscope",key="azuresqlserver")
    PortNum = dbutils.secrets.get(scope="optumdbxscope",key="azuresqlserverport")
    DatabaseName = dbutils.secrets.get(scope="optumdbxscope",key="dbname")
    DBProperties = {
    "user": dbutils.secrets.get(scope="optumdbxscope",key="dbuser"),
    "password": dbutils.secrets.get(scope="optumdbxscope",key="dbpassword")}
    urloftarget = "jdbc:sqlserver://{0}:{1};database={2}".format(Hostname,PortNum,DatabaseName)
    output = df.write.jdbc(url=urloftarget,table=tablename,mode="overwrite",properties=DBProperties)
    print("***************successfully written in azure sql database*******************")

# COMMAND ----------

def write2silver(df,file_name):
    silver_path = "abfss://optum@adlsoptum.dfs.core.windows.net/silver"
    #temp_path = f"{silver_path}/output_temp"
    temp_path = "abfss://optum@adlsoptum.dfs.core.windows.net/silver/output_temp"
    final_path = f"{silver_path}/{file_name}"
    df.write.mode("overwrite").option("header","true").csv(temp_path)
    files = dbutils.fs.ls(temp_path)
    csv_file = [file.path for file in files if file.path.endswith(".csv")][0]
    dbutils.fs.mv(csv_file,final_path)
    dbutils.fs.rm(temp_path,recurse=True)
    print("*******successfully written in silver layer**********")

# COMMAND ----------

def write2gold(df,file_name):
    gold_path = "abfss://optum@adlsoptum.dfs.core.windows.net/gold"
    #temp_path = f"{silver_path}/output_temp"
    temp_path = "abfss://optum@adlsoptum.dfs.core.windows.net/gold/output_temp"
    final_path = f"{gold_path}/{file_name}"
    df.write.mode("overwrite").option("header","true").csv(temp_path)
    files = dbutils.fs.ls(temp_path)
    csv_file = [file.path for file in files if file.path.endswith(".csv")][0]
    dbutils.fs.mv(csv_file,final_path)
    dbutils.fs.rm(temp_path,recurse=True)
    print("*******successfully written in Gold layer**********")