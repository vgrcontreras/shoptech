with

source as (

    select * from {{source ('shoptech', 'products')}}

),

renamed as (

    select
        id as product_id
        ,name as product_name
        ,category
        ,sub_category
        ,brand
        ,price
    from
        source

)

select * from renamed