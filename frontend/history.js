const API_BASE_URL = "http://localhost:8000";

const complaintIdInputEl = document.getElementById("complaint-id-input");
const historyListEl = document.getElementById("history-list");

/**
 * Получаем complaint_id из query-параметра, например:
 * history.html?complaint_id=123456
 */
function getComplaintIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("complaint_id");
    return id ? Number(id) : null;
}

/**
 * Загружаем историю статусов заявки и отрисовываем
 */
async function loadComplaintHistory(complaintId) {
    try {
        // ВАЖНО: твоя ручка объявлена как @router.get("/statuses/complaint_id")
        // и принимает complaint_id как query-параметр.
        //
        // Значит URL будет вида:
        //   /statuses/complaint_id?complaint_id=123
        //
        // Если поменяешь роут на /statuses/, поправь здесь!
        const resp = await fetch(
            `${API_BASE_URL}/statuses/complaint_id?complaint_id=${encodeURIComponent(
                complaintId
            )}`
        );

        if (!resp.ok) {
            console.error("Ошибка при загрузке статусов:", resp.status);
            return;
        }

        const statuses = await resp.json();

        renderHistory(statuses);
    } catch (e) {
        console.error("Ошибка при запросе истории статусов:", e);
    }
}

/**
 * Отрисовка истории в стиле твоих блоков Frame 23 / 24 / 25 / 26
 */
function renderHistory(statuses) {
    historyListEl.innerHTML = "";

    if (!Array.isArray(statuses) || statuses.length === 0) {
        historyListEl.textContent = "История изменений отсутствует.";
        return;
    }

    // Можно отсортировать по sort_order, если нужно
    statuses.sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0));

    statuses.forEach((status) => {
        const item = document.createElement("div");
        item.className = "history-item";

        // status.data — предполагаю, что там дата статуса (или ты можешь хранить отдельное поле)
        // Если там что-то другое, адаптируй.
        const dateStr = status.data?.created_at ?? status.data ?? "";

        item.innerHTML = `
            <div class="history-item__header">
                <div class="history-item__date">${escapeHtml(dateStr)}</div>
                <div class="history-item__author">
                    ${escapeHtml(status.executor_id ? `Исполнитель: ${status.executor_id}` : "Система")}
                </div>
            </div>
            <div class="history-item__status-line">
                <span class="history-item__status-label">Статус:</span>
                <span class="history-item__status-value">
                    ${escapeHtml(mapStatusCode(status.status_code))}
                </span>
            </div>
            <div class="history-item__description">
                ${escapeHtml(status.description ?? "")}
            </div>
        `;

        historyListEl.appendChild(item);
    });
}

/**
 * Маппинг кодов статусов на "чипы"
 */
function mapStatusCode(code) {
    switch (code) {
        case "NEW":
            return "Новое";
        case "ON_MODERATION":
            return "На модерации";
        case "AI_STOPPED":
            return "Остановлено ИИ";
        case "ASSIGNED":
            return "Назначено ответственному";
        default:
            return code ?? "Неизвестный статус";
    }
}

/**
 * Простая защита от XSS
 */
function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}

/**
 * Инициализация страницы истории
 */
document.addEventListener("DOMContentLoaded", () => {
    const complaintId = getComplaintIdFromUrl();

    if (!complaintId) {
        historyListEl.textContent = "Не передан параметр complaint_id";
        return;
    }

    complaintIdInputEl.value = complaintId;

    loadComplaintHistory(complaintId);
});
