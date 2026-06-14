-- CTE 1: source — just select from Bronze
-- CTE 2: deduplicate — remove duplicate transaction_ids
-- CTE 3: clean — round amount, cast types
-- Final SELECT — output everything including processed_at

with source as (
    SELECT * from {{source('finflow_bronze','RAW_TRANSACTIONS')}}
),
deduplicate as (
    select *, ROW_NUMBER() OVER (PARTITION BY TRANSACTION_ID
    ORDER BY (TIMESTAMP) ) AS rn 
    FROM source 
),
final as (
    select TRANSACTION_ID, USER_ID, MERCHANT_ID, ROUND(AMOUNT,2) as Amount, TIMESTAMP,LOCATION,DEVICE_TYPE,IS_FRAUD
    from deduplicate 
    where rn = 1

)

select *, CURRENT_TIMESTAMP() AS processed_at from final

