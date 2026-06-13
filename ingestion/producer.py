import sys
import json
import time
from kafka import KafkaProducer

sys.path.append('data_generator')
from generate_transactions import create_transactions

producer = KafkaProducer(
    bootstrap_servers= 'localhost:9092',
    value_serializer=lambda x: json.dumps(x, default=str).encode('utf-8')
)

# Loop forever
while True:
    transaction = create_transactions()  # generate one transaction
    producer.send('transactions', value=transaction)  # send to 'transactions' topic
    print(f"Sent: {transaction['transaction_id']} | Fraud: {transaction['is_fraud']} | Amount: ${transaction['amount']:.2f}")
    time.sleep(0.5)  # sleep 0.5 seconds between messages