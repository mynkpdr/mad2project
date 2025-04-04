<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow-sm">
                    <div class="card-body text-center">
                        <h3 class="card-title">Confirm Email</h3>
                        <p v-if="loading" class="text-primary">Verifying your email...</p>
                        <p v-if="message && error" class="text-danger">{{ message }}</p>
                        <p v-if="message && !error" class="text-success">{{ message }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute } from "vue-router";
import router from "../../router";
import { push } from "notivue";

const loading = ref(true);
const message = ref("");
const error = ref(false);
const route = useRoute();

const confirmEmail = async () => {
    const token = route.params.token; // Get token from route params
    try {
        const response = await axios.get(`/api/auth/confirm-email/${token}`);
        message.value = response.data.message;
        await new Promise(resolve => setTimeout(resolve, 1000));
        error.value = false;
        push.success("Email successfully confirmed. You can now login.");
        router.push({ name: 'Login' });
    } catch (e) {
        error.value = true;
        message.value = e.response
            ? e.response.data.message
            : "An error occurred.";
        throw e
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    confirmEmail(); // Confirm email when component is mounted
});


</script>