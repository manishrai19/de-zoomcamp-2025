#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    db =params.db
    url=params.url
    port = params.port
    table_name = params.table_name

    temp_parquet = 'output.parquet'
    csv_name = 'output.csv'
    #download the csv file
        

    os.system(f"wget -O {temp_parquet} {url}")

    data = pd.read_parquet(temp_parquet)
    data.to_csv(csv_name)

    os.system(f"rm {temp_parquet}")


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(csv_name, iterator = True,chunksize=100000)
    df = next(df_iter)
    df.tpep_pickup_datetime  = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime   = pd.to_datetime(df.tpep_dropoff_datetime )
    df.rename(columns={'Unnamed: 0': 'ID'}, inplace = True)
    df.head(n=0).to_sql(name = table_name,con=engine,if_exists='replace')


    while True:
        t_start=time()
        df=next(df_iter)
        df.tpep_pickup_datetime  = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime   = pd.to_datetime(df.tpep_dropoff_datetime )
        df.rename(columns={'Unnamed: 0': 'ID'}, inplace = True)
        df.to_sql(name=table_name,con=engine,if_exists='append')
        t_end=time()
        print(f'inserted another chunk, took {(t_end-t_start):.2f} seconds')

# df.to_sql(name=table_name,con=engine,if_exists='append')

if __name__=='__main__':
    
    parser = argparse.ArgumentParser(description='Ingest CSV to POSTGRES')
    # user , host , password , port, database name ,  table
    # url of the csv
    parser.add_argument('--user', help="username for postgres database")
    parser.add_argument('--password',help="password for the postgres database",)
    parser.add_argument('--host',help="host for the postgres database",)
    parser.add_argument('--db',help="database name for the postgres database",)
    parser.add_argument('--port',help="port for the postgres database",)
    parser.add_argument('--table_name',help="table name for the postgres database",)
    parser.add_argument('--url',help="URL for csv file")
    args = parser.parse_args()
    main(args)





#data = pd.read_parquet(r"/home/raim/de-zoomcamp-2025/yellow_tripdata_2024-01.parquet")





# len(data)




# df = pd.read_csv(r"/home/raim/de-zoomcamp-2025/yellow_tripdata_2024-01.csv", nrows=100)

# df.rename(columns={'Unnamed: 0': 'ID'}, inplace = True)







# print(pd.io.sql.get_schema(df, name ='yellow_taxi_data',con=engine))


# df=next(df_iter)

# len(df)







