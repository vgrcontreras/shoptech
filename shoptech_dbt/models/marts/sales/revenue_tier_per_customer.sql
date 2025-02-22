-- Separe os clientes em 5 grupos de acordo com o valor pago por cliente

with

total_revenue_per_customer_tier as (

select
	customer_id
	,sum(order_value::numeric) as total_revenue
	,NTILE(5) OVER (ORDER BY sum(order_value) DESC) AS group_number
from
	{{ ref('stg_shoptech__orders') }}
	-- staging.stg_shoptech__orders
group by customer_id
order by total_revenue desc

)

select
	concat(t2.first_name, ' ', t2.last_name) as complete_name
	,t2.gender
	,t2.state
	,t1.total_revenue
	,t1.group_number
from
	total_revenue_per_customer_tier t1
inner join 
	staging.stg_shoptech__customers t2
	on t1.customer_id = t2.customer_id
order by t1.total_revenue desc