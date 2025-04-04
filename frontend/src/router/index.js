import { createRouter, createWebHistory } from "vue-router";
import { jwtDecode } from 'jwt-decode';
import { useUserStore } from "@/store/user";

import axios from "axios";

import auth_routes from "@/router/auth_routes";
import main_routes from "@/router/main_routes";
import admin_routes from "@/router/admin_routes";
import student_routes from "@/router/student_routes";
import user_routes from "./user_routes";
import { push } from "notivue";

const routes = [
  ...main_routes,
  ...auth_routes,
  ...student_routes,
  ...admin_routes,
  ...user_routes
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    } else if (savedPosition) {
      return savedPosition;
    }
    // Always scroll to top
    return { top: 0 };
  },
});

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();

  try {
    // Check if the route requires authentication
    if (to.meta.requiresAuth) {
      // If the user is not authenticated
      if (!userStore.isAuthenticated) {
        push.error('You are not authenticated. Please log in.')
        return next({ "name": "Login" });
      }

      // If authenticated but user data is missing
      if (!userStore.userData.id) {
        // Check if the user_token exists in localStorage (or sessionStorage)
        const response = await axios.post('/api/users/user_token');
        const user_token = response.data
        if (user_token) {
          try {
            // Decode the user_token and get the user data
            const decoded = jwtDecode(user_token);
            userStore.setUserData(decoded.sub); // Set user data in store
          } catch (error) {
            console.error('Error decoding user_token:', error);
            userStore.logout(); // Clear user data if user_token decoding fails
            push.error('Session expired. Please log in again')
            return next({ 'name': "Login" });
          }
        }
      }
    }
    if (to.meta.requiresAdmin) {
      // Check if the user is an admin
      if (!userStore.isAdmin) {
        push.error('You do not have permission to access this page')
        return next({ name: 'Home' }); // Redirect to dashboard or any other route
      }
    }

    // Prevent authenticated users from accessing login or signup pages
    if (userStore.isAuthenticated && (to.name === 'Login' || to.name === 'Signup')) {
      push.error('You are already authenticated')
      return next('/'); // Redirect to home
    }

    // Proceed to the requested route if all checks pass
    next();
  } catch (error) {
    console.error('Error during route validation:', error);

    // Handle cases where the token is invalid or user data fetch fails
    if (error.response?.status === 401 || error.response?.status === 403) {
      userStore.logout(); // Clear user data and token
      push.error('Your session has expired. Please log in again')
      return next('/login');
    }

    next('/error');
  }
});

export default router;
