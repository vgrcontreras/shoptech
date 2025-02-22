with

sales_by_region as (

    select
        t2.state
		,count(t1.id) as total_orders
    from
        {{ ref('stg_shoptech__orders') }} t1
		-- staging.stg_shoptech__orders t1
	inner join
        {{ ref('stg_shoptech__customers') }} t2
		-- staging.stg_shoptech__customers t2
		on t1.customer_id = t2.customer_id
	group by t2.state
	order by total_orders desc
	
),

sales_by_region_share as (

	select
		state
		,total_orders
		,SUM(total_orders) OVER () as grand_total_orders
	from
		sales_by_region
	group by state, total_orders
	
),

sales_by_region_share_percent as (

	select
		state
		,total_orders
		,round((total_orders / grand_total_orders), 4) as state_share
	from
		sales_by_region_share
	order by total_orders desc
	
)

select * from sales_by_region_share_percent