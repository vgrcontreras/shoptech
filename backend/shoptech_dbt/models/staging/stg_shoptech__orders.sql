with

source as (

    select * from {{ source('shoptech', 'orders') }}

)


select * from source