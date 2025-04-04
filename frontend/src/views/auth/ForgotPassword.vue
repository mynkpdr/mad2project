<template>
    <section class="d-flex align-items-start justify-content-center py-4">
        <div class="card p-3 rounded-2" style="max-width: 430px; width: 100%;">
            <div class="card-body">
                <h3 class="text-center mb-4">Forgot Password?</h3>
                <form @submit.prevent="handleSubmit">
                    <div class="form-floating mb-3">
                        <input type="email" class="form-control" id="email" placeholder="name@example.com" 
                            v-model="email" required>
                        <label for="email" class="mb-4 text-secondary">Email</label>
                    </div>
                    <div class="d-grid">
                        <button class="btn btn-primary btn-sm fs-6 fw-light" style="height:50px" :disabled="loading">
                            {{ loading ? 'Sending...' : 'Send Reset Link' }}
                        </button>
                    </div>
                </form>
                <p v-if="message" :class="['message mt-3 text-center', messageClass]">{{ message }}</p>
                <div class="text-center mt-3">
                    <span class="text-secondary">Remember your password? 
                        <router-link :to="{ 'name': 'Login' }" class="text-primary link-underline link-underline-opacity-0 link-underline-opacity-100-hover fw-light">Login</router-link>
                    </span>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const email = ref("");
const loading = ref(false);
const message = ref("");
const messageClass = ref('');

const sendResetLink = async () => {
    loading.value = true;
    try {
        const response = await axios.post('/api/auth/forgot-password', { email: email.value });
        message.value = response.data.message;
        messageClass.value = 'text-success';
    } catch (error) {
        message.value = error.response?.data?.message || "Something went wrong.";
        messageClass.value = 'text-danger';
    } finally {
        loading.value = false;
    }
};

const handleSubmit = () => {
    sendResetLink();
};
</script>

<style scoped>
.message {
    padding: 10px;
    border-radius: 4px;
}
.form-floating > label::after {
    background-color: transparent !important;
}

.btn {
  border: 1px solid #CACACA !important;
  border-radius: 0.375rem;
}
</style>
