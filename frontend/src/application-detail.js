import './style.css';

class ApplicationDetail {
  constructor(applicationId) {
    this.applicationId = applicationId;
    this.historyData = this.generateHistoryData();
    this.init();
  }

  init() {
    this.createLayout();
    this.renderHistory();
    this.addEventListeners();
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
            <div class="sidebar-subtitle">Онлайн</div>
          </div>

          <nav class="sidebar-menu">
            <div class="menu-section">
              <div class="menu-title">Меню</div>
              <ul class="menu-list">
                <li class="menu-item">
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
            <h1>Сообщения</h1>
            <div class="application-header-card">
              <div class="card-title">Карточка сообщения</div>
              <div class="id-section">
                <span class="id-label">Id</span>
                <div class="id-input-container">
                  <span class="id-value">${this.applicationId}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="application-tabs">
            <div class="tabs-container">
              <div class="tab">Подробно</div>
              <div class="tab">Адрес</div>
              <div class="tab">Комментарии (0)</div>
              <div class="tab">Обработка</div>
              <div class="tab active">История изменений</div>
            </div>
          </div>

          <div class="history-table">
            <div class="table-header">
              <div class="table-header-cell">Дата</div>
              <div class="table-header-cell">Автор</div>
              <div class="table-header-cell">Изменено</div>
            </div>

            <div class="table-body" id="historyItems">
              <!-- History items will be rendered here -->
            </div>
          </div>
        </div>
      </div>
    `;
  }

  generateHistoryData() {
    return [
      {
        id: 1,
        date: '2025-11-12 15:42:45',
        author: 'Аналитический центр города',
        changes: [
          {
            type: 'status',
            from: { label: 'Остановлено ИИ', colorClass: 'orange' },
            to: { label: 'На модерации', colorClass: 'orange' }
          },
          {
            type: 'assigned',
            from: 'ИИ',
            to: 'ИИ'
          }
        ]
      },
      {
        id: 2,
        date: '2025-11-12 15:42:45',
        author: 'Аналитический центр города',
        changes: [
          {
            type: 'status',
            from: { label: 'Остановлено ИИ', colorClass: 'orange' },
            to: { label: 'Взято в работу ответственным', colorClass: 'blue' }
          },
          {
            type: 'assigned',
            from: 'ИИ',
            to: 'Администрация Нижегородского района'
          }
        ]
      },
      {
        id: 3,
        date: '2025-11-12 15:42:45',
        author: 'Аналитический центр города',
        changes: [
          {
            type: 'status',
            from: { label: 'Остановлено ИИ', colorClass: 'orange' },
            to: { label: 'Назначено ответственному', colorClass: 'blue' }
          },
          {
            type: 'assigned',
            from: 'ИИ',
            to: 'Администрация Нижегородского района'
          }
        ]
      },
      {
        id: 4,
        date: '2025-11-12 15:42:45',
        author: 'Аналитический центр города',
        changes: [
          {
            type: 'status',
            from: { label: 'Остановлено ИИ', colorClass: 'orange' },
            to: { label: 'Перенаправлено ИИ', colorClass: 'green' }
          },
          {
            type: 'assigned',
            from: 'ИИ',
            to: 'ИИ'
          }
        ]
      }
    ];
  }

  renderHistory() {
    const container = document.getElementById('historyItems');

    this.historyData.forEach(item => {
      const historyElement = this.createHistoryElement(item);
      container.appendChild(historyElement);
    });
  }

  createHistoryElement(item) {
    const historyElement = document.createElement('div');
    historyElement.className = 'table-row';

    historyElement.innerHTML = `
      <div class="table-cell date-cell">
        <div class="date-time">
          <div class="date-part">${item.date.split(' ')[0]}</div>
          <div class="time-part">${item.date.split(' ')[1]}</div>
        </div>
      </div>
      <div class="table-cell author-cell">
        ${item.author}
      </div>
      <div class="table-cell changes-cell">
        <div class="changes-content">
          ${item.changes.map(change => this.createChangeBlock(change)).join('')}
        </div>
      </div>
    `;

    return historyElement;
  }

  createChangeBlock(change) {
    if (change.type === 'status') {
      return `
        <div class="change-block status-block">
          <div class="change-row">
            <span class="change-label">Статус</span>
            <div class="status-combination">
              <div class="status-badge ${change.from.colorClass}">${change.from.label}</div>
              <span class="change-arrow">=></span>
              <div class="status-badge ${change.to.colorClass}">${change.to.label}</div>
            </div>
          </div>
        </div>
      `;
    } else if (change.type === 'assigned') {
      return `
        <div class="change-block assignment-block">
          <div class="change-row">
            <span class="change-label">Назначено</span>
            <div class="assignment-combination">
              <span class="assigned-value">${change.from}</span>
              ${change.from !== change.to ? `<span class="change-arrow">=></span><span class="assigned-value">${change.to}</span>` : ''}
            </div>
          </div>
        </div>
      `;
    }
    return '';
  }

  addEventListeners() {
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

    // Tabs
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        this.switchTab(tab.textContent);
      });
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

  switchTab(tabName) {
    console.log('Switching to tab:', tabName);
    // Implement tab switching logic here
  }

  handleNotificationClick() {
    console.log('Notification icon clicked - feature not implemented');
    const notification = document.querySelector('.notification-icon');
    notification.classList.add('notification-pulse');
    setTimeout(() => {
      notification.classList.remove('notification-pulse');
    }, 500);
  }

  toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('sidebar-collapsed');
  }

  setupScroll() {
      let lastScrollTop = 0;
      const header = document.querySelector('.header');

      window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 50) {
          // При скролле добавляем компактный стиль
          header.classList.add('header-scrolled');
        } else {
          // В верхней части страницы - обычный стиль
          header.classList.remove('header-scrolled');
        }

        lastScrollTop = scrollTop;
      });
    }
}

// Initialize application detail when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Get application ID from URL or other source
  const urlParams = new URLSearchParams(window.location.search);
  const applicationId = urlParams.get('id') || '123456';
  
  new ApplicationDetail(applicationId);
});