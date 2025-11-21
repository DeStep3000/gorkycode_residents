// src/pages/LandingPage.tsx
import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();

  const goNew = () => navigate("/new");
  const goTickets = () => navigate("/tickets");
  const goAuth = () => navigate("/auth");

  return (
    <div
      style={{
        padding: "40px",
        maxWidth: "900px",
        margin: "0 auto",
        fontFamily: "sans-serif",
      }}
    >
      {/* шапка с кнопкой Войти */}
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 30 }}>
        <div style={{ fontWeight: "bold", fontSize: 20 }}>Платформа «Лобачевский»</div>
        <button
          onClick={goAuth}
          style={{
            padding: "8px 16px",
            borderRadius: 8,
            border: "1px solid #005ff9",
            background: "white",
            color: "#005ff9",
            cursor: "pointer",
          }}
        >
          Войти
        </button>
      </div>

      <h1 style={{ fontSize: "36px", marginBottom: "10px" }}>
        Единый портал для решения вопросов жителей
      </h1>

      <p style={{ marginBottom: "30px", fontSize: "18px", color: "#555" }}>
        Средний срок ответа — 3 дня
      </p>

      <div style={{ display: "flex", gap: "20px" }}>
        <button
          onClick={goNew}
          style={{
            padding: "15px 25px",
            background: "#005ff9",
            color: "white",
            fontSize: "18px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
          }}
        >
          Сообщить о проблеме
        </button>

        <button
          onClick={goTickets}
          style={{
            padding: "15px 25px",
            background: "#f1f4ff",
            color: "#0033aa",
            fontSize: "18px",
            borderRadius: "8px",
            border: "1px solid #ccd5ff",
            cursor: "pointer",
          }}
        >
          Открыть чаты по заявкам
        </button>
      </div>
    </div>
  );
}
