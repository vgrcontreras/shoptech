select
    id,
    shipping_date
from {{ ref('stg_shoptech__orders') }}
where shipping_date < order_date