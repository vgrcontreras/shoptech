with

source as (

    select * from {{ source('shoptech', 'customers') }}

),

renamed as (

    select
        id as customer_id
        ,first_name
        ,last_name
        ,email
        ,phone_number
        ,gender
        ,date_of_birth
        ,address
        ,city
        ,state
        ,country
        ,postal_code
        ,created_at
    from
        source

)

select * from renamed