import { useEffect, useState } from "react";
import axios from "axios";

export default function Transactions() {

  const [transactions, setTransactions] = useState([]);

  useEffect(() => {

    axios
      .get("http://127.0.0.1:8000/transactions")
      .then((res) => setTransactions(res.data));

  }, []);

  return (
    <div>

      <h2>Transactions</h2>

      {transactions.map((txn) => (

        <div key={txn.id}>

          #{txn.id}

          {" | "}

          ₹{txn.amount}

          {" | "}

          {txn.status}

        </div>

      ))}

    </div>
  );
}