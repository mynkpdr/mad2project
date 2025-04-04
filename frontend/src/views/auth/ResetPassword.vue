<template>
    <section class="d-flex align-items-center justify-content-center py-4">
        <div class="card p-4 rounded-2" style="max-width: 430px; width: 100%;">
            <div class="card-body">
                <h3 class="text-center mb-4">Reset Password</h3>
                <form @submit.prevent="resetPassword">
                    <div class="form-floating mb-3">
                        <input :type="showPassword ? 'text' : 'password'" class="form-control" id="new-password"
                            placeholder="Password" v-model="newPassword" required minlength="8">
                        <label for="new-password" class="text-secondary">New Password</label>
                        <i :class="showPassword ? 'bi bi-eye-fill' : 'bi bi-eye-slash-fill'"
                            class="position-absolute top-50 end-0 translate-middle-y me-3 text-secondary"
                            style="cursor: pointer; z-index: 5;" @click="togglePassword"></i>
                    </div>
                    <div class="form-floating mb-3">
                        <input :type="showPassword ? 'text' : 'password'" class="form-control" id="confirm_password"
                            placeholder="Confirm Password" v-model="confirmPassword" required minlength="8">
                        <label for="confirm_password" class="text-secondary">Confirm Password</label>
                    </div>
                    <div class="d-grid">
                        <button :disabled="loading || !(newPassword == confirmPassword) " class="btn btn-primary btn-sm fs-6 fw-light" style="height:50px">{{
                            loading ? 'Resetting...' : 'Reset Password' }}</button>
                    </div>
                </form>
                <p v-if="message" :class="messageClass" style="font-size: 12px;">{{ message }}</p>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { push } from "notivue";
import router from "../../router";

const route = useRoute();
const token = route.params.token;
const newPassword = ref("");
const confirmPassword = ref("");
const loading = ref(false);
const message = ref("");
const messageClass = ref('');
const showPassword = ref(false);
const togglePassword = () => {
    showPassword.value = !showPassword.value;
};
const resetPassword = async () => {
    loading.value = true;
    try {
        const response = await axios.post(`/api/auth/reset-password/${token}`,
            { new_password: newPassword.value }
        );
        message.value = response.data.message;
        messageClass.value = 'text-success';
        push.success("Password successfully reset. You can now login.");
        router.push({ name: 'Login' });
    } catch (error) {
        message.value = error.response?.data?.message || "Something went wrong.";
        messageClass.value = 'text-danger';
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
.form-floating>label::after {
    background-color: transparent !important;
}

.btn {
    border: 1px solid #CACACA !important;
    border-radius: 0.375rem;
}
</style>