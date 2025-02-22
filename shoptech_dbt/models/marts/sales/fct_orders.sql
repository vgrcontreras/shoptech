with 

source as (

    select *
	from
		-- staging.stg_shoptech__orders
		{{ ref('stg_shoptech__orders') }}

),

renamed as (

select
	t1.id as order_id
	,concat(t2.first_name, ' ', t2.last_name) as customer_name
	,t2.gender as customer_gender
	,t2.state as customer_state
	,t3.product_name as product_name
	,t3.category as product_category
	,t3.sub_category as product_subcategory
	,t3.brand as product_brand
	,t1.products_quantity
	,t1.order_value
	,t1.payment_status
	,t1.status
	,t1.payment_method
	,t1.shipping_method
	,t1.shipping_fee
	,t1.shipping_date
	,t1.estimated_delivery_date
	,t1.delivery_date
from
	source t1
inner join
	staging.stg_shoptech__customers t2
-- 	{{ ref('stg_shoptech__customers') }} t2
	on t1.customer_id = t2.customer_id
inner join
-- 	{{ ref('stg_shoptech__products') }} t3
	staging.stg_shoptech__products t3
	on t1.product_id = t3.product_id

)

select * from renamed