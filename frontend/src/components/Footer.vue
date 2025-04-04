<template>
    <div class="pb-4" :style="{'background-color': isNightMode ? '#070914' : '' }">
        <div class="container py-4 rounded-2"
            style="border: 1px solid rgba(0, 0, 0, 0.175); background-color: #161a2d;">
            <div class="row">

                <div class="col-md-4 text-md-start">
                    <a href="#" class="text-white text-decoration-none">
                        <img :src="staticSrc.value + 'logo/logo_512.png'" alt="Logo" class="mr-2"
                            style="width: 30px; height: 30px;">
                        <span class="mx-2">&copy; 2025 Exambhai</span>
                    </a>
                </div>

                <div class="col-md-4 text-center">
                    <router-link class="text-white ms-3 text-decoration-none" :to="{ name: 'Home'}">Home</router-link>
                    <router-link class="text-white ms-3 text-decoration-none" :to="{ name: 'Home', hash: '#key_features' }">Features</router-link>
                    <router-link class="text-white ms-3 text-decoration-none" :to="{ name: 'Home', hash: '#faqs' }">FAQs</router-link>
                    <router-link class="text-white ms-3 text-decoration-none" :to="{ name: 'Home', hash: '#contact' }">Contact</router-link>
                </div>


                <div class="col-md-4 text-md-end">
                    <a href="https://www.facebook.com/exambhai" class="text-white ms-3"><i
                            class="bi bi-facebook"></i></a>
                    <a href="https://www.x.com/exambhai" class="text-white ms-3"><i class="bi bi-twitter"></i></a>
                    <a href="https://www.instagram.com/exambhai" class="text-white ms-3"><i
                            class="bi bi-instagram"></i></a>
                    <a href="https://www.linkedin.com/in/exambhai" class="text-white ms-3"><i
                            class="bi bi-linkedin"></i></a>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useNightModeStore } from '../store/nightMode';
const {isNightMode} = useNightModeStore();
</script>