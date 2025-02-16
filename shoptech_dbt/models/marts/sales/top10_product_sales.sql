with 

top_10_products_by_sales as (

    select
        products.product_name,
        count(id) as total_pedidos
    from
        -- staging.stg_shoptech__orders as orders
        {{ ref('stg_shoptech__orders') }} as orders
    inner join
        -- staging.stg_shoptech__products as products
        {{ ref('stg_shoptech__products') }} as products
        on products.product_id = orders.product_id
    group by
        products.product_name
    order by total_pedidos desc
    limit 10

)

select * from top_10_products_by_sales