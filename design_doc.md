# 📐 FinFlow — Project Design Document

**Author:** Parin Thaokar  
**Role:** Data Engineering Intern (Simulated)  
**Company:** FinFlow Analytics (Personal Project)  
**Date:** June 2026  
**Status:** In Progress

---

## 1. Problem Statement

Fintech companies process millions of transactions daily. Fraud detection systems that rely on batch processing introduce dangerous lag — by the time fraud patterns surface in a next-day report, significant financial damage has already occurred.

**The question this project answers:**
> How quickly can a modern data engineering pipeline detect, score, and surface fraud risk from a live transaction stream — and what does that look like end to end?

---

## 2. Goals & Success Metrics

| Goal | Success Metric |
|---|---|
| Real-time ingestion | Transactions streamed via Kafka with < 2 second latency |
| Scalable storage | Snowflake Medallion Architecture (Bronze/Silver/Gold) |
| Reliable transformations | dbt models with schema tests passing on every run |
| Orchestration | Airflow DAGs running on schedule with 0 manual triggers |
| Business visibility | Power BI dashboard showing fraud exposure, revenue at risk, cohort risk |

---

## 3. Architecture Overview

```
[Python Data Generator] → [Kafka Producer] → [Kafka Topic: transactions]
        → [Kafka Consumer / PySpark] → [Snowflake Bronze]
        → [dbt Silver: cleansed + enriched] → [dbt Gold: fraud scores + metrics]
        → [Airflow: orchestration DAGs]
        → [Power BI: executive dashboard]
```

---

## 4. Data Model

### Synthetic Transaction Schema
| Field | Type | Description |
|---|---|---|
| transaction_id | STRING | Unique transaction identifier |
| user_id | STRING | Customer identifier |
| merchant_id | STRING | Merchant identifier |
| amount | FLOAT | Transaction amount (USD) |
| currency | STRING | Transaction currency |
| timestamp | TIMESTAMP | Transaction time |
| location | STRING | Transaction location |
| device_type | STRING | Mobile / Desktop / ATM |
| is_fraud | BOOLEAN | Ground truth fraud label (for scoring) |

### Medallion Layers
- **Bronze:** Raw transactions as-landed from Kafka, no transformations
- **Silver:** Cleansed, deduplicated, schema-validated, enriched with customer profiles
- **Gold:** Fraud risk scores, velocity metrics, merchant anomaly flags, cohort segments

---

## 5. Tech Stack & Justification

| Tool | Justification |
|---|---|
| Apache Kafka | Industry-standard for real-time event streaming in fintech |
| PySpark | Scalable stream processing, matches production DE environments |
| Snowflake | Cloud-native warehouse used by most fintech data teams |
| dbt Core | Production-grade transformation framework, version-controlled SQL |
| Apache Airflow | Most in-demand orchestration tool on DE job descriptions |
| Docker | Ensures reproducible local environment |
| Power BI | Executive-facing dashboards, widely used in financial services |

---

## 6. Sprint Plan

### Week 1 — Foundation & Ingestion
- [ ] Docker Compose setup (Kafka + Zookeeper)
- [ ] Synthetic transaction data generator
- [ ] Kafka producer
- [ ] Kafka consumer → Snowflake Bronze

### Week 2 — Transformation & Orchestration
- [ ] dbt project setup
- [ ] Silver layer models (cleansing, validation, enrichment)
- [ ] Gold layer models (fraud scores, velocity, merchant anomalies)
- [ ] Airflow DAGs for orchestration

### Week 3 — Business Impact & Delivery
- [ ] Power BI executive dashboard
- [ ] Quantify business impact metrics
- [ ] Architecture diagram
- [ ] Final README polish + Loom walkthrough video

---

## 7. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Kafka local setup complexity | Docker Compose abstracts the environment |
| Snowflake free trial expiry | Monitor usage, optimize queries early |
| Scope creep | Stick to sprint plan, log blockers daily in STANDUP.md |

---

## 8. Out of Scope
- Real transaction data (synthetic only for privacy/compliance)
- ML model training (rule-based fraud scoring only)
- Production deployment (local + Snowflake cloud only)
