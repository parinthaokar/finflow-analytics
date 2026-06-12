# ⚡ FinFlow — Real-Time Fraud Intelligence Platform

> **Fintech companies lose billions annually to payment fraud — not because detection is impossible, but because their data infrastructure can't react fast enough. By the time a fraud pattern surfaces in a next-day report, thousands of transactions have already processed. FinFlow is the pipeline that closes that gap.**

FinFlow is an end-to-end real-time fraud detection platform that streams synthetic financial transactions through a Kafka ingestion layer, processes them with PySpark, lands them in a Snowflake Medallion Architecture, orchestrates transformations via Apache Airflow, and surfaces fraud risk intelligence through an executive Power BI dashboard — all containerized with Docker.

**The core problem it solves:** When a fraud pattern emerges, how quickly can your data infrastructure detect it, score it, and put it in front of a decision-maker? FinFlow answers that in under 2 seconds.

---

## 🏗️ Architecture

```
Synthetic Data Generator (Python / Faker)
        ↓
Apache Kafka (Producer → Topic → Consumer)
        ↓
Snowflake — Bronze Layer (raw transactions)
        ↓
dbt Core — Silver Layer (cleansed, validated, enriched)
        ↓
dbt Core — Gold Layer (fraud risk scores, velocity metrics, merchant anomalies)
        ↓
Apache Airflow — Orchestration (DAGs for batch reconciliation)
        ↓
Power BI — Executive Dashboard (fraud exposure, revenue at risk, cohort analysis)
```

---

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data Generation | Python, Faker | Synthetic Stripe-like transaction data with fraud patterns |
| Streaming Ingestion | Apache Kafka | Real-time transaction streaming |
| Stream Processing | PySpark, Spark Structured Streaming | Consumer processing & Bronze landing |
| Data Warehouse | Snowflake | Medallion Architecture (Bronze/Silver/Gold) |
| Transformation | dbt Core | Modular SQL transformations, schema validation |
| Orchestration | Apache Airflow | DAG-based pipeline scheduling |
| Containerization | Docker, Docker Compose | Reproducible local environment |
| BI & Reporting | Power BI | Executive fraud intelligence dashboard |

---

## 📁 Repository Structure

```
finflow-analytics/
├── README.md
├── STANDUP.md                  # Daily progress log
├── design_doc.md               # Project design & requirements
├── docker-compose.yml          # Kafka + Zookeeper + Airflow setup
├── ingestion/
│   ├── producer.py             # Kafka transaction producer
│   └── consumer.py             # Kafka consumer → Snowflake Bronze
├── data_generator/
│   └── generate_transactions.py # Synthetic fintech data generator
├── dbt_finflow/
│   ├── models/
│   │   ├── staging/            # Raw → cleaned
│   │   ├── silver/             # Enriched transactions, customer profiles
│   │   └── gold/               # Fraud scores, velocity metrics, cohorts
├── airflow/
│   └── dags/                   # Orchestration DAGs
├── dashboard/                  # Power BI files
└── docs/
    └── architecture.png        # Architecture diagram
```

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Snowflake account (free trial works)
- dbt Core (`pip install dbt-snowflake`)

### Setup
```bash
# Clone the repo
git clone https://github.com/parinthaokar/finflow-analytics.git
cd finflow-analytics

# Start Kafka + Zookeeper
docker-compose up -d

# Install Python dependencies
pip install -r requirements.txt

# Generate synthetic transaction data
python data_generator/generate_transactions.py

# Start the Kafka producer
python ingestion/producer.py
```

---

## 📊 Business Impact

| Metric | Target |
|---|---|
| Transaction flagging latency | < 2 seconds |
| Fraud exposure modeled | $X across X transactions |
| Pipeline uptime | 99%+ via Airflow monitoring |
| Dashboard refresh | Automated, no manual runs |

---

## 📅 Build Log
See [STANDUP.md](./STANDUP.md) for daily progress updates.

---

## 👤 Author
**Parin Thaokar** — Data Science & Finance @ UNC Charlotte  
[LinkedIn](https://linkedin.com/in/parinthaokar) | [GitHub](https://github.com/parinthaokar)
