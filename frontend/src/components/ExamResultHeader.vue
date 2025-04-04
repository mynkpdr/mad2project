<template>
    <div class="card shadow mb-4">
        <div class="card-body px-4">
            <div class="row align-items-center">
                <div class="col-auto">
                    <div class="d-flex align-items-center">
                        <img :src="profilePictureSrc.value + quizData.student_profile_picture" alt="Profile Image"
                            class="rounded-circle me-3" style="width: 50px; height: 50px; object-fit: cover;" />
                        <div>
                            <div>Candidate Name: {{ quizData.student_name }}</div>
                            <div>Quiz Name: {{ quizData.quiz_name }}</div>
                        </div>
                    </div>
                </div>
                <div class="col text-end">
                    <div class="timer">Time Taken: {{ useDateFormatter().formatTimeTaken(quizData.time_taken) }}</div>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary" @click="toggleCalculator">
                        <i class="bi bi-calculator"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Calculator Modal -->
    <div v-show="isCalculatorVisible">
        <div class="modal d-block rounded-0" style="background-color: rgba(0, 0, 0, 0.4);">
            <div class="modal-dialog">
                <div class="modal-content rounded-0">
                    <div class="modal-header">
                        <h5 class="modal-title">Scientific Calculator</h5>
                        <button type="button" class="btn-close" @click="toggleCalculator" aria-label="Close"></button>
                    </div>
                    <div class="container d-flex p-0 m-0">
                        <iframe src="https://mynkpdr.github.io/scientific-calculator/"
                            style="width: 100%; height: 301px; border: none;"></iframe>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useDateFormatter } from '../utils/useDateFormatter';

const props = defineProps({
    quizData: {
        type: Object,
        required: true
    }
});

const isCalculatorVisible = ref(false);

const toggleCalculator = () => {
    isCalculatorVisible.value = !isCalculatorVisible.value;
};
</script>
<style scoped>
.timer {
    font-family: monospace;
    font-size: 1.5rem;
    color: #0d6efd;
}
</style>