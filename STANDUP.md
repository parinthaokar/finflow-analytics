# 📋 FinFlow — Daily Standup Log

> This log simulates the daily standup cadence of a real data engineering internship.
> Format: **What I did | What I'm doing next | Any blockers**

---

## Week 1 — Foundation & Ingestion

### Day 1 — Jun 12 2026
**✅ Done:**
- Initialized repository with full folder structure
- Created README, STANDUP, and design doc
- Defined project scope and Medallion Architecture design

**🔜 Next:**
- Set up Docker Compose with Kafka + Zookeeper
- Build synthetic transaction data generator

**🚧 Blockers:**
- None

---
### Day 2 — Jun 13 2026
✅ Done:
- Built Kafka producer streaming synthetic transactions to Kafka topic
- Debugged Docker + Python environment issues
- Transactions flowing in real time with fraud patterns visible

🔜 Next:
- Build Kafka consumer → Snowflake Bronze layer

🚧 Blockers:
- Kafka UI loading issue (not critical, producer confirmed working via terminal)
