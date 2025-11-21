import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

type Mode = "login" | "register";

export default function AuthPage() {
  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // поля только для регистрации
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");

  const navigate = useNavigate();

  const apiBase = "http://localhost:8000";

  const handleLogin = async () => {
    const res = await axios.post(`${apiBase}/api/auth/login`, {
      email,
      password,
    });

    localStorage.setItem("token", res.data.access_token);
    navigate("/");
  };

const handleRegister = async () => {
  try {
    await axios.post(`${apiBase}/api/auth/register`, {
      email,
      password,
      name,
      surname,
      fathername: null,
      phone: null,
    });

    await handleLogin();
  } catch (e: any) {
    if (axios.isAxiosError(e) && e.response?.status === 400) {
      alert("Пользователь с таким email уже существует");
    } else {
      alert("Ошибка регистрации");
    }
    throw e;
  }
};


  const submit = async () => {
    try {
      if (mode === "login") {
        await handleLogin();
      } else {
        await handleRegister();
      }
    } catch (e: any) {
      console.error(e);
      alert("Ошибка авторизации");
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "50px auto", fontFamily: "sans-serif" }}>
      <h2 style={{ marginBottom: 20 }}>
        {mode === "login" ? "Вход" : "Регистрация"}
      </h2>

      <div style={{ marginBottom: 10 }}>
        <label>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ width: "100%", padding: 8, boxSizing: "border-box" }}
        />
      </div>

      <div style={{ marginBottom: 10 }}>
        <label>Пароль</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: "100%", padding: 8, boxSizing: "border-box" }}
        />
      </div>

      {mode === "register" && (
        <>
          <div style={{ marginBottom: 10 }}>
            <label>Имя</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={{ width: "100%", padding: 8, boxSizing: "border-box" }}
            />
          </div>
          <div style={{ marginBottom: 10 }}>
            <label>Фамилия</label>
            <input
              value={surname}
              onChange={(e) => setSurname(e.target.value)}
              style={{ width: "100%", padding: 8, boxSizing: "border-box" }}
            />
          </div>
        </>
      )}

      <button
        onClick={submit}
        style={{
          width: "100%",
          padding: 10,
          marginTop: 10,
          background: "#005ff9",
          border: "none",
          color: "white",
          borderRadius: 6,
          fontSize: 16,
          cursor: "pointer",
        }}
      >
        {mode === "login" ? "Войти" : "Зарегистрироваться"}
      </button>

      <div style={{ marginTop: 15, fontSize: 14 }}>
        {mode === "login" ? (
          <>
            Нет аккаунта?{" "}
            <button
              type="button"
              onClick={() => setMode("register")}
              style={{ border: "none", background: "none", color: "#005ff9", cursor: "pointer" }}
            >
              Зарегистрироваться
            </button>
          </>
        ) : (
          <>
            Уже есть аккаунт?{" "}
            <button
              type="button"
              onClick={() => setMode("login")}
              style={{ border: "none", background: "none", color: "#005ff9", cursor: "pointer" }}
            >
              Войти
            </button>
          </>
        )}
      </div>
    </div>
  );
}
