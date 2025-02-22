-- quais são as sub_categorias com mais vendas e qual seu ranking em termos de marge?

with

fct_orders as (

	select
		orders.id
		,products.sub_category
		,round(orders.order_value::numeric, 2) as total_selling_order_value
		,(orders.products_quantity * products.price) as total_buying_order_value
	from
		{{ ref('stg_shoptech__orders') }} orders
		-- staging.stg_shoptech__orders orders
	inner join
		staging.stg_shoptech__products products
		on orders.product_id = products.product_id

),

agg_orders_subcategory_data as (

	select
		sub_category
		,count(id) as total_orders
		,sum(total_selling_order_value) as total_selling_order_value
		,sum(total_buying_order_value::numeric) as total_buying_order_value
	from 
		fct_orders
	group by
		sub_category
	
),

gross_profit as (

	select
		sub_category
		,total_orders
		,total_selling_order_value
		,total_buying_order_value
		,(total_selling_order_value - total_buying_order_value) as gross_profit
	from
		agg_orders_subcategory_data

)

select * from gross_profit
