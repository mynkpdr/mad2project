<template>
  <Notivue v-slot="item">
    <Notification :item="item">
      <NotificationProgress :item="item" />
    </Notification>
  </Notivue>
  <div class="app-container" :style="{ backgroundColor: isNightMode ? '#070914 !important' : '' }" :class="{'night-mode' : isNightMode}">
    <div v-if="userStore.isAuthenticated && userStore.isAdmin" class="admin-layout">
      <Sidebar />
      <div class="main-wrapper">
        <NavBar />
        <main class="main-content">
          <router-view />
        </main>
      </div>
    </div>
    <div v-else class="user-layout">
      <NavBar />
      <main class="main-content" :style="{ backgroundColor: isNightMode ? '#070914 !important' : '' }">
        <router-view />
      </main>
      <Footer></Footer>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/AdminSidebar.vue';
import NavBar from './components/NavBar.vue';
import Footer from './components/Footer.vue';
import { Notivue, Notification, NotificationProgress } from 'notivue'
import { useUserStore } from './store/user';
import { useNightModeStore } from './store/nightMode';
const isNightMode = useNightModeStore().isNightMode;
const userStore = useUserStore();
</script>

<style>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.user-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  transition: margin-left 0.4s ease;
  margin-left: 70px;
}

.sidebar:hover~.main-wrapper {
  margin-left: 245px;
}

/* Responsive styles */
@media (max-width: 768px) {
  .main-wrapper {
    margin-left: 0;
  }

  .sidebar:hover~.main-wrapper {
    margin-left: 170px;
  }

  .admin-layout {
    margin-left: 85px;
  }
}
</style>