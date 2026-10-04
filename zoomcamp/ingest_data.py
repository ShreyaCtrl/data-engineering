import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

# Read a sample of the data
# prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
# df = pd.read_csv(
#     prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz', 
#     dtype=dtype,
#     parse_dates=parse_dates
# )

# df.head()
# len(df)

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-database', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='trip_data', help='Target table name')
def ingest_data(pg_user, pg_password, pg_host, pg_port, pg_database, target_table):
    # pg_user = 'root'
    # pg_password = 'root'
    # pg_host = 'localhost'
    # pg_port = 5432
    # pg_database = 'ny_taxi'
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    year = 2021
    month = 1
    chunksize = 100000

    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')
    
    df_iter = pd.read_csv(
        prefix + f'yellow_tripdata_{year}-{month:02d}.csv.gz',
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    for i, chunk in enumerate(df_iter):
        print(f"Inserting chunk {i}, rows={len(chunk)}")
        
        if i == 0:
            chunk.head(n=0).to_sql(
                name=target_table, 
                con=engine, 
                if_exists='replace'
            )

        chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append",
            index=False
        )

        print("Done")

if __name__ == '__main__':
    ingest_data()