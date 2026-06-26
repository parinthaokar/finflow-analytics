SELECT *
FROM FINFLOW.SILVER_GOLD.fraud_scores
WHERE risk_score < 0 OR risk_score > 100