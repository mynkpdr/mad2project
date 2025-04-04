<template>
    <StudentDashboard :isAdmin="true" :studentId="studentId" />
</template>

<script setup>

import { useRoute } from 'vue-router';
import StudentDashboard from '../../student/dashboard/StudentDashboard.vue';
const route = useRoute()
const studentId = parseInt(route.params.id)
</script>