import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import NewTicketPage from "./pages/NewTicketPage";
import TicketsChatListPage from "./pages/TicketsChatListPage";
import AuthPage from "./pages/AuthPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/new" element={<NewTicketPage />} />
      <Route path="/tickets" element={<TicketsChatListPage />} />
    </Routes>
  );
}
