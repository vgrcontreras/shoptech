-- Quais são os produtos com melhores margens e suas respectivas quantidade de vendas e ranking de vendas?

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
		-- staging.stg_shoptech__products products
		on products.product_id = orders.product_id
	
),

teste2 as (

	select
		*
		,((product_selling_price - product_buying_price) / product_buying_price) * 100 as margin
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
	,round(avg_margin, 2) avg_margin
	,RANK() OVER(ORDER BY total_orders DESC) as ranking_total_orders
from
	teste3
order by avg_margin desc
limit 10