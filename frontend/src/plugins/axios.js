// src/plugins/axios.js 
import axios from 'axios';

// Request interceptor
axios.interceptors.request.use(
    (config) => {
        // Window global variable থেকে token নেওয়া
        const token = window.accessToken;

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        // Content-Type automatically set হয়, কিন্তু explicit ভালো
        if (!(config.data instanceof FormData)) {
            config.headers['Content-Type'] = 'application/json';
        }

        config.headers['Accept'] = 'application/json';

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor
axios.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        // Error handling
        if (error.response?.status === 401) {
            console.error('Authentication failed - Redirect to login');
            // আপনার login page এ redirect করুন
            window.location.href = '/login/';
        }
        return Promise.reject(error);
    }
);

export default axios;