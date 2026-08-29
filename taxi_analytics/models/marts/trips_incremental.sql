{{
    config(
        materialized='incremental',
        unique_key='trip_id'            
    )
}}
-- не пересоздавать и дописывать в строки в существующую
-- на проверку дубля
select
    row_number() over (order by pickup_datetime, vendor_id) as trip_id,
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    fare_amount,
    trip_distance
from {{ ref('stg_trips') }}


{% if is_incremental() %}             --условие на проверку таблицы если нет --full-refresh
    where pickup_datetime > (select max(pickup_datetime) from {{ this }})      --ссылается на саму себя, и береёт только строки новее чем макс. дата
{% endif %}







-- docker exec -it airflow-practice-airflow-scheduler-1 bash -c "cd /opt/airflow/dbt && dbt run --select trips_incremental"
-- docker exec -it airflow-practice-airflow-scheduler-1 bash -c "cd /opt/airflow/dbt && dbt run --select trips_incremental"