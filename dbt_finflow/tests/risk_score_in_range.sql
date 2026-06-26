SELECT *
FROM {{ ref('fraud_scores') }}
WHERE risk_score < 0 OR risk_score > 100