select
    id,
    shipping_date
from {{ ref('stg_shoptech__orders') }}
where estimated_delivery_date < shipping_date