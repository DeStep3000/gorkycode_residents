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
          <div class="menu-icon">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <div class="logo-placeholder"></div>
          <div class="header-actions">
            <button class="btn btn-back">← Назад к списку</button>
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
            <div class="application-header-card">
              <div class="card-header">
                <span class="card-title">Карточка сообщения</span>
                <div class="application-id">
                  <span class="id-label">Id</span>
                  <div class="id-value">${this.applicationId}</div>
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

          <div class="history-container">
            <div class="history-header">
              <div class="history-column date-column">Дата</div>
              <div class="history-column author-column">Автор</div>
              <div class="history-column changes-column">Изменено</div>
            </div>
            
            <div class="history-items" id="historyItems">
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
            from: { label: 'Остановлено ИИ', color: '#FEB049' },
            to: { label: 'На модерации', color: '#FEB049' }
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
            from: { label: 'Остановлено ИИ', color: '#FEB049' },
            to: { label: 'Взято в работу ответственным', color: '#006ABC' }
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
            from: { label: 'Остановлено ИИ', color: '#FEB049' },
            to: { label: 'Назначено ответственному', color: '#006ABC' }
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
            from: { label: 'Остановлено ИИ', color: '#FEB049' },
            to: { label: 'Перенаправлено ИИ', color: '#04BD23' }
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
    historyElement.className = 'history-item';
    
    const changesHTML = item.changes.map(change => {
      if (change.type === 'status') {
        return `
          <div class="change-row">
            <div class="change-label">Статус</div>
            <div class="status-badge" style="background: ${change.from.color}">${change.from.label}</div>
            <div class="change-arrow">=></div>
            <div class="status-badge" style="background: ${change.to.color}">${change.to.label}</div>
          </div>
        `;
      } else if (change.type === 'assigned') {
        return `
          <div class="change-row">
            <div class="change-label">Назначено</div>
            <div class="assigned-value">${change.from}</div>
            <div class="change-arrow">=></div>
            <div class="assigned-value">${change.to}</div>
          </div>
        `;
      }
      return '';
    }).join('');

    historyElement.innerHTML = `
      <div class="history-item-background">
        <div class="history-date">${item.date}</div>
        <div class="history-author">${item.author}</div>
        <div class="history-changes">
          ${changesHTML}
        </div>
      </div>
    `;

    return historyElement;
  }

  addEventListeners() {
    // Back button
    const backButton = document.querySelector('.btn-back');
    backButton.addEventListener('click', () => {
      this.goBackToList();
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

    // Menu icon
    const menuIcon = document.querySelector('.menu-icon');
    menuIcon.addEventListener('click', () => {
      this.toggleSidebar();
    });

    // Menu items
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
      item.addEventListener('click', () => {
        menuItems.forEach(i => i.classList.remove('active'));
        item.classList.add('active');
      });
    });
  }

  goBackToList() {
    // Here you would typically navigate back to the list view
    // For now, we'll just reload the page to show the list
    window.location.reload();
  }

  switchTab(tabName) {
    console.log('Switching to tab:', tabName);
    // Implement tab switching logic here
  }

  toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('sidebar-collapsed');
  }
}

// Initialize application detail when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Get application ID from URL or other source
  const urlParams = new URLSearchParams(window.location.search);
  const applicationId = urlParams.get('id') || '123456';
  
  new ApplicationDetail(applicationId);
});