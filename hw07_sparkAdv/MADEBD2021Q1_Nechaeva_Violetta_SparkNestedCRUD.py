def update_df(df, columns_dict):
    """
    Updates existing columns or creates new in dataframe df using
    columns from columns_dict.

    :param df: input dataframe
        :type df: pyspark.sql.Dataframe
    :param columns_dict:
        Key-value dictionary of columns which need to be updated.
        Key is a column name in the format of path.to.col
        :type param: Dict[str, pyspark.sql.Column]
    :return: dataframe with updated columns
    :rtype pyspark.sql.DataFrame
    """
    result = df.select("*").columns
    while True:
        try:
            for col in set(result):
                result.append(col)
                new_col = col + ".*"
                new_columns = df.select(new_col).columns
                result += [col + "." + i for i in new_columns]
        except:
            break
    new_schema = set(result + list(columns_dict.keys()))
    col_to_idx = {}
    idx_to_col = {}
    for i, k in enumerate(new_schema):
        col_to_idx[k] = i
        idx_to_col[i] = k
    visited = [False for _, _ in col_to_idx.items()]

    return df
