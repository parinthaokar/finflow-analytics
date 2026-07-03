    import json
    from kafka import KafkaConsumer
    import snowflake.connector

    import os

    conn = snowflake.connector.connect(
        user=os.environ.get('SNOWFLAKE_USER'),
        password=os.environ.get('SNOWFLAKE_PASSWORD'),
        account=os.environ.get('SNOWFLAKE_ACCOUNT'),
        warehouse='COMPUTE_WH',
        database='FINFLOW',
        schema='BRONZE'
    )
    cursor = conn.cursor()

    # Connect to Kafka
    consumer = KafkaConsumer(
        'transactions',  # topic name
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='finflow-consumer-group'
    )

    # Read messages and insert into Snowflake
    for message in consumer:
        transaction = message.value  # get the value from the message

        cursor.execute("""
            INSERT INTO FINFLOW.BRONZE.RAW_TRANSACTIONS 
            (transaction_id, user_id, merchant_id, amount, timestamp, location, device_type, is_fraud)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            transaction['transaction_id'],
            transaction['user_id'],
            transaction['merchant_id'],
            transaction['amount'],
            transaction['timestamp'],
            transaction['location'],
            transaction['device_type'],
            transaction['is_fraud']
        ))

        conn.commit()
        print(f"Landed: {transaction['transaction_id']} | Fraud: {transaction['is_fraud']} | Amount: ${transaction['amount']:.2f}")