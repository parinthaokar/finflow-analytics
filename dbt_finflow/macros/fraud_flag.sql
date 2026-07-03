{% macro sum_fraud_flag(is_fraud)%}
sum(case when {{is_fraud}} then 1 else 0 end) 
{%endmacro%}