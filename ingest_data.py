import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# Constants stay at the top
PREFIX = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'

DTYPE = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    # ... rest of your schema ...
    "congestion_surcharge": "float64"
}

PARSE_DATES = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

# Dynamic config becomes function parameters (with defaults)
def run(
    pg_user='root',
    pg_pass='root',
    pg_host='localhost',
    pg_port=5432,
    pg_db='ny_taxi',
    target_table='yellow_taxi_data',
    year=2021,
    month=1,
    chunksize=100000
):
    # Connection and URL are built locally when run() executes
    url = f'{PREFIX}yellow_tripdata_{year}-{month:02d}.csv.gz'
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_iter = pd.read_csv(
        url,
        dtype=DTYPE,
        parse_dates=PARSE_DATES,
        iterator=True,
        chunksize=chunksize,
    )

    first_chunk = next(df_iter)
    first_chunk.head(0).to_sql(name=target_table, con=engine, if_exists="replace")
    print("Table created")

    first_chunk.to_sql(name=target_table, con=engine, if_exists="append")
    print("Inserted first chunk:", len(first_chunk))

    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(name=target_table, con=engine, if_exists="append")
        print("Inserted chunk:", len(df_chunk))

if __name__ == '__main__':
    run()
