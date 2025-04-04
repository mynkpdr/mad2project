<template>
    <StudentMyQuizzes :isAdmin="true" :studentId="studentId" />
</template>

<script setup>
import { useRoute } from 'vue-router';
import StudentMyQuizzes from '../../student/dashboard/StudentMyQuizzes.vue';
const route = useRoute()
const studentId = parseInt(route.params.id)
</script>