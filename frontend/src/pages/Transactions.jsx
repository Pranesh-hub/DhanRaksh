import { useEffect, useState } from "react";
import axios from "axios";

export default function Transactions() {

  const [transactions, setTransactions] = useState([]);

  useEffect(() => {

    axios
      .get("http://127.0.0.1:8000/transactions")
      .then((res) => setTransactions(res.data));

  }, []);

  const riskColor = (level) => {
    if (level === "CRITICAL")
      return "red";

    if (level === "HIGH")
      return "orange";

    if (level === "MEDIUM")
      return "gold";

    return "green";
  };

  return (
    <div>

      <h2>Transactions</h2>

      {transactions.map((txn) => (

        <div
          key={txn.id}
          style={{
            border: "1px solid black",
            padding: "10px",
            margin: "10px"
          }}
        >

          <p>Transaction #{txn.id}</p>

          <p>Amount: ₹{txn.amount}</p>

          <p>Status: {txn.status}</p>

          <p>Fraud Score: {txn.fraud_score}</p>

          <p style={{color: riskColor(txn.risk_level)}}>Risk Level: {txn.risk_level}</p>

          <p>Reasons: {txn.fraud_reasons}</p>

        </div>

      ))}

    </div>
  );
}