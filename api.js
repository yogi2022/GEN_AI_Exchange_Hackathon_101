
// utils/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiCall = async (endpoint, method = 'GET', data = null) => {
  const token = localStorage.getItem('auth_token');

  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  if (data && method !== 'GET') {
    config.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

export const uploadFile = async (endpoint, file) => {
  const token = localStorage.getItem('auth_token');
  const formData = new FormData();
  formData.append('file', file);

  const config = {
    method: 'POST',
    headers: {},
    body: formData
  };

  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error('File upload failed:', error);
    throw error;
  }
};
