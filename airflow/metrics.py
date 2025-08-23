import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/gcp-creds.json"

def get_metrics(data_csv_path):
    import pandas as pd
    from scipy.stats import zscore
    from IPython.display import display
    df2 = pd.read_csv(
        data_csv_path,
        storage_options={"token": os.environ["GOOGLE_APPLICATION_CREDENTIALS"]}
    )
    # fill_rates =df2.notna().mean()
    # total_fill_rate = 0
    # for col,values in fill_rates.items():
    #     total_fill_rate += values
    # avg = total_fill_rate / 4
    # print(f"{avg * 100:.2f}%")
    totalcells =df2.size
    non_null_cells = df2.count().sum()
    total_fill_rate = (non_null_cells/totalcells) * 100
    fillrate = f"{total_fill_rate:.2f}"

    row_count = df2.shape[0]

    df2.columns = df2.columns.str.strip()  
    numeric_cols = df2.select_dtypes(include=['number']).columns
    newdf = pd.DataFrame()
    for col in numeric_cols:
        newdf[f'Zscore{col}']=zscore(df2[col])
    newdf[[f'Zscore{col}' for col in numeric_cols]].abs()
    newdf = newdf>3
    df2['isoutlier'] = newdf.any(axis=1)
    outlier_rows = df2[df2['isoutlier']]
    outlier = f"{df2['isoutlier'].mean() * 100:.2f}"

    # import pandas as pd
    # df = pd.read_csv(timeliness_csv_path)
    # df['expected_time']= pd.to_datetime(df['expected_time'])
    # df['actual_time'] = pd.to_datetime(df['actual_time'])
    # df['delay']= (df['actual_time'] - df['expected_time']).dt.total_seconds()/60
    # for x in df.index:
    #     if df.loc[x,'delay'] <= 0:
    #         df.loc[x,'ontime'] = True
    #     else:
    #         df.loc[x,'ontime'] = False
    # ontime_percentage = float(df['ontime'].mean() *100)
    result = {'fillrate':fillrate , 'row_count':row_count , 'outlier':outlier}
    return result
