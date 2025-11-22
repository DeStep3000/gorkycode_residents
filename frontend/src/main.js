import './style.css';
import apiService from './api_service.js';

class ModerationDashboard {
  constructor() {
    this.applications = [];
    this.notifications = [];
    this.isLoading = false;

    this.init();
  }

  async init() {
    await this.loadData();
    this.createLayout();
    this.renderApplications();
    this.addEventListeners();
    this.setupScroll();
  }

  async loadData() {
    this.isLoading = true;
    try {
      // Загружаем жалобы с бэкенда
      const complaintsData = await apiService.getComplaints();
      this.applications = this.transformComplaintsData(complaintsData);

      // Загружаем уведомления (можно адаптировать под ваш бэкенд)
      this.notifications = await this.loadNotifications();

    } catch (error) {
      console.error('Error loading data:', error);
      this.showError('Ошибка загрузки данных');
    } finally {
      this.isLoading = false;
    }
  }

  transformComplaintsData(complaintsData) {
    // Преобразуем данные бэкенда в формат фронтенда
    if (!complaintsData || !Array.isArray(complaintsData)) {
      return [];
    }

    return complaintsData.map((complaint, index) => ({
      id: complaint.complaint_id?.toString() || `temp_${index}`,
      status: this.mapBackendStatus(complaint.status),
      position: index * 120 + 100, // Динамическая позиция
      backendData: complaint // Сохраняем оригинальные данные
    }));
  }

  mapBackendStatus(backendStatus) {
    const statusMap = {
      'new': 'moderation',
      'modernized': 'moderation',
      'black_workflow': 'redirected',
      'initial_sum': 'moderation',
      'completed': 'approved',
      'rejected': 'rejected'
    };

    return statusMap[backendStatus] || 'moderation';
  }

  async loadNotifications() {
    try {
      // Пример загрузки уведомлений с бэкенда
      // В реальности нужно создать соответствующий эндпоинт
      const statuses = await apiService.getStatusesByTemplate();

      return statuses.map(status => ({
        id: status.content_id,
        applicationId: status.compilation_id?.toString(),
        type: 'status_update',
        message: status.description || 'Обновление статуса',
        read: false,
        date: status.data
      }));
    } catch (error) {
      console.error('Error loading notifications:', error);
      return [];
    }
  }

  async handleApplicationClick(applicationId) {
    try {
      // Загружаем детальную информацию о жалобе
      const complaintDetail = await apiService.getComplaint(applicationId);
      const statusHistory = await apiService.getComplaintStatuses(applicationId);

      // Переходим на страницу деталей
      this.navigateToApplicationDetail(applicationId, {
        complaint: complaintDetail,
        history: statusHistory
      });

    } catch (error) {
      console.error('Error loading application details:', error);
      this.showError('Ошибка загрузки деталей заявки');
    }
  }

  navigateToApplicationDetail(applicationId, data = null) {
    if (data) {
      // Сохраняем данные в sessionStorage для передачи на страницу деталей
      sessionStorage.setItem(`app_${applicationId}`, JSON.stringify(data));
    }

    window.location.href = `application-detail.html?id=${applicationId}`;
  }

  // Добавляем метод для обновления статуса
  async updateApplicationStatus(applicationId, newStatus) {
    try {
      const statusData = {
        status: this.mapFrontendStatusToBackend(newStatus),
        final_status_at: new Date().toISOString()
      };

      await apiService.updateComplaintStatus(applicationId, statusData);

      // Обновляем локальные данные
      const appIndex = this.applications.findIndex(app => app.id === applicationId);
      if (appIndex !== -1) {
        this.applications[appIndex].status = newStatus;
        this.renderApplications();
      }

      this.showSuccess('Статус успешно обновлен');

    } catch (error) {
      console.error('Error updating status:', error);
      this.showError('Ошибка обновления статуса');
    }
  }

  mapFrontendStatusToBackend(frontendStatus) {
    const reverseStatusMap = {
      'moderation': 'modernized',
      'redirected': 'black_workflow',
      'approved': 'completed',
      'rejected': 'rejected'
    };

    return reverseStatusMap[frontendStatus] || 'modernized';
  }

  showError(message) {
    // Реализация показа ошибок
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #ff4444;
      color: white;
      padding: 10px 20px;
      border-radius: 4px;
      z-index: 1000;
    `;

    document.body.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
  }

  showSuccess(message) {
    // Реализация показа успешных сообщений
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    successDiv.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #00C851;
      color: white;
      padding: 10px 20px;
      border-radius: 4px;
      z-index: 1000;
    `;

    document.body.appendChild(successDiv);
    setTimeout(() => successDiv.remove(), 5000);
  }

