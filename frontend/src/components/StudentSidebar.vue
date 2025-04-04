<template>
    <div v-if="userStore.isAuthenticated && userStore.userData.role.toLowerCase() == 'student'" class="col-md-2 h-100">
        <ConfirmationModal :visible="isModalVisible" :message="modalMessage" @close="closeModal"
            @confirm="handleConfirm" />
        <div class="card mb-4">
            <div class="card-header">
                <h5 class="card-title mb-0 fw-bold">Student Portal</h5>
                <span class="fs-6 text-warning" v-if="props.pending_result">( Pending Results )</span>
            </div>
            <div class="card-body p-0">
                <div class="list-group">
                    <router-link :to="{ name: 'StudentDashboard' }"
                        class="list-group-item list-group-item-action border-0 py-3 px-4">
                        <i class="bi bi-speedometer2 me-3"></i>
                        <span>Dashboard</span>
                    </router-link>
                    <router-link :to="{ name: 'StudentMyQuizzes' }"
                        class="list-group-item list-group-item-action border-0 py-3 px-4">
                        <i class="bi bi-clipboard-check me-3"></i>
                        <span>My Quizzes</span>
                    </router-link>
                    <router-link :to="{ name: 'StudentProfile' }"
                        class="list-group-item list-group-item-action border-0 py-3 px-4">
                        <i class="bi bi-person me-3"></i>
                        <span>Profile</span>
                    </router-link>
                    <router-link :to="{ name: 'StudentSettings' }"
                        class="list-group-item list-group-item-action border-0 py-3 px-4">
                        <i class="bi bi-gear me-3"></i>
                        <span>Settings</span>
                    </router-link>
                    <button @click.prevent="openModal"
                        class="list-group-item list-group-item-action border-0 py-3 px-4 text-danger">
                        <i class="bi bi-box-arrow-right me-3"></i>
                        <span>Logout</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
    <div v-else-if="userStore.isAuthenticated && userStore.userData.role.toLowerCase() == 'admin'" class="col-md-2">
        <div class="card mb-4">
            <div class="card-body p-0">
                <div class="list-group">
                    <router-link :to="{ name: 'AdminStudentProfile' }"
                        class="list-group-item list-group-item-action border-0 py-3 px-4">
                        <i class="bi bi-person me-3"></i>
                        <span>Profile</span>
                    </router-link>
                    <router-link :to="{ name: 'AdminStudentQuizzes' }"
                        class="list-group-item list-group-item-action border-0 py-3 px-4">
                        <i class="bi bi-clipboard-check me-3"></i>
                        <span>Quizzes</span>
                    </router-link>
                    <router-link :to="{ name: 'AdminStudentSummary' }"
                        class="list-group-item list-group-item-action border-0 py-3 px-4">
                        <i class="bi bi-graph-up me-3"></i>
                        <span>Summary</span>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import router from '../router';
import { useUserStore } from '../store/user';
import ConfirmationModal from './modals/ConfirmationModal.vue';
import { push } from 'notivue';

const isModalVisible = ref(false);
const modalMessage = ref('');
const userStore = useUserStore();
const openModal = () => {
    modalMessage.value = 'Are you sure you want to log out?';
    isModalVisible.value = true;
};

const closeModal = () => {
    isModalVisible.value = false;
};

const handleConfirm = async () => {
    closeModal();
    await router.push('/');
    userStore.logout();
    push.success('You have been logged out!');
};

const props = defineProps({
    pending_result: {
        type: Boolean
    }
});

</script>

<style scoped></style>