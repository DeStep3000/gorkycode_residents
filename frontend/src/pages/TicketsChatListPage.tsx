import { useEffect, useState } from "react";
import axios from "axios";
import Chat from "../components/Chat";
import { API_BASE } from "../config";

interface Ticket {
  id: number;
  description: string;
  created_at: string;
  relevance: number;
}

export default function TicketsChatListPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [activeId, setActiveId] = useState<number | null>(null);

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) return;

    axios
      .get(`${API_BASE}/api/tickets`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        // бэк возвращает { tickets: [...] }
        const data = res.data;
        setTickets(data.tickets ?? []);
      })
      .catch((err) => {
        console.error(err);
      });
  }, [token]);

  // автооткрытие тикета из /new
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const openId = params.get("open");
    if (openId) setActiveId(Number(openId));
  }, []);

  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "sans-serif" }}>
      {/* Список тикетов */}
      <div
        style={{
          width: "30%",
          borderRight: "1px solid #ddd",
          padding: "20px",
          overflowY: "auto",
        }}
      >
        <h3>Ваши заявки</h3>
        {tickets.map((t) => (
          <div
            key={t.id}
            onClick={() => setActiveId(t.id)}
            style={{
              padding: "10px",
              marginBottom: "10px",
              borderRadius: "8px",
              cursor: "pointer",
              background: activeId === t.id ? "#e8f1ff" : "#f7f7f7",
            }}
          >
            <div>
              <b>#{t.id}</b>
            </div>
            <div style={{ fontSize: "14px", color: "#444" }}>
              {t.description.slice(0, 60)}...
            </div>
          </div>
        ))}
      </div>

      {/* Чат */}
      <div style={{ flex: 1, padding: "20px" }}>
        {activeId ? (
          <Chat ticketId={activeId} token={token!} />
        ) : (
          <div style={{ padding: "20px", color: "#777" }}>
            Выберите заявку из списка слева
          </div>
        )}
      </div>
    </div>
  );
}
