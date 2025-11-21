// frontend/src/components/Chat.tsx
import { useEffect, useRef, useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

type Message = {
  id?: number;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
};

interface ChatProps {
  ticketId: number;
  token: string;
}

export default function Chat({ ticketId, token }: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const wsRef = useRef<WebSocket | null>(null);

  // 1) грузим историю при входе в чат
  useEffect(() => {
    if (!token) return;

    axios
      .get(`${API_BASE}/api/tickets/${ticketId}/messages`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        // бэк отдаёт { messages: [ ... ] }
        setMessages(res.data.messages ?? []);
      })
      .catch((err) => {
        console.error("failed to load history", err);
      });
  }, [ticketId, token]);

  // 2) подключаемся к вебсокету
  useEffect(() => {
    if (!token) return;

    const ws = new WebSocket(
      `ws://localhost:8000/ws/tickets/${ticketId}?token=${token}`
    );
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        // ты шлёшь {"role": "assistant", "delta": "..."} — стриминг токенов
        if (data.role === "assistant") {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last && last.role === "assistant" && !last.id) {
              // доклеиваем токены в последнее ассистентское сообщение
              const updated = [...prev];
              updated[updated.length - 1] = {
                ...last,
                content: last.content + data.delta,
              };
              return updated;
            }
            // если нет текущего ассистентского — создаём
            return [...prev, { role: "assistant", content: data.delta }];
          });
        }
      } catch (e) {
        console.error("ws message parse error", e);
      }
    };

    ws.onclose = () => {
      console.log("ws closed");
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [ticketId, token]);

  // 3) отправка сообщений
  const send = () => {
    if (!input.trim()) return;
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      alert("Нет соединения с чатом");
      return;
    }

    const text = input.trim();

    // оптимистично добавляем своё сообщение
    setMessages((prev) => [...prev, { role: "user", content: text }]);

    wsRef.current.send(text);
    setInput("");
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        borderRadius: 12,
        border: "1px solid #ddd",
        padding: 16,
      }}
    >
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          marginBottom: 12,
          paddingRight: 4,
        }}
      >
        {messages.map((m, idx) => (
          <div
            key={m.id ?? idx}
            style={{
              marginBottom: 8,
              textAlign: m.role === "user" ? "right" : "left",
            }}
          >
            <div
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: 12,
                background:
                  m.role === "user" ? "#005ff9" : "rgba(0,0,0,0.05)",
                color: m.role === "user" ? "#fff" : "#000",
                maxWidth: "80%",
                whiteSpace: "pre-wrap",
              }}
            >
              {m.content}
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Напишите сообщение..."
          style={{
            flex: 1,
            padding: 8,
            borderRadius: 8,
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={send}
          style={{
            padding: "8px 16px",
            borderRadius: 8,
            border: "none",
            background: "#005ff9",
            color: "#fff",
            cursor: "pointer",
          }}
        >
          Отправить
        </button>
      </div>
    </div>
  );
}
