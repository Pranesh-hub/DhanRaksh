import { useState } from "react";
import axios from "axios";

export default function Payment() {

  const [senderId, setSenderId] = useState("");
  const [receiverId, setReceiverId] = useState("");
  const [amount, setAmount] = useState("");

  const handleSubmit = async () => {

    const response = await axios.post(
      "http://127.0.0.1:8000/payment",
      {
        sender_id: Number(senderId),
        receiver_id: Number(receiverId),
        amount: Number(amount)
      }
    );

    alert(
      `Transaction ID: ${response.data.transaction_id}`
    );
  };

  return (
    <div>
      <h2>Make Payment</h2>

      <input
        placeholder="Sender ID"
        value={senderId}
        onChange={(e) => setSenderId(e.target.value)}
      />

      <br />

      <input
        placeholder="Receiver ID"
        value={receiverId}
        onChange={(e) => setReceiverId(e.target.value)}
      />

      <br />

      <input
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />

      <br />

      <button onClick={handleSubmit}>
        Pay
      </button>
    </div>
  );
}