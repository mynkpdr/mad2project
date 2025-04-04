import { computed, createApp } from 'vue'
import { createPinia } from 'pinia'
import { createNotivue } from 'notivue';
import { push } from 'notivue';
import 'notivue/notification.css'
import 'notivue/animations.css'
import 'notivue/notification-progress.css'
import App from './App.vue'
import router from "./router";
import vue3GoogleLogin from 'vue3-google-login'
import axios from "axios";

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css';

const notivue = createNotivue({
    notifications: {
        global: {
            duration: 3000
        }
    },
    position: 'bottom-right', // Default position
    darkTheme: true
})
const pinia = createPinia()
const app = createApp(App);
app.use(pinia)
app.use(router);
app.use(vue3GoogleLogin, {
    clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID
})
app.use(notivue);

// app.config.errorHandler = (error) => {
//     console.error(error);
//     const message = error?.response?.data?.message || "An unexpected error occurred";
//     push.error(message);
// };

app.config.globalProperties.backendUrl = computed(() =>
    import.meta.env.VITE_CDN_URL + import.meta.env.VITE_STATIC_FOLDER
);

app.config.globalProperties.staticSrc = computed(() =>
    import.meta.env.VITE_CDN_URL + import.meta.env.VITE_STATIC_FOLDER
);

app.config.globalProperties.profilePictureSrc = computed(() =>
    import.meta.env.VITE_CDN_URL + import.meta.env.VITE_PROFILE_PICTURE_UPLOAD_FOLDER
);

app.config.globalProperties.questionImageSrc = computed(() =>
    import.meta.env.VITE_CDN_URL + import.meta.env.VITE_QUESTION_IMAGE_UPLOAD_FOLDER
);

// Setup Axios
axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL
axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`
axios.interceptors.response.use(function (response) {
    return response;
}, function (error) {
    const message = error?.response?.data?.message || "Axios Network error";
    push.error(message);
    return Promise.reject(error);
});
app.mount("#app");
