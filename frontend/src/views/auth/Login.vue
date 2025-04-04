<template>
  <section class="d-flex align-items-center justify-content-center py-4">
    <div class="card p-4 rounded-2" style="max-width: 430px; width: 100%;">
      <div class="card-body">
        <h3 class="text-center mb-4">Login</h3>
        <form @submit.prevent="handleLogin('regular')">
          <div class="form-floating mb-3">
            <input type="email" class="form-control" id="email" placeholder="name@example.com" 
              v-model="loginEmail" required>
            <label for="email" class="text-secondary">Email</label>
          </div>
          <div class="form-floating mb-3">
            <input :type="showPassword ? 'text' : 'password'" class="form-control" 
              id="password" placeholder="Password" v-model="loginPassword" required minlength="8">
            <label for="password" class="text-secondary">Password</label>
            <i :class="showPassword ? 'bi bi-eye-fill' : 'bi bi-eye-slash-fill'"
              class="position-absolute top-50 end-0 translate-middle-y me-3 text-secondary"
              style="cursor: pointer; z-index: 5;"
              @click="togglePassword"></i>
          </div>
          <div class="text-center mb-3">
            <router-link :to="{ 'name': 'ForgotPassword' }" class="text-primary link-underline link-underline-opacity-0 link-underline-opacity-100-hover fw-light small">Forgot password?</router-link>
          </div>
          <div class="d-grid">
            <button class="btn btn-primary btn-sm fs-6 fw-light" style="height:50px">Login</button>
          </div>
        </form>
        <div class="text-center mt-3">
          <span class="text-secondary small">Don't have an account? 
            <router-link :to="{ 'name': 'Signup' }" class="text-primary link-underline link-underline-opacity-0 link-underline-opacity-100-hover fw-light">Signup</router-link>
          </span>
        </div>

        <div class="position-relative my-4">
          <hr class="text-secondary">
          <span class="span-line position-absolute top-50 start-50 translate-middle px-3 text-secondary">Or</span>
        </div>

        <div class="d-grid gap-2">
            <a href="#" class="btn btn-facebook position-relative text-white btn-sm fs-6 fw-light d-flex align-items-center my-2" style="height:50px;" @click="loginWithFacebook">
              <i class="bi bi-facebook position-absolute start-0 ms-3 facebook-icon"></i>
              <span class="mx-auto">Login with Facebook</span>
            </a>
          <a href="#" @click.prevent="loginWithGoogle" class="btn position-relative text-secondary btn-sm fs-6 d-flex align-items-center my-2" style="height:50px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/32px-Google_%22G%22_logo.svg.png"
              alt="Google" class="position-absolute start-0 ms-3" style="width: 20px;">
            <span class="mx-auto">Login with Google</span>
          </a>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from '@/store/user';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { googleTokenLogin } from 'vue3-google-login'
import { push } from "notivue";
const showPassword = ref(false);
const loginEmail = ref("");
const loginPassword = ref("");

const router = useRouter();
const userStore = useUserStore();

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

const handleLogin = async (loginType) => {
  try {
    let response;
    // Regular Login
    if (loginType === "regular") {
      response = await axios.post('/api/auth/login', {
        email: loginEmail.value,
        password: loginPassword.value,
      });
    }
    // Google Login
    else if (loginType.access_token) {
      const access_token = loginType.access_token;
      response = await axios.post('/api/auth/login/google', { access_token });
    }
    // Facebook Login
    else if (loginType.accessToken) {
      const facebookToken = loginType.accessToken;
      response = await axios.post('/api/auth/login/facebook', { facebookToken });
    }

    const { access_token, user } = response.data;

    // Store user data and token
    userStore.setUserData(user);
    userStore.setToken(access_token);

    // Show success message and redirect
    push.success("Login Successful!")
    if (user.role.toLowerCase() === 'admin') {
      await router.push({ name: 'AdminDashboard' });
    } else {
      await router.push({ name: 'Home' });
    }
  } catch (error) {
    throw error;
  }
};

const loginWithFacebook = () => {
  window.FB.login((response) => {
    if (response.authResponse) {
      handleLogin(response.authResponse);
    } else {
      console.log("User cancelled login or did not fully authorize.");
    }
  }, { scope: 'email' });
  return false;
};

const loginWithGoogle = async () => {
  try {
    // Fetch the access token using the googleTokenLogin method
    const response = await googleTokenLogin();
    handleLogin(response);
  } catch (error) {
    throw error
  }
};


// Initialize Facebook SDK
const initFacebook = () => {
  window.fbAsyncInit = function () {
    window.FB.init({
      appId: "1276923853358149",
      cookie: true,
      xfbml: true,
      version: "v21.0",
    });
  };
};

// Load Facebook SDK script
const loadFacebookSDK = (d, s, id) => {
  const fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) {
    return;
  }
  const js = d.createElement(s);
  js.id = id;
  js.src = "https://connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
};

onMounted(() => {
  initFacebook();
  loadFacebookSDK(document, "script", "facebook-jssdk");
});
</script>

<style scoped>
.form-floating > label::after {
  background-color: transparent !important;
}

.btn-facebook {
  background-color: #4267b2;
}

.btn-facebook:hover {
  background-color: #375694;
}

.facebook-icon {
  font-size: 1.25rem;
}

.btn {
  border: 1px solid #CACACA !important;
  border-radius: 0.375rem;
}

.night-mode .span-line {
  background-color: #161a2d !important;
}
.span-line {
  background-color: #fff;
}

</style>