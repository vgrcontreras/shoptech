with

year_per_order_id as (

	select
		id
		,extract(year from order_date) as year
		,extract(day from order_date) as dia
		,extract(day from CURRENT_DATE) as dia_atual
	from
		{{ ref('stg_shoptech__orders') }}
		-- staging.stg_shoptech__orders
	where 1=1
),

year_per_order_id_mtd as (

	select
		id
		,year
	from
		year_per_order_id
	where 1=1
		and dia <= dia_atual
),


total_order_per_year as (

	select
		year
		,count(id) as total_order
	from
		year_per_order_id_mtd
	group by year
	order by year
),

lag_total_order_per_year as (

	select
		year
		,total_order
		,LAG(total_order) OVER() as previous_total_order
	from
		total_order_per_year
	
),

tb_yoy_variance as (

	select
		year
		,total_order
		,previous_total_order
		,((total_order::numeric - previous_total_order::numeric) / NULLIF(previous_total_order::numeric, 0)) AS percentage_variance
	from
		lag_total_order_per_year
		
),

tb_rounded_yoy_variance as (

	select
		cast(year as integer) as ano
		,total_order
		,previous_total_order
		,round(percentage_variance, 2) as yoy
	from
		tb_yoy_variance

)

select * from tb_rounded_yoy_variance