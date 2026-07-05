{% macro calculate_risk_score(fraud_rate, amount, avg_amount, fraud_flags) %}
    (CASE WHEN {{ fraud_rate }} > 50 THEN 40 ELSE 0 END) +
    (CASE WHEN {{ amount }} > (2 * {{ avg_amount }}) THEN 25 ELSE 0 END) +
    (CASE WHEN {{ fraud_flags }} > 0 THEN 20 ELSE 0 END) +
    (CASE WHEN {{ amount }} > 2000 THEN 15 ELSE 0 END)
{% endmacro %}