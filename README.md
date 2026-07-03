# PayShield

PayShield is a real-time fraud intelligence platform designed to simulate the core architecture of a modern digital payment system. It combines transaction processing, explainable machine learning, graph-based fraud investigation, and an event-driven microservices architecture to provide an end-to-end payment risk analysis pipeline.

---

## Overview

Modern payment systems require fast transaction processing while identifying fraudulent activity with minimal latency. PayShield provides a modular architecture that evaluates every transaction using both rule-based and machine learning approaches, assigns a fraud risk score, and exposes explainable outputs for investigation.

The platform is built around asynchronous communication using Apache Kafka and follows a microservices architecture to enable scalability and independent service deployment.

---

## Features

- Real-time payment processing workflow
- Machine learning based fraud scoring
- Explainable predictions using SHAP
- Rule-based fraud detection engine
- Graph-based fraud investigation dashboard
- Merchant and account risk profiling
- Event-driven microservices architecture
- Transaction ledger with audit history
- Interactive fraud investigation interface
- Dockerized deployment

---

## System Architecture

```
                +----------------+
                |   React Frontend |
                +--------+-------+
                         |
                    REST APIs
                         |
        +----------------+----------------+
        |                                 |
+-------v-------+                 +-------v-------+
| Payment API   |                 | Fraud API     |
+-------+-------+                 +-------+-------+
        |                                 |
        +-------------+-------------------+
                      |
                Apache Kafka
                      |
    +-----------------+------------------+
    |                 |                  |
+---v----+     +------v------+    +------v------+
| Ledger |     | ML Pipeline |    | Graph Engine|
+--------+     +-------------+    +-------------+
                      |
               PostgreSQL / Redis
```

---

## Technology Stack

### Frontend

- React
- TypeScript
- Tailwind CSS
- Recharts

### Backend

- FastAPI
- Python
- PostgreSQL
- Redis
- Apache Kafka

### Machine Learning

- XGBoost
- Scikit-learn
- SHAP
- Pandas
- NumPy

### DevOps

- Docker
- Docker Compose

---

## Fraud Detection Pipeline

Every incoming transaction passes through the following stages:

1. Transaction validation
2. Rule-based fraud screening
3. Feature engineering
4. Machine learning risk scoring
5. SHAP explanation generation
6. Risk aggregation
7. Ledger persistence
8. Kafka event publication
9. Graph-based investigation

---

## Fraud Features

The machine learning model uses engineered features including:

- Transaction amount
- Transaction velocity
- Merchant risk
- Account age
- Failed payment history
- Device consistency
- Geographic anomalies
- Time-of-day patterns
- Historical fraud rate
- User transaction behaviour

---

## Graph Analytics

The investigation module represents accounts and transactions as a graph to identify coordinated fraud patterns.

Supported capabilities include:

- Risk propagation
- Centrality analysis
- Fraud ring detection
- Connected account discovery
- Transaction path visualization

---

## Explainable AI

Each fraud prediction is accompanied by SHAP explanations showing how individual features contributed to the final fraud score, allowing investigators to understand model decisions instead of relying on black-box predictions.

---

## Project Structure

```
PayShield/
│
├── frontend/
├── payment-service/
├── fraud-service/
├── ledger-service/
├── graph-service/
├── ml-service/
├── notification-service/
│
├── docker-compose.yml
├── README.md
└── docs/
```

---

## Future Improvements

- Real-time streaming dashboards
- Graph Neural Network based fraud detection
- Online model retraining
- Multi-region deployment
- Kubernetes orchestration
- Role-based access control
- Distributed tracing and observability

---

## License

This project was developed for educational and research purposes.
