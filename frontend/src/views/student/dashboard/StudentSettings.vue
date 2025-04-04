<template>
    <div class="container my-4 px-0">
        <div class="row">
            <StudentSidebar />
            <div class="col-md-10">
                <div class="row">
                    <!-- Export Settings Card -->
                    <div class="col-md-6 mb-4">
                        <div class="card h-100">
                            <div class="card-header">
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-file-earmark-arrow-down fs-4 me-2 text-primary"></i>
                                    <h5 class="card-title mb-0">Export Settings</h5>
                                </div>
                            </div>
                            <div class="card-body">
                                <p class="text-secondary mb-4">Choose how you want to receive your exported data</p>
                                <div class="mb-4">
                                    <div class="form-check form-check-inline mb-3">
                                        <input class="form-check-input" type="radio" v-model="exportMethod"
                                            value="direct" id="directExport">
                                        <label class="form-check-label" for="directExport">
                                            <i class="bi bi-download me-2"></i>Direct Download
                                        </label>
                                    </div>
                                    <div class="form-check form-check-inline">
                                        <input class="form-check-input" type="radio" v-model="exportMethod"
                                            value="email" id="emailExport">
                                        <label class="form-check-label" for="emailExport">
                                            <i class="bi bi-envelope me-2"></i>Send to Email
                                        </label>
                                    </div>
                                </div>
                                <div class="text-secondary">
                                    <small>
                                        <i class="bi bi-info-circle me-1"></i>
                                        {{ exportMethod === 'direct' ?
                                            'Files will be downloaded directly to your device' :
                                            'Files will be sent to your registered email address' }}
                                    </small>
                                    {{ exportMethod === 'direct' ? '' : useUserStore().userData.email }}
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Display Settings Card -->
                    <div class="col-md-6 mb-4">
                        <div class="card h-100">
                            <div class="card-header">
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-palette fs-4 me-2 text-primary"></i>
                                    <h5 class="card-title mb-0">Display Settings</h5>
                                </div>
                            </div>
                            <div class="card-body">
                                <p class="text-secondary mb-4">Customize your viewing experience</p>
                                <div class="d-flex align-items-center justify-content-start">
                                    <i class="bi bi-sun me-2"></i>
                                    <span class="me-3">Light Mode</span>
                                    <div class="form-check form-switch d-flex align-items-center">
                                        <input class="form-check-input" type="checkbox" role="switch"
                                            id="nightModeSwitch" :checked="isNightMode" @change="toggleNightMode">
                                        <label class="form-check-label ms-2" for="nightModeSwitch">
                                            <i class="bi bi-moon-stars ms-2"></i>
                                        </label>
                                    </div>
                                    <span class="ms-2">Night Mode</span>
                                </div>

                                <div class="text-secondary mt-3">
                                    <small>
                                        <i class="bi bi-info-circle me-1"></i>
                                        Night mode reduces eye strain in low-light conditions
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <!-- Notifications Settings Card -->
                    <div class="col-md-6 mb-4">
                        <div class="card h-100">
                            <div class="card-header">
                                <div class="d-flex align-items-center">
                                    <i class="bi bi-bell fs-4 me-2 text-primary"></i>
                                    <h5 class="card-title mb-0">Notifications Settings</h5>
                                </div>
                            </div>
                            <div class="card-body">
                                <p class="text-secondary mb-4">Choose how you want to receive notifications</p>
                                <div class="mb-4">
                                    <div class="form-check mb-3">
                                        <input class="form-check-input" type="checkbox" v-model="emailNotification"
                                            id="emailNotification">
                                        <label class="form-check-label" for="emailNotification">
                                            <i class="bi bi-envelope me-2"></i>Email
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Save Button -->
                <div class="row">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-body">
                                <button @click="saveSettings" class="btn btn-primary">
                                    <i class="bi bi-save me-2"></i>Save Settings
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import StudentSidebar from '../../../components/StudentSidebar.vue';
import { push } from 'notivue';
import { useNightModeStore } from '../../../store/nightMode';
import { useUserStore } from '../../../store/user';
import axios from 'axios';
const { isNightMode, toggleNightMode } = useNightModeStore();
const exportMethod = ref('direct');
const emailNotification = ref(true);

onMounted(() => {
    const savedMethod = localStorage.getItem('exportMethod');
    if (savedMethod) {
        exportMethod.value = savedMethod;
    }
    axios.get('/api/users/notifications').then(response => {
        emailNotification.value = response.data.notifications_enabled;
    });
});

const saveSettings = () => {
    localStorage.setItem('exportMethod', exportMethod.value);
    axios.post('/api/users/notifications/' + (emailNotification.value ? 'enable' : 'disable'));
    push.success('Settings saved successfully!');
};
</script>