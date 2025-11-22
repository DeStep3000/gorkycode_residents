// Базовый URL API (подставь свой реальный адрес/порт, если нужен)
const API_BASE_URL = "http://localhost:8000";

// Селекторы важных элементов
const complaintsListEl = document.getElementById("complaints-list");
const notificationCountEl = document.getElementById("notification-count");
const notificationPopupEl = document.getElementById("notification-popup");
const notificationPopupTitleEl = document.getElementById("notification-popup-title");
const notificationPopupTextEl = document.getElementById("notification-popup-text");
const notificationPopupCloseBtn = document.getElementById("notification-popup-close");
const notificationPopupOpenBtn = document.getElementById("notification-popup-open");

// Последнее уведомление — будем хранить complaint_id, чтобы открыть историю по кнопке
let lastNotificationComplaintId = null;
let notificationCount = 0;
function mapStatusToText(statusCode) {
    switch (statusCode) {
        case "need_moderation":
            return { text: "Нужна модерация", cls: "status-label--moderation" };
        case "ai_redirected":
            return { text: "Перенаправлена ИИ", cls: "status-label--ai" };
        default:
            return { text: statusCode ?? "Неизвестный статус", cls: "" };
    }
}

async function loadComplaints() {
    try {
        const resp = await fetch(`${API_BASE_URL}/complaints/?limit=50&offset=0`);

        if (!resp.ok) {
            console.error("Ошибка при загрузке заявок:", resp.status);
            return;
        }

        const complaints = await resp.json();
        complaintsListEl.innerHTML = "";

        complaints.forEach((complaint) => {
            const status = mapStatusToText(complaint.status);

            const card = document.createElement("div");
            card.className = "complaint-card";

            card.innerHTML = `
                <div class="complaint-card__left">
                    <div class="complaint-card__title">
                        Заявка номер №${complaint.complaint_id}
                    </div>
                    <div class="complaint-card__address">
                        ${complaint.address ?? ""}
                    </div>
                </div>
                <div class="complaint-card__right">
                    <div class="status-label ${status.cls}">
                        ${status.text}
                    </div>
                </div>
            `;

            card.addEventListener("click", () => {
                openComplaintHistory(complaint.complaint_id);
            });

            complaintsListEl.appendChild(card);
        });
    } catch (e) {
        console.error("Ошибка при запросе /complaints/:", e);
    }
}

/**
 * Переход на страницу истории статусов.
 * В качестве id используем query-параметр, чтобы history.html мог его прочитать.
 */
function openComplaintHistory(complaintId) {
    window.location.href = `history.html?complaint_id=${encodeURIComponent(complaintId)}`;
}

/**
 * Подключение к WebSocket и обработка уведомлений
 */
// Бэк на FastAPI

const API_BASE_URL = "http://127.0.0.1:8000";

function initWebSocket() {
    const wsUrl = "ws://127.0.0.1:8000/ws/notifications";
    // если у роутера есть префикс /api:
    // const wsUrl = "ws://127.0.0.1:8000/api/ws/notifications";

    const socket = new WebSocket(wsUrl);

    socket.addEventListener("open", () => {
        console.log("WebSocket подключен");
    });

    socket.addEventListener("message", (event) => {
        const data = JSON.parse(event.data);
        handleNotification(data);
    });

    socket.addEventListener("close", () => {
        console.log("WebSocket закрыт");
    });

    socket.addEventListener("error", (err) => {
        console.error("Ошибка WebSocket:", err);
    });
}


/**
 * Обработка уведомления, пришедшего по WebSocket:
 *  - увеличиваем счетчик на колокольчике,
 *  - показываем попап,
 *  - сохраняем complaint_id для перехода в историю.
 */
function handleNotification(message) {
    // Обновляем счетчик
    notificationCount += 1;
    notificationCountEl.textContent = String(notificationCount);

    // Запоминаем ID заявки
    lastNotificationComplaintId = message.complaint_id;

    // Заполняем текст попапа
    notificationPopupTitleEl.textContent = `Заявка №${message.complaint_id}`;
    notificationPopupTextEl.textContent = message.description ?? "Новое уведомление по заявке";

    // Показываем попап
    notificationPopupEl.classList.remove("hidden");
}

/**
 * Инициализация обработчиков для попапа
 */
function initNotificationPopupHandlers() {
    notificationPopupCloseBtn.addEventListener("click", () => {
        notificationPopupEl.classList.add("hidden");
    });

    notificationPopupOpenBtn.addEventListener("click", () => {
        if (lastNotificationComplaintId != null) {
            openComplaintHistory(lastNotificationComplaintId);
        }
    });
}

/**
 * Инициализация страницы
 */
document.addEventListener("DOMContentLoaded", () => {
    loadComplaints();
    initWebSocket();
    initNotificationPopupHandlers();
});
