import pytest
from pyspark.sql import SparkSession
from melt import melt


@pytest.fixture(scope='session')
def spark():
    return SparkSession.builder \
      .master("local") \
      .appName("test") \
      .enableHiveSupport() \
      .getOrCreate()

def test_melt_simple(spark):
    """Simple test function
    """
    data = [
        (1, "one", "123"),
        (2, "two", "456"),
    ]
    df = spark.createDataFrame(data, ["id", "name", "phone"])
    prepared_data = melt(df, id_vars=['id'], value_vars=["name", "phone"])
    assert ['id', 'attr_name', 'attr_value'] == prepared_data.columns
    assert 4 == prepared_data.count()

def test_melt_null(spark):
    """test data with null
    """
    data = [
        (1, "one", "123"),
        (2, "two", None),
    ]
    df = spark.createDataFrame(data, ["id", "name", "phone"])
    prepared_data = melt(df, id_vars=['id'], value_vars=["name", "phone"])
    assert ['id', 'attr_name', 'attr_value'] == prepared_data.columns
    assert 4 == prepared_data.count()
