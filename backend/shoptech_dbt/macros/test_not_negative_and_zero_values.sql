{% test not_negative_and_zero_values(model, column_name) %}

    select
        id,
        sum( {{ column_name }} ) as total_amount
    from {{ model }}
    group by 1
    having sum( {{ column_name }} ) <= 0

{% endtest %}