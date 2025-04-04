<template>
  <!-- Navigation -->
  <nav v-if="!isAuthenticated" class="navbar navbar-expand-lg navbar-dark" :style="navbarStyle">
    <div class="container mt-4 p-2 rounded-2" style="border: 1px solid rgba(0, 0, 0, 0.175);"
      :style="route.name == 'Home' ? 'background-color: #070914;' : 'background-color: #161a2d;'">
      <router-link :to="{ name: 'Home' }" class="navbar-brand">
        <img :src="staticSrc.value + 'logo/logo_horizontal_white_400_100.png'" alt="logo" width="200" />
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto fs-5">
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'BrowseExam' }">Exams</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'BrowsePractice' }">Practice</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Leaderboard' }">Leaderboard</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Home', hash: '#key_features' }">Features</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Home', hash: '#faqs' }">FAQs</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Home', hash: '#contact' }">Contact</router-link>
          </li>

        </ul>
        <div class="d-flex gap-2">
          <router-link :to="{ name: 'Login' }" class="btn btn-primary m-2 px-4 py-2 fw-bold">Login</router-link>
          <router-link :to="{ name: 'Signup' }"
            class="btn btn-light text-dark my-2 px-3 py-2 fw-bold">Signup</router-link>
        </div>
      </div>
    </div>
  </nav>
  <nav v-else-if="isAuthenticated && isAdmin" class="navbar navbar-expand-lg navbar-dark" style="background-color: #161a2d;">
    <div class="container-fluid">
      <router-link :to="{ name: 'AdminDashboard' }" class="navbar-brand">
        <span class="fw-bold text-white">ADMIN PANEL</span>
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <span class="badge timer text-secondary fs-6 nav-time d-block"><i class="bi bi-calendar"></i> {{ dateNow
          }}</span>
        <span class="badge timer text-secondary fs-6 nav-time d-block"><i class="bi bi-clock"></i> {{ timeNow }}</span>
        <ul class="navbar-nav ms-auto align-items-center me-4">
          <li class="nav-item dropdown ms-5">
            <a class="nav-link d-flex align-items-center pe-0" href="#" data-bs-toggle="dropdown" aria-expanded="false">
              <img :src="profilePictureSrc.value + userStore.userData.profile_picture" alt="Profile"
                class="img-fluid rounded-circle mx-2" width="50" height="50">
              <div class="dropdown-toggle">
              </div>
            </a>
            <ul class="dropdown-menu dropdown-menu-end dropdown-menu-arrow profile my-2">
              <li class="dropdown-header">
                <h6>{{ userStore.userData.name }}</h6>
                <span>{{ userStore.userData.email }}</span>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <router-link class="dropdown-item d-flex align-items-center" :to="{ name: 'AdminProfile' }">
                  <i class="bi bi-person me-2"></i>
                  <span>My Profile</span>
                </router-link>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <router-link class="dropdown-item d-flex align-items-center" :to="{ name: 'AdminSettings' }">
                  <i class="bi bi-gear me-2"></i>
                  <span>Settings</span>
                </router-link>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <button class="dropdown-item d-flex align-items-center" @click="toggleNightMode">
                  <i :class="isNightMode ? 'bi bi-sun-fill me-2' : 'bi bi-moon-fill me-2'"></i>
                  <span>{{ isNightMode ? 'Light Mode' : 'Night Mode' }}</span>
                </button>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <button @click.prevent="openModal" class="dropdown-item d-flex align-items-center">
                  <i class="bi bi-box-arrow-right me-2"></i>
                  <span>Logout</span>
                </button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <nav v-else-if="isAuthenticated && !isAdmin" class="navbar navbar-expand-lg navbar-dark" :style="navbarStyle">
    <div class="container mt-4 p-2 rounded-2" style="border: 1px solid rgba(0, 0, 0, 0.175);"
      :style="route.name == 'Home' ? 'background-color: #070914;' : 'background-color: #161a2d;'">
      <router-link :to="{ name: 'Home' }" class="navbar-brand">
        <img :src="staticSrc.value + 'logo/logo_horizontal_white_400_100.png'" alt="logo" width="200" />
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto fs-5">
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'StudentDashboard' }">Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'BrowseExam' }">Exams</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'BrowsePractice' }">Practice</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'Leaderboard' }">Leaderboard</router-link>
          </li>
        </ul>
        <ul class="navbar-nav ms-auto align-items-center">
          <span class="badge timer text-secondary fs-6 nav-time d-block"><i class="bi bi-calendar"></i> {{ dateNow
            }}</span>
          <span class="badge timer text-secondary fs-6 nav-time d-block"><i class="bi bi-clock"></i> {{ timeNow
            }}</span>
          <li class="nav-item dropdown ms-5">
            <a class="nav-link d-flex align-items-center pe-0" href="#" data-bs-toggle="dropdown" aria-expanded="false">
              <img :src="profilePictureSrc.value + userStore.userData.profile_picture" alt="Profile"
                class="img-fluid rounded-circle mx-2" width="50" height="50">
              <div class="dropdown-toggle">
              </div>
            </a>
            <ul class="dropdown-menu dropdown-menu-end dropdown-menu-arrow profile my-2">
              <li class="dropdown-header">
                <h6>{{ userStore.userData.name }}</h6>
                <span>{{ userStore.userData.email }}</span>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <router-link class="dropdown-item d-flex align-items-center" :to="{ name: 'StudentProfile' }">
                  <i class="bi bi-person me-2"></i>
                  <span>My Profile</span>
                </router-link>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <button class="dropdown-item d-flex align-items-center" @click="toggleNightMode">
                  <i :class="isNightMode ? 'bi bi-sun-fill me-2' : 'bi bi-moon-fill me-2'"></i>
                  <span>{{ isNightMode ? 'Light Mode' : 'Night Mode' }}</span>
                </button>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <router-link class="dropdown-item d-flex align-items-center" :to="{ name: 'StudentSettings' }">
                  <i class="bi bi-gear me-2"></i>
                  <span>Settings</span>
                </router-link>
              </li>
              <li>
                <hr class="dropdown-divider">
              </li>
              <li>
                <button @click.prevent="openModal" class="dropdown-item d-flex align-items-center">
                  <i class="bi bi-box-arrow-right me-2"></i>
                  <span>Logout</span>
                </button>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <ConfirmationModal :visible="isModalVisible" :message="modalMessage" @close="closeModal" @confirm="handleConfirm" />
