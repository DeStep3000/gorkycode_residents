import './style.css';

class ModerationDashboard {
  constructor() {
    this.applications = [
      { id: '122739', status: 'moderation', position: 210 },
      { id: '122738', status: 'moderation', position: 87 },
      { id: '123003', status: 'moderation', position: 333 },
      { id: '122711', status: 'moderation', position: 579 },
      { id: '122710', status: 'moderation', position: 456 },
      { id: '122291', status: 'moderation', position: 702 },
      { id: '123456', status: 'moderation', position: 948 },
      { id: '122555', status: 'moderation', position: 825 }
    ];

    this.init();
  }

  init() {
    this.createLayout();
    this.renderApplications();
    this.addEventListeners();
    this.setupScroll();
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
                <circle class="notification-dot" cx="18" cy="6" r="3" fill="#ff4444"/>
              </svg>
            </div>
          </div>
        </div>

        <div class="sidebar">
          <div class="sidebar-header">
            <div class="sidebar-title">Аналитический цент...</div>
            <div class="sidebar-subtitle">Силайн</div>
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
      </div>
    `;
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
    // Add click handlers for applications - entire card is clickable
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
      this.handleNotificationClick();
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
        // Scrolling down
        header.classList.add('header-hidden');
      } else {
        // Scrolling up
        header.classList.remove('header-hidden');
      }

      lastScrollTop = scrollTop;
    });
  }

  handleApplicationClick(applicationId) {
    console.log('Application clicked:', applicationId);
    this.navigateToApplicationDetail(applicationId);
  }

  handleNotificationClick() {
    console.log('Notification icon clicked - feature not implemented');
    const notification = document.querySelector('.notification-icon');
    notification.classList.add('notification-pulse');
    setTimeout(() => {
      notification.classList.remove('notification-pulse');
    }, 500);
  }

  navigateToApplicationDetail(applicationId) {
    window.location.href = `application-detail.html?id=${applicationId}`;
  }

  toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const menuIcon = document.querySelector('.menu-icon');
    sidebar.classList.toggle('sidebar-collapsed');
    menuIcon.classList.toggle('menu-icon-close');
  }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new ModerationDashboard();
});