  createLayout() {
    const app = document.getElementById('app');

    app.innerHTML = `
      <div class="wireframe">
        <div class="header">
          <div class="header-left">
            <div class="menu-icon">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div class="logo-placeholder"></div>
          </div>
          <div class="header-right">
            <div class="notification-icon">
              <svg class="bell-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M18 8C18 6.4087 17.3679 4.88258 16.2426 3.75736C15.1174 2.63214 13.5913 2 12 2C10.4087 2 8.88258 2.63214 7.75736 3.75736C6.63214 4.88258 6 6.4087 6 8C6 15 3 17 3 17H21C21 17 18 15 18 8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M13.73 21C13.5542 21.3031 13.3019 21.5547 12.9982 21.7295C12.6946 21.9044 12.3504 21.9965 12 21.9965C11.6496 21.9965 11.3054 21.9044 11.0018 21.7295C10.6982 21.5547 10.4458 21.3031 10.27 21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                ${this.getUnreadNotificationsCount() > 0 ? `
                  <circle class="notification-dot" cx="18" cy="6" r="3" fill="#FF3E3E"/>
                  <text x="18" y="8" text-anchor="middle" fill="white" font-size="8" font-weight="bold">${this.getUnreadNotificationsCount()}</text>
                ` : ''}
              </svg>
            </div>
          </div>
        </div>

        <div class="sidebar">
          <div class="sidebar-header">
            <div class="sidebar-title">Аналитический цент...</div>
            <div class="sidebar-subtitle">Онлайн</div>
          </div>

          <nav class="sidebar-menu">
            <div class="menu-section">
              <div class="menu-title">Меню</div>
              <ul class="menu-list">
                <li class="menu-item active">
                  <span class="menu-icon">📊</span>
                  <span class="menu-text">Городские проекты</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">📈</span>
                  <span class="menu-text">Как изменялся город</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">🎉</span>
                  <span class="menu-text">800 лет</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">📅</span>
                  <span class="menu-text">Афиша</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">🏙️</span>
                  <span class="menu-text">НашНижний</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">🔧</span>
                  <span class="menu-text">ПОС</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">📰</span>
                  <span class="menu-text">Медиалогия</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">🗺️</span>
                  <span class="menu-text">Карты</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">📢</span>
                  <span class="menu-text">Новости</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">💡</span>
                  <span class="menu-text">Инициативы</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">🗳️</span>
                  <span class="menu-text">Голосования</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">💬</span>
                  <span class="menu-text">Все комментарии</span>
                </li>
              </ul>
            </div>

            <div class="menu-section">
              <div class="menu-title">Администрирование</div>
              <ul class="menu-list">
                <li class="menu-item">
                  <span class="menu-icon">⚙️</span>
                  <span class="menu-text">Настройки</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">📚</span>
                  <span class="menu-text">Справочники</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">📊</span>
                  <span class="menu-text">Статистика</span>
                </li>
                <li class="menu-item">
                  <span class="menu-icon">📞</span>
                  <span class="menu-text">Обратная связь</span>
                </li>
              </ul>
            </div>
          </nav>

          <div class="sidebar-footer">
            <div class="user-info">
              <div class="user-avatar"></div>
              <div class="user-details">
                <div class="user-name">Администратор</div>
                <div class="user-role">Модератор</div>
              </div>
            </div>
          </div>
        </div>

        <div class="main-content">
          <div class="content-header">
            <h1>Панель модерации</h1>
          </div>

          <div class="applications-container" id="applicationsContainer">
            <!-- Applications will be rendered here -->
          </div>
        </div>

        <!-- Уведомления -->
        <div class="notifications-panel" id="notificationsPanel">
          <div class="notifications-header">
            <h3>Уведомления</h3>
            <div class="close-notifications" id="closeNotifications">×</div>
          </div>
          <div class="notifications-list" id="notificationsList">
            ${this.renderNotifications()}
          </div>
        </div>

        <!-- Всплывающее уведомление для заявки 122291 -->
        ${this.applications.find(app => app.id === '122291' && app.status === 'redirected') ? `
          <div class="floating-notification" id="floatingNotification">
            <div class="notification-header">
              <div class="notification-title">Заявка №122291 перенаправлена ИИ</div>
              <div class="close-notification" id="closeFloatingNotification">
                <div class="close-icon"></div>
              </div>
            </div>
            <div class="notification-body">
              Данная заявка не в нашей компетенции. За данную территорию отвечает ДУК Московского района Перенаправьте данную заявку туда.
            </div>
          </div>
        ` : ''}
      </div>
    `;
  }

  getUnreadNotificationsCount() {
    return this.notifications.filter(notification => !notification.read).length;
  }

  renderNotifications() {
    if (this.notifications.length === 0) {
      return '<div class="no-notifications">Нет новых уведомлений</div>';
    }

    return this.notifications.map(notification => `
      <div class="notification-item ${notification.read ? 'read' : 'unread'}" data-id="${notification.id}">
        <div class="notification-dot"></div>
        <div class="notification-content">
          <div class="notification-message">${notification.message}</div>
        </div>
      </div>
    `).join('');
  }

  renderApplications() {
    const container = document.getElementById('applicationsContainer');

    this.applications.forEach(app => {
      const applicationElement = this.createApplicationElement(app);
      container.appendChild(applicationElement);
    });
  }

