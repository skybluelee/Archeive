# Spark 예시 코드
from pyspark.sql import SparkSession
from pyspark.sql.functions import floor
import logging

# SparkSession 초기화
spark = SparkSession.builder \
    .appName("Simple PySpark Example") \
    .config("spark.network.timeout", "600s") \
    .getOrCreate()

logging.info("start")    

# 예제 데이터 생성
data = [("Alice", 34), ("Bob", 45), ("Catherine", 29), ("David", 25), ("Emily", 34)]
columns = ["Name", "Age"]

# DataFrame 생성
df = spark.createDataFrame(data, columns)

# 연령대 계산
df_with_age_group = df.withColumn("AgeGroup", floor(df["Age"] / 10) * 10)

# 연령대별 사용자 수 계산
user_count_by_age_group = df_with_age_group.groupBy("AgeGroup").count().orderBy("AgeGroup")

# 결과 출력
user_count_by_age_group.show()

# SparkSession 종료
# spark.stop()
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import floor
# import logging

# # SparkSession 초기화
# with SparkSession.builder \
#     .appName("Simple PySpark Example") \
#     .getOrCreate() as spark:

#     logging.info("start")    

#     # 예제 데이터 생성
#     data = [("Alice", 34), ("Bob", 45), ("Catherine", 29), ("David", 25), ("Emily", 34)]
#     columns = ["Name", "Age"]

#     # DataFrame 생성
#     df = spark.createDataFrame(data, columns)

#     # 연령대 계산
#     df_with_age_group = df.withColumn("AgeGroup", floor(df["Age"] / 10) * 10)

#     # 연령대별 사용자 수 계산
#     user_count_by_age_group = df_with_age_group.groupBy("AgeGroup").count().orderBy("AgeGroup")

#     # 결과 출력
#     user_count_by_age_group.show()
