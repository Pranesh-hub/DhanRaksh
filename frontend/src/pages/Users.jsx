import { useEffect, useState } from "react";
import axios from "axios";

export default function Users() {

  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/users")
      .then((res) => setUsers(res.data));
  }, []);

  return (
    <div>
      <h2>Users</h2>

      {users.map((user) => (
        <div key={user.id}>
          {user.name}
          {" | "}
          Balance: ₹{user.balance}
        </div>
      ))}
    </div>
  );
}