  createApplicationElement(application) {
    const appElement = document.createElement('div');
    appElement.className = 'application-frame';
    appElement.style.top = `${application.position}px`;
    appElement.dataset.id = application.id;

    appElement.innerHTML = `
      <div class="application-content">
        <div class="application-number">Заявка номер №${application.id}</div>
        <div class="application-status status-${application.status}">
          ${this.getStatusText(application.status)}
        </div>
        <div class="application-date">Создано: ${this.getRandomDate()}</div>
      </div>
    `;

    return appElement;
  }

  getStatusText(status) {
    const statusTexts = {
      'moderation': 'Нужна модерация',
      'redirected': 'Перенаправлена ИИ',
      'approved': 'Одобрена',
      'rejected': 'Отклонена'
    };

    return statusTexts[status] || 'Неизвестный статус';
  }

  getRandomDate() {
    const start = new Date(2024, 0, 1);
    const end = new Date();
    const date = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
    return date.toLocaleDateString('ru-RU');
  }

  addEventListeners() {
    // Add click handlers for applications
    const applications = document.querySelectorAll('.application-frame');
    applications.forEach(app => {
      app.addEventListener('click', () => {
        this.handleApplicationClick(app.dataset.id);
      });
    });

    // Menu icon click handler
    const menuIcon = document.querySelector('.menu-icon');
    menuIcon.addEventListener('click', () => {
      this.toggleSidebar();
    });

    // Notification icon click handler
    const notificationIcon = document.querySelector('.notification-icon');
    notificationIcon.addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleNotificationsPanel();
    });

    // Close notifications panel
    const closeNotifications = document.getElementById('closeNotifications');
    if (closeNotifications) {
      closeNotifications.addEventListener('click', (e) => {
        e.stopPropagation();
        this.closeNotificationsPanel();
      });
    }

    // Close floating notification
    const closeFloatingNotification = document.getElementById('closeFloatingNotification');
    if (closeFloatingNotification) {
      closeFloatingNotification.addEventListener('click', () => {
        this.closeFloatingNotification();
      });
    }

    // Notification items click handlers
    const notificationItems = document.querySelectorAll('.notification-item');
    notificationItems.forEach(item => {
      item.addEventListener('click', () => {
        this.handleNotificationClick(item.dataset.id);
      });
    });

    // Close notifications when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.notifications-panel') && !e.target.closest('.notification-icon')) {
        this.closeNotificationsPanel();
      }
    });

    // Menu items click handlers
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
      item.addEventListener('click', () => {
        menuItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');
      });
    });
  }

  setupScroll() {
    let lastScrollTop = 0;
    const header = document.querySelector('.header');

    window.addEventListener('scroll', () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

      if (scrollTop > lastScrollTop && scrollTop > 100) {
        header.classList.add('header-hidden');
      } else {
        header.classList.remove('header-hidden');
      }

      lastScrollTop = scrollTop;
    });
  }

  handleApplicationClick(applicationId) {
    console.log('Application clicked:', applicationId);
    this.navigateToApplicationDetail(applicationId);
  }

  handleNotificationClick(notificationId) {
    const notification = this.notifications.find(n => n.id == notificationId);
    if (notification) {
      notification.read = true;
      this.updateNotificationsUI();
      this.navigateToApplicationDetail(notification.applicationId);
    }
  }

  toggleNotificationsPanel() {
    const panel = document.getElementById('notificationsPanel');
    panel.classList.toggle('active');
  }

  closeNotificationsPanel() {
    const panel = document.getElementById('notificationsPanel');
    panel.classList.remove('active');
  }

  closeFloatingNotification() {
    const floatingNotification = document.getElementById('floatingNotification');
    if (floatingNotification) {
      floatingNotification.style.display = 'none';
    }
  }

  updateNotificationsUI() {
    const notificationsList = document.getElementById('notificationsList');
    const notificationIcon = document.querySelector('.notification-icon');

    if (notificationsList) {
      notificationsList.innerHTML = this.renderNotifications();
    }

    // Update notification dot
    const bellIcon = document.querySelector('.bell-icon');
    const existingDot = bellIcon.querySelector('.notification-dot');
    const existingText = bellIcon.querySelector('text');

    if (existingDot) existingDot.remove();
    if (existingText) existingText.remove();

    const unreadCount = this.getUnreadNotificationsCount();
    if (unreadCount > 0) {
      bellIcon.innerHTML += `
        <circle class="notification-dot" cx="18" cy="6" r="3" fill="#FF3E3E"/>
        <text x="18" y="8" text-anchor="middle" fill="white" font-size="8" font-weight="bold">${unreadCount}</text>
      `;
    }
  }

  navigateToApplicationDetail(applicationId) {
    window.location.href = `application-detail.html?id=${applicationId}`;
  }

  toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('sidebar-collapsed');
  }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new ModerationDashboard();
});