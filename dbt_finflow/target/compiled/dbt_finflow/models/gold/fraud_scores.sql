with stage as (
    select * from FINFLOW.SILVER_SILVER.stg_transactions
), customer_profile as (

     select * from FINFLOW.SILVER_SILVER.customer_profiles
), merchant_profiles as (

     select * from FINFLOW.SILVER_SILVER.merchant_profiles
), join_final as(
select
    s.transaction_id,
    s.user_id,
    s.merchant_id,
    s.amount,
    s.timestamp,
    s.location,
    s.device_type,
    s.is_fraud,
    cp.total_fraud_flags,
    cp.Average_Transaction_Amount,
    ms.fraud_rate,
    ms.Average_Transaction_Amount as merchant_avg_amount
from stage s
join customer_profile cp on s.user_id = cp.user_id
join merchant_profiles ms on s.merchant_id = ms.merchant_id 
), risk_score as (
    select
        *,
        (CASE WHEN fraud_rate > 50 THEN 40 ELSE 0 END) +
        (CASE WHEN amount > (2 * Average_Transaction_Amount) THEN 25 ELSE 0 END) +
        (CASE WHEN total_fraud_flags > 0 THEN 20 ELSE 0 END) +
        (CASE WHEN amount > 2000 THEN 15 ELSE 0 END) as risk_score
    from join_final
)



SELECT 
    transaction_id,
    user_id,
    merchant_id,
    amount,
    timestamp,
    location,
    device_type,
    is_fraud,
    total_fraud_flags,
    fraud_rate,
    risk_score,
    CASE 
        WHEN risk_score >= 80 THEN 'HIGH'
        WHEN risk_score BETWEEN 40 AND 79 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_label,
    CURRENT_TIMESTAMP() as processed_at
FROM risk_score