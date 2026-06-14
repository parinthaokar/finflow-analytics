with step_one as (
    SELECT * from {{ ref('stg_transactions') }}
),
final as (
select user_id, count(transaction_id) as Total_Transactions, avg(amount) as Average_Transaction_Amount, max(amount) as max_transaction_amount, 
SUM(case when is_fraud then 1 else 0 END ) as total_fraud_flags, count(distinct merchant_id) as distinct_merchants, COUNT(DISTINCT LOCATION) as distinct_locations , min(timestamp) as first_seen, 
max(timestamp) as last_seen, CURRENT_TIMESTAMP() as processed_at
from step_one
group by user_id
)

select * from final