</template>

<script setup>
import { ref, computed } from 'vue';
import { useUserStore } from '../store/user';
import ConfirmationModal from './modals/ConfirmationModal.vue';
import { useRoute, useRouter } from 'vue-router';
import { push } from 'notivue';
import { useNightModeStore } from '../store/nightMode';
const { isNightMode, toggleNightMode } = useNightModeStore();

const userStore = useUserStore();
const isAdmin = computed(() => userStore.isAdmin);
const isAuthenticated = computed(() => userStore.isAuthenticated);
const dateNow = ref('');
const timeNow = ref('');
const isModalVisible = ref(false);
const modalMessage = ref('');
const router = useRouter();
const route = useRoute();
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

const updateDateTime = () => {
  const today = new Date();
  const date = today.toDateString().toUpperCase();
  const time = today.toLocaleTimeString('en-US', { hour12: true });
  dateNow.value = date;
  timeNow.value = time;
}

setInterval(updateDateTime, 1000);
updateDateTime();


const navbarStyle = computed(() => {
  const homePage = route.path === '/';
  if (homePage && isAuthenticated.value && !isAdmin.value && isNightMode) {
    return 'background-color: #161a2d;';
  } else if (!homePage && isAuthenticated.value && !isAdmin.value && isNightMode) {
    return 'background-color: #070914;';
  } else if (!isAuthenticated.value && !homePage && isNightMode) {
    return 'background-color: #070914;';
  } else if (!isAuthenticated.value && homePage && isNightMode) {
    return 'background-color: #161a2d;';
  }
});
</script>

<style scoped>
.profile {
  min-width: 250px;
}
</style>