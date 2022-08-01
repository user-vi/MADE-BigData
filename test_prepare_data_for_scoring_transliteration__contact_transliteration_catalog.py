"""
Run in terminal
```
clear && \
pytest -v --maxfail=1 --disable-pytest-warnings \
./contact/tests/test_prepare_data_for_scoring_transliteration__contact_transliteration_catalog.py
```
"""

import pytest
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark_test import assert_pyspark_df_equal
from contact.transliteration.prepare_data_for_scoring_transliteration import ParquetCreator


extra_schema = StructType(
    [
        StructField('doc_id', LongType(), True),
        StructField('field_id', LongType(), True),
        StructField('line_text', StringType(), True),
        StructField('in_out', StringType(), True),
        StructField('is_actual', IntegerType(), True),
        StructField('year_month', LongType(), True)
    ]
)

@pytest.fixture(scope='session')
def spark():
    return SparkSession.builder \
        .config("spark.local.ip", "192.168.0.5") \
        .master("local") \
        .appName("tests") \
        .enableHiveSupport() \
        .getOrCreate()


@pytest.fixture(scope='session')
def full_path(tmpdir_factory):
    """
    Creare full_path as in ParquetCreator
    """
    temp_dir = tmpdir_factory.mktemp('tmp')
    full_path = str(temp_dir) + '/'
    return full_path


def write_parquet(spark, data_list, data_schema, path):
    df = spark.createDataFrame(data_list, data_schema)
    df.write.mode("overwrite").parquet(path)


def test_contact_transliteration_catalog_simple(spark, full_path):
    extra_list = [
        (1, 1, '20200101', "I", 1, 202001),
        (1, 101, 'Кирилл', "I", 1, 202001),
        (1, 101, 'Kirill', "O", 1, 202001),
    ]
    extra = spark.createDataFrame(extra_list, extra_schema)
    extra.write.mode("overwrite").parquet(full_path + 'pp_rts_doc_text')

    ParquetCreator.contact_transliteration_catalog(
        spark, full_path, path_to_rts_doc_text=full_path + 'pp_rts_doc_text', threshold=0
    )
    actual = spark.read.parquet(full_path + 'transliteration_catalog') \
        .select('attr_name', 'ru_names', 'en_names')

    expected_list = [(101, 'кирилл', 'kirill')]
    expected_schema = StructType(
        [
            StructField('attr_name', LongType(), True),
            StructField('ru_names', StringType(), True),
            StructField('en_names', StringType(), True),
        ]
    )
    expected = spark.createDataFrame(expected_list, expected_schema)

    expected.show()
    actual.show()

    assert_pyspark_df_equal(expected, actual)


def test_contact_transliteration_catalog_double(spark, full_path):
    extra_list = [
        (1, 1, '20200101', "I", 1, 202001),
        (1, 101, 'Кирилл', "I", 1, 202001),
        (1, 101, 'Kirill', "O", 1, 202001),
        (2, 1, '20200102', "I", 1, 202001),
        (2, 101, 'Кирилл', "I", 1, 202001),
        (2, 101, 'Kirill', "O", 1, 202001),
    ]
    extra = spark.createDataFrame(extra_list, extra_schema)
    extra.write.mode("overwrite").parquet(full_path + 'pp_rts_doc_text')

    ParquetCreator.contact_transliteration_catalog(
        spark, full_path, path_to_rts_doc_text=full_path + 'pp_rts_doc_text', threshold=0
    )
    actual = spark.read.parquet(full_path + 'transliteration_catalog') \
        .select('attr_name', 'ru_names', 'en_names')

    expected_list = [(101, 'кирилл', 'kirill')]
    expected_schema = StructType(
        [
            StructField('attr_name', LongType(), True),
            StructField('ru_names', StringType(), True),
            StructField('en_names', StringType(), True),
        ]
    )
    expected = spark.createDataFrame(expected_list, expected_schema)

    expected.show()
    actual.show()

    assert_pyspark_df_equal(expected, actual)
