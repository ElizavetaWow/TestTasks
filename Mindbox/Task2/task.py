from pyspark.sql import SparkSession
import pandas as pd

def get_products_with_categories(df_products, df_categories, df_rel):
    dt_result = df_rel.join(df_products, df_rel.product == df_products.id , 'fullouter').select(df_rel.category, df_products.name.alias('product_name'))\
    .join(df_categories, df_rel.category == df_categories.id , 'left').select('product_name', df_categories.name.alias('category_name'))
    return dt_result


spark = SparkSession.builder.getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

pandas_df = pd.DataFrame({'name': ['хлеб','булочка','батон','кекс','печенье','мука','пирожное','торт','молоко','кефир','сливки','говядина','курица','карась'],})
pandas_df['id'] = pandas_df.index+1
df_products = spark.createDataFrame(pandas_df)
pandas_df = pd.DataFrame({'name': ['хлебобулочные изделия','молочные изделия', 'мясо'],})
pandas_df['id'] = pandas_df.index+1
df_categories = spark.createDataFrame(pandas_df)
pandas_df = pd.DataFrame({'product': [2, 3, 4, 5, 7, 8, 9, 14, 3],'category':[1, 1, 1, 1, 1, 1, 2, 3, 2]})
df_rel = spark.createDataFrame(pandas_df)
get_products_with_categories(df_products, df_categories, df_rel).show()