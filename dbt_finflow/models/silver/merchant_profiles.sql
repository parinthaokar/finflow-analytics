with step_one as (
    SELECT * from {{ ref('stg_transactions') }}
),
final as (
   select merchant_id, COUNT(transaction_id) as Total_Transactions, avg(amount) as Average_Transaction_Amount, max(amount) as max_transaction_amount,
    SUM(case when is_fraud then 1 else 0 END ) as total_fraud_flags, count(distinct user_id) as distinct_users, (SUM(case when is_fraud then 1 else 0 end)::float / COUNT(transaction_id)) * 100 as fraud_rate,
    CURRENT_TIMESTAMP() as processed_at
    from step_one
    group by merchant_id    
)

select * from final