import { useEffect, useState } from "react";
import axios from "axios";

export default function Ledger() {

  const [entries, setEntries] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/ledger")
      .then((res) => setEntries(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2>Ledger Entries</h2>

      {entries.map((entry) => (
        <div key={entry.id}>
          User: {entry.user_id}
          {" | "}
          {entry.event_type}
          {" | "}
          ₹{entry.amount}
        </div>
      ))}
    </div>
  );
}