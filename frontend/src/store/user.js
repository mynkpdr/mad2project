import { defineStore } from 'pinia';
import { googleLogout } from "vue3-google-login";
import axios from 'axios';

export const useUserStore = defineStore('user', {
    state: () => ({
        userData: JSON.parse(localStorage.getItem('userData')) || {
            "id": null,
            "username": null,
            "name": null,
            "email": null,
            "profile_picture": null,
            "role": null
        },
        access_token: localStorage.getItem('access_token') || '',
    }),
    getters: {
        isAuthenticated: (state) => !!state.access_token,
        isAdmin: (state) => state.userData.role === 'Admin',
    },
    actions: {
        setUserData(user) {
            this.userData = {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "profile_picture": user.profile_picture,
                "role": user.role
            };
            localStorage.setItem('userData', JSON.stringify(user));
        },
        setToken(access_token) {
            this.access_token = access_token;
            localStorage.setItem('access_token', access_token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
        },
        logout() {
            googleLogout()
            this.userData = {};
            this.access_token = '';
            localStorage.removeItem('access_token');
            localStorage.removeItem('userData');
            delete axios.defaults.headers.common['Authorization'];
        },
    },
});
