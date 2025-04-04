<template>
    <ConfirmationModal :visible="isModalVisible" :message="modalMessage" @close="closeModal" @confirm="handleConfirm" />
    <aside class="sidebar" v-if="userStore.isAuthenticated && userStore.isAdmin">
        <div class="sidebar-header">
            <img :src="staticSrc.value + 'logo/logo_horizontal_white_400_100.png'" alt="logo" />
        </div>
        <ul class="sidebar-links">
            <h4>
                <span>General</span>
                <div class="menu-separator"></div>
            </h4>
            <li>
                <router-link :to="{ 'name': 'AdminDashboard' }">
                    <i class="bi bi-speedometer2"></i>Dashboard</router-link>
            </li>
            <li>
                <router-link :to="{ 'name': 'AdminStudents' }"><i class="bi bi-person"></i>Students</router-link>
            </li>
            <li>
                <router-link :to="{ 'name' : 'AdminLeaderboard' }">
                    <i class="bi bi-trophy"></i>Leaderboard</router-link>
            </li>
            <h4>
                <span>Main</span>
                <div class="menu-separator"></div>
            </h4>
            <li>
                <router-link :to="{ 'name': 'AdminAdd' }"><i class="bi bi-plus-circle"></i>Add</router-link>
            </li>
            <li>
                <router-link :to="{ 'name': 'AdminQuizzes' }"><i class="bi bi-clipboard-check"></i>Quizzes</router-link>
            </li>
            <li>
                <router-link :to="{ 'name': 'AdminSubjects' }"><i class="bi bi-book"></i>Subjects</router-link>
            </li>
            <li>
                <router-link :to="{ 'name': 'AdminChapters' }"><i
                        class="bi bi-file-earmark-text"></i>Chapters</router-link>
            </li>
            <li>
                <router-link :to="{ 'name': 'AdminQuestions' }"><i class="bi bi-clipboard"></i>Questions</router-link>
            </li>
            <li>
                <router-link :to="{ 'name': 'AdminContacts' }"><i class="bi bi-envelope"></i>Messages</router-link>
            </li>
            <h4>
                <span>Account</span>
                <div class="menu-separator"></div>
            </h4>
            <li>
                <router-link :to="{ 'name': 'AdminProfile' }"><i class="bi bi-person-circle"></i>Profile</router-link>
            </li>
            <li>
                <a v-if="isNightMode" href="#" @click="toggleNightMode">
                    <i class='bi bi-sun-fill'></i>Light Mode
                </a>
                <a v-else href="#" @click="toggleNightMode">
                    <i class='bi bi-moon-fill'></i>Night Mode
                </a>
            </li>
            <li>
                <router-link :to="{ 'name': 'AdminSettings' }"><i class="bi bi-gear"></i>Settings</router-link>
            </li>
            <li>
                <a href="#" @click.prevent="openModal" class="text-danger"><i class="bi bi-box-arrow-right text-danger"></i>Logout</a>
            </li>
        </ul>
        <div class="user-account">
            <div class="user-profile">
                <img :src="profilePictureSrc.value + userStore.userData.profile_picture" alt="Profile Image" />
                <div class="user-detail">
                    <h3>{{ userStore.userData.name }}</h3>
                    <span>{{ userStore.userData.email }}</span>
                </div>
            </div>
        </div>
    </aside>
</template>

<script setup>
import { ref } from 'vue';
import { useUserStore } from '../store/user';
import { useRouter } from 'vue-router';
import ConfirmationModal from './modals/ConfirmationModal.vue';
import { push } from 'notivue';
import { useNightModeStore } from '../store/nightMode';
const { isNightMode, toggleNightMode } = useNightModeStore();


const router = useRouter();
const userStore = useUserStore();

const isModalVisible = ref(false);
const modalMessage = ref('');

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

</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Poppins", sans-serif;
}

body {
    min-height: 100vh;
    background: #F0F4FF;
}

.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100%;
    width: 85px;
    display: flex;
    overflow-x: hidden;
    flex-direction: column;
    padding: 25px 20px;
    transition: all 0.4s ease;
}

.sidebar:hover {
    width: 260px;
}

.sidebar .sidebar-header {
    display: flex;
    align-items: center;
}

.sidebar .sidebar-header img {
    width: 100%;
}


.sidebar-links h4 {
    color: #fff;
    font-weight: 500;
    white-space: nowrap;
    margin: 10px 0;
    position: relative;
}

.sidebar-links h4 span {
    opacity: 0;
}

.sidebar:hover .sidebar-links h4 span {
    opacity: 1;
}

.sidebar-links .menu-separator {
    position: absolute;
    left: 0;
    top: 50%;
    width: 100%;
    height: 1px;
    transform: scaleX(1);
    transform: translateY(-50%);
    background: #4f52ba;
    transform-origin: right;
    transition-delay: 0.2s;
}

.sidebar:hover .sidebar-links .menu-separator {
    transition-delay: 0s;
    transform: scaleX(0);
}

.sidebar-links {
    list-style: none;
    margin-top: 20px;
    height: 80%;
    overflow-y: auto;
    scrollbar-width: none;
}

.sidebar-links::-webkit-scrollbar {
    display: none;
}

.sidebar-links li a {
    display: flex;
    align-items: center;
    gap: 0 20px;
    color: #fff;
    font-weight: 500;
    white-space: nowrap;
    padding: 15px 10px;
    text-decoration: none;
    transition: 0.2s ease;
}

.sidebar-links li a:hover {
    color: #161a2d;
    background: #fff;
    border-radius: 4px;
}

.user-account {
    margin-top: auto;
    padding: 12px 10px;
    margin-left: -10px;
}

.user-profile {
    display: flex;
    align-items: center;
    color: #161a2d;
}

.user-profile img {
    width: 42px;
    border-radius: 50%;
    border: 2px solid #fff;
}

.user-profile h3 {
    font-size: 1rem;
    font-weight: 600;
}

.user-profile span {
    font-size: 0.775rem;
    font-weight: 600;
}

.user-detail {
    margin-left: 23px;
    white-space: nowrap;
}

.sidebar:hover .user-account {
    background: #fff;
    border-radius: 4px;
}
</style>