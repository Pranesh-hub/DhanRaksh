import { useEffect, useState } from "react";
import axios from "axios";

export default function FraudDashboard() {

    const [transactions, setTransactions] =
        useState([]);

    useEffect(() => {

        axios
            .get(
                "http://127.0.0.1:8000/fraud-transactions"
            )
            .then((res) =>
                setTransactions(res.data)
            );

        axios
            .get(
                "http://127.0.0.1:8000/fraud-summary"
            )
            .then(res =>
                setSummary(res.data)
            );

        axios
            .get(
                "http://127.0.0.1:8000/top-risky-merchants"
            )
            .then(res =>
                setMerchants(res.data)
            );

        axios
            .get(
                "http://127.0.0.1:8000/top-risky-users"
            )
            .then(res =>
                setUsers(res.data)
            );

    }, []);

    const getColor = (risk) => {

        if (risk === "CRITICAL")
            return "red";

        if (risk === "HIGH")
            return "orange";

        if (risk === "MEDIUM")
            return "gold";

        return "green";
    };

    const [summary, setSummary] =
    useState({});

    const [merchants, setMerchants] =
        useState([]);

    const [users, setUsers] =
        useState([]);

    return (
        <div>

            <h1>
                Fraud Dashboard
            </h1>

            <div>

                <h2>
                    Total Transactions:
                    {" "}
                    {summary.total_transactions}
                </h2>

                <h2>
                    Suspicious:
                    {" "}
                    {summary.suspicious_transactions}
                </h2>

                <h2>
                    Critical:
                    {" "}
                    {summary.critical_transactions}
                </h2>

                <h2>
                    Avg Fraud Score:
                    {" "}
                    {summary.avg_fraud_score}
                </h2>

            </div>

            <h2>Top Risky Merchants</h2>

            {
                merchants.map(m => (

                    <div key={m.id}>

                        {m.name}

                        {" | Risk Score: "}

                        {m.risk_score}

                    </div>

                ))
            }

            <h2>Top Risky Users</h2>

            {
                users.map(u => (

                    <div key={u.user_id}>

                        {u.name}

                        {" | Risk Score: "}

                        {u.risk_score}

                    </div>

                ))
}

            {transactions.map((txn) => (

                <div
                    key={txn.id}
                    style={{
                        border: "1px solid black",
                        padding: "10px",
                        margin: "10px"
                    }}
                >

                    <p>
                        Transaction #{txn.id}
                    </p>

                    <p>
                        Amount: ₹{txn.amount}
                    </p>

                    <p>
                        Fraud Score:
                        {" "}
                        {txn.fraud_score}
                    </p>

                    <p
                        style={{
                            color: getColor(
                                txn.risk_level
                            )
                        }}
                    >
                        Risk Level:
                        {txn.risk_level}
                    </p>

                    <p>
                        Reasons:
                        {" "}
                        {txn.fraud_reasons}
                    </p>

                </div>

            ))}

        </div>
    );
}