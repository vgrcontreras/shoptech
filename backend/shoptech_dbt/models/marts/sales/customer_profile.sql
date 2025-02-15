-- qual é a faixa etaria de clientes que mais compram conosco e sua média de faturamento?

with

total_orders_per_customer as (

	select
		t2.gender
		,t2.state
		,count(t2.customer_id) as total_orders
		,round(cast(avg(date_part('year', age(t2.date_of_birth))) as numeric), 0) as avg_age
		,round(avg(t1.order_value::numeric), 2) as avg_order_value
	from
        {{ ref('stg_shoptech__orders') }} t1
		-- staging.stg_shoptech__orders t1
	inner join
        {{ ref('stg_shoptech__customers') }} t2
		-- staging.stg_shoptech__customers t2
		on t1.customer_id = t2.customer_id
	group by t2.gender,t2.state
	order by total_orders desc

)

select 
	*
	,rank() over (order by total_orders desc) as rank_total_orders
	,rank() over (order by avg_order_value) as rank_avg_order_value
from 
	total_orders_per_customer
order by total_orders desc