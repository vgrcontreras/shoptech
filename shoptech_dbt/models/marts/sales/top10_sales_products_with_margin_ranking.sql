-- Quais são os produtos mais vendidos e suas respectivas margens e ranking de margem?

with teste as (
	
	select
		orders.id
		,products.product_name
		,orders.products_quantity
		,round(orders.order_value::numeric, 2) as order_value
		,products.price as product_buying_price
		,round((orders.order_value::numeric / orders.products_quantity), 2) as product_selling_price
	from
		{{ ref('stg_shoptech__orders') }} orders
		-- staging.stg_shoptech__orders as orders
	inner join
		{{ ref('stg_shoptech__products') }} products
		-- staging.stg_shoptech__products as products
		on products.product_id = orders.product_id
	
),

teste2 as (

	select
		*
		,((product_selling_price - product_buying_price) / product_buying_price) as margin
	from
		teste
	
),

teste3 as (

	select
		product_name
		,count(id) as total_orders
		,sum(product_selling_price) as total_value_sold
		,avg(margin::numeric) as avg_margin
	from
		teste2
	group by product_name
	order by total_orders desc

)

select
	product_name
	,total_orders
	,total_value_sold
	,avg_margin avg_margin
	,RANK() OVER(ORDER BY avg_margin DESC) as ranking_margin
from
	teste3
order by total_orders desc