
import teradatasql
from pyspark.sql import SparkSession
from pyspark.sql.functions import length, max as spark_max
from datetime import datetime

# Teradata connection info
td_conn_params = {
    'host': '<TERADATA_HOST>',
    'user': '<USERNAME>',
    'password': '<PASSWORD>',
    'database': '<DATABASE>'
}
table_name = 'your_table'

# Step 1: Fetch Teradata metadata
query = f"""
SELECT ColumnName, ColumnType
FROM DBC.Columns
WHERE DatabaseName = '{td_conn_params['database'].upper()}'
  AND TableName = '{table_name.upper()}'
ORDER BY ColumnId;
"""

with teradatasql.connect(
    host=td_conn_params['host'],
    user=td_conn_params['user'],
    password=td_conn_params['password']
) as con:
    with con.cursor() as cur:
        cur.execute(query)
        columns_meta = cur.fetchall()

# Step 2: Spark session
spark = SparkSession.builder.appName("TD-Ingest").getOrCreate()

df_raw = spark.read \
    .format("jdbc") \
    .option("url", f"jdbc:teradata://{td_conn_params['host']}/DATABASE={td_conn_params['database']}") \
    .option("user", td_conn_params['user']) \
    .option("password", td_conn_params['password']) \
    .option("dbtable", table_name) \
    .load()

# Step 3: Infer dynamic types
cast_expressions = []

for col_name, td_type in columns_meta:
    td_type_clean = td_type.strip().upper()

    if td_type_clean in ['CF', 'CV']:  # Variable/Fixed character
        max_len = df_raw.select(spark_max(length(col_name))).collect()[0][0] or 1
        max_len = max(1, max_len)  # avoid VARCHAR(0)
        spark_type = f"VARCHAR({max_len})"

    elif td_type_clean == 'D':  # Decimal
        stats = df_raw.selectExpr(
            f"MAX(LENGTH(CAST(`{col_name}` AS STRING))) AS len",
            f"MAX(LENGTH(SPLIT(CAST(`{col_name}` AS STRING), '\\.')[0])) AS int_part",
            f"MAX(LENGTH(SPLIT(CAST(`{col_name}` AS STRING), '\\.')[1])) AS frac_part"
        ).collect()[0]
        p = (stats.int_part or 1) + (stats.frac_part or 0)
        s = stats.frac_part or 0
        spark_type = f"DECIMAL({p}, {s})"

    elif td_type_clean == 'I':
        spark_type = 'INT'
    elif td_type_clean == 'I1':
        spark_type = 'BYTE'
    elif td_type_clean == 'I2':
        spark_type = 'SMALLINT'
    elif td_type_clean == 'I8':
        spark_type = 'BIGINT'
    elif td_type_clean == 'DA':
        spark_type = 'DATE'
    elif td_type_clean == 'TS':
        spark_type = 'TIMESTAMP'
    else:
        print(f"Unknown type '{td_type_clean}' for column '{col_name}', defaulting to STRING")
        spark_type = 'STRING'

    cast_expressions.append(f"CAST(`{col_name}` AS {spark_type}) AS `{col_name}`")

# Step 4: Cast and write
df_casted = df_raw.selectExpr(*cast_expressions)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
df_casted.write.format("delta").mode("overwrite").save(f"/mnt/delta/{table_name}_{timestamp}")
