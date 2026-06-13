import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
import json

fake = Faker()

USER_IDS = [f"user_{i}" for i in range(1, 51)]

normal_merchants = [
    "Costco Wholesale",
    "Chevron",
    "Shell",
    "Trader Joe's",
    "Chipotle Mexican Grill",
    "Delta Air Lines",
    "Best Buy",
    "CVS Pharmacy",
    "Lyft Rideshare"
]

sketchy_merchants = [
    "Apex-Privacy-Nodes",
    "Bling-Lux-Liquidators",
    "Z-Crypto-Mixer-Protocol",
    "Mega-Win-Sweepstakes-Hub",
    "Card-Verify-Test-Vendor",
    "Global-Gift-Escrow-LLC",
    "Unlock-Code-Central"
]

DEVICE_TYPES = ["Mobile", "Desktop", "ATM"] 


def create_transactions():
    my_uuid = uuid.uuid4()
    is_fraud = random.random() < 0.10  # 10% chance

    if is_fraud:
        amount = random.uniform(2000,5000) #high amount
        merchent = random.choice(sketchy_merchants)
    else: 
        amount = random.uniform(5,500) #normal amount
        merchent = random.choice(normal_merchants)

    if is_fraud:
        timestamp = datetime.now() - timedelta(seconds=random.uniform(0, 30))
    else:
        timestamp = datetime.now()    
    
    transaction = {"transaction_id": str(uuid.uuid4()), "user_id": random.choice(USER_IDS), 
                   "merchant_id": merchent, "amount": amount, "timestamp": timestamp,
                   "location": fake.city(), "device_type": random.choice(DEVICE_TYPES),"is_fraud":is_fraud}
    return transaction

def generate_batch(num_transactions):
    transactions = []
    for _ in range(num_transactions):
        transactions.append(create_transactions())
    return transactions

if __name__ == "__main__":
    batch = generate_batch(1000)
    for transaction in batch:
        print(json.dumps(transaction, default=str))
