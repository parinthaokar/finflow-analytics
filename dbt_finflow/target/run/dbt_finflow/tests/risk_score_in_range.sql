
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT *
FROM FINFLOW.SILVER_GOLD.fraud_scores
WHERE risk_score < 0 OR risk_score > 100
  
  
      
    ) dbt_internal_test