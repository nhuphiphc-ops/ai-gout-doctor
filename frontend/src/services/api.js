import axios from 'axios';

// Use relative path for API requests (Vite proxy handles it in development, Nginx in production)
const API_URL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL: API_URL,
});

// Request interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const apiService = {
  // Authentication
  loginGoogle: async (idToken) => {
    const response = await api.post('/api/auth/google', { id_token: idToken });
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  loginMock: async () => {
    const response = await api.post('/api/auth/mock');
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  },

  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // User Profile
  getProfile: async () => {
    const response = await api.get('/api/user/profile');
    return response.data;
  },

  updateProfile: async (profileData) => {
    const response = await api.put('/api/user/profile', profileData);
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  },

  uploadAvatar: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/user/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    const user = apiService.getCurrentUser();
    if (user) {
      user.avatar_url = response.data.avatar_url;
      localStorage.setItem('user', JSON.stringify(user));
    }
    return response.data;
  },

  // Logs
  getTodayLog: async () => {
    const response = await api.get('/api/logs/today');
    return response.data;
  },

  submitMorningLog: async (logData) => {
    const response = await api.post('/api/logs/morning', logData);
    return response.data;
  },

  submitAfternoonLog: async (logData) => {
    const response = await api.post('/api/logs/afternoon', logData);
    return response.data;
  },

  getHistoryLogs: async (limit = 100, offset = 0) => {
    const response = await api.get('/api/logs/history', {
      params: { limit, offset },
    });
    return response.data;
  },

  // Analytics
  getDashboardData: async (view = 'week') => {
    const response = await api.get('/api/analytics/dashboard', {
      params: { view },
    });
    return response.data;
  },

  getCorrelations: async (days = 30) => {
    const response = await api.get('/api/analytics/correlation', {
      params: { days },
    });
    return response.data;
  },

  getGoogleFitUrl: async () => {
    const response = await api.get('/api/auth/google-fit/url');
    return response.data;
  },

  syncSteps: async () => {
    const response = await api.post('/api/user/sync-steps');
    return response.data;
  },

  // Export URLs (helper to get download url)
  getExportUrl: (format) => {
    const token = localStorage.getItem('auth_token') || '';
    return `${API_URL}/api/export/${format}?token=${token}`;
  },

  // Medical Checkups
  getMedicalCheckups: async () => {
    const response = await api.get('/api/medical-checkups');
    return response.data;
  },
  
  createMedicalCheckup: async (data) => {
    const response = await api.post('/api/medical-checkups', data);
    return response.data;
  },
  

  // Video Script Generator
  generateVideoScript: async (data) => {
    const response = await api.post('/api/video-script/generate', data);
    return response.data;
  },
  
  // AI Chat
  sendChatMessage: async (message, history) => {
    const response = await api.post('/api/chat', { message, history });
    return response.data;
  }
};
export default apiService;
