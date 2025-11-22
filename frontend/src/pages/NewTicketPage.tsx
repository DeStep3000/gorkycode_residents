import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { API_BASE } from "../config";

const API_BASE = "http://localhost:8000";

export default function NewTicketPage() {
  const [description, setDescription] = useState("");
  const [categoryId, setCategoryId] = useState<number | null>(null);

  const navigate = useNavigate();

  const submit = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      alert("Сначала авторизуйтесь");
      return;
    }

    try {
      const res = await axios.post(
        `${API_BASE}/api/tickets/`,   // ← важный слэш в конце
        {
          description,
          category_id: categoryId,
          relevance: 5,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const ticketId = res.data.id;
      navigate(`/tickets?open=${ticketId}`);
    } catch (e: any) {
      console.error(e);
      alert("Не удалось создать заявку");
    }
  };

  return (
    <div style={{ padding: "40px", maxWidth: "700px", margin: "0 auto" }}>
      <h2 style={{ marginBottom: "20px" }}>Форма приёма заявки</h2>

      <div style={{ marginBottom: "20px" }}>
        <label>
          <b>Описание *</b>
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={8}
          style={{ width: "100%", marginTop: "10px", padding: "10px" }}
        />
      </div>

      <div style={{ marginBottom: "20px" }}>
        <label>
          <b>Категория</b>
        </label>
        <select
          value={categoryId ?? ""}
          onChange={(e) =>
            setCategoryId(e.target.value ? Number(e.target.value) : null)
          }
          style={{ width: "100%", marginTop: "10px", padding: "10px" }}
        >
          <option value="">Не выбрано</option>
          <option value="1">Дороги</option>
          <option value="2">Освещение</option>
          <option value="3">Мусор</option>
        </select>
      </div>

      <button
        onClick={submit}
        style={{
          padding: "15px 25px",
          background: "#005ff9",
          color: "white",
          borderRadius: "8px",
          border: "none",
          fontSize: "18px",
        }}
      >
        Отправить
      </button>
    </div>
  );
}
