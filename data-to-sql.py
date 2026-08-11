import pandas as pd
from sqlalchemy import create_engine


df = pd.read_parquet('yellow_tripdata_2023-12.parquet', engine='pyarrow')

print(df.shape)      # строк/колонок
print(df.dtypes)     # типы данных
print(df.head())     # первые строки

engine = create_engine('postgresql://practice:practice@localhost:5432/de_practice')

df.to_sql(
    'trips', 
    engine, 
    if_exists='replace', 
    index=False, 
    chunksize=10000,
    method='multi'  
)

print(f"Загружено {len(df)} строк")