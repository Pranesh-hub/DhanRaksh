import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Home from "./pages/Home";
import Payment from "./pages/Payment";
import Transactions from "./pages/Transactions";

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

      </Routes>

    </BrowserRouter>
  );
}

export default App;