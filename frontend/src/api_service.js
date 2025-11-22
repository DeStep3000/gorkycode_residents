class ApiService {
  constructor() {
    this.baseUrl = 'http://localhost:8080';
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Получить список жалоб
  async getComplaints(limit = 50, offset = 0) {
    return this.request(`/complaints?limit=${limit}&offset=${offset}`);
  }

  // Получить конкретную жалобу
  async getComplaint(complaintId) {
    return this.request(`/complaints/${complaintId}`);
  }

  // Получить статусы жалобы
  async getComplaintStatuses(complaintId) {
    return this.request(`/statuses?complaint_id=${complaintId}`);
  }

  // Получить статусы по шаблону
  async getStatusesByTemplate(templateId = 1) {
    return this.request(`/statuser/?template_id=${templateId}`);
  }

  // Обновить статус жалобы
  async updateComplaintStatus(complaintId, statusData) {
    return this.request(`/complaints/${complaintId}`, {
      method: 'PUT',
      body: JSON.stringify(statusData),
    });
  }
}

export default new ApiService();