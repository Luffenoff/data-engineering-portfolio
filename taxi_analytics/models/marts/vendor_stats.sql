select
    vendor_id,
    count(*) as trip_count,
    round(avg(fare_amount)::numeric, 2) as avg_fare,
    round(avg(trip_distance)::numeric, 2) as avg_distance,
    round(sum(total_amount)::numeric, 2) as total_revenue
from {{ ref('stg_trips') }}
group by vendor_id
order by vendor_id