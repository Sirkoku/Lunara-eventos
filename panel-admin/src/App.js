import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./home/Home";
import Admin from "./admin/Admin";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;