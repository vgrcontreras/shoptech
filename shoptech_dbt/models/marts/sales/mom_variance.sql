with

current_year_sales as (

select
    id
    ,extract(month from order_date) as order_month
from
	{{ ref('stg_shoptech__orders') }}
    -- staging.stg_shoptech__orders
where 1=1
	-- WHERE CONDITION TO FILTER ONLY VALUES FOR CURRENT YEAR
	and date_part('year', order_date) = date_part('year', CURRENT_DATE)

),

total_orders_per_month as (

	select
		order_month
		,count(id) as total_orders
	from
		current_year_sales
	group by order_month

),

lag_total_orders_per_month as (

select
	order_month
	,total_orders
	,LAG(total_orders) OVER() as previous_total_order
from
	total_orders_per_month	

),

mom_variance as (

select
	order_month
	,total_orders
	,((total_orders::numeric - previous_total_order::numeric) / NULLIF(previous_total_order::numeric, 0)) AS percentage_variance
from
	lag_total_orders_per_month
	
)

select
	order_month
	,total_orders
	,percentage_variance as percentage_variance
	,SUM(total_orders) OVER () as sum_total_orders
from
	mom_variance