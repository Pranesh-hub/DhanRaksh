import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Home from "./pages/Home";
import Payment from "./pages/Payment";
import Transactions from "./pages/Transactions";
import Ledger from "./pages/Ledger";
import Users from "./pages/Users";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Home />} />

        <Route
          path="/payment"
          element={<Payment />}
        />

        <Route
          path="/transactions"
          element={<Transactions />}
        />

        <Route
          path="/ledger"
          element={<Ledger />}
        />

        <Route
          path="/users"
          element={<Users />}
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;