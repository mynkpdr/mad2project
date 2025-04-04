<template>
    <div class="container my-4 px-0">
        <div v-if="!start">
            <div class="text-center">
                <button class="btn btn-primary btn-lg px-5 fs-4 py-3" @click="startQuiz">
                    Start Quiz
                </button>
            </div>
        </div>
        <div v-if="start">
            <div v-if="!isSubmitted" class="card mb-4 mx-auto p-4"
                style="max-width: 800px;">
                <h2 class="text-center mb-5 h3">{{ quizStore.getCurrentQuestion().statement }}</h2>
                <div class="d-flex flex-column gap-3 mb-5">
                    <img v-if="quizStore.getCurrentQuestion().question_image"
                        :src="questionImageSrc.value + (quizStore.getCurrentQuestion().question_image)"
                        class="img-fluid mb-2" alt="Question Image"
                        style="max-width: 100%; max-height: 400px; object-fit: contain;" />
                    <div class="d-flex justify-content-between mb-3">
                        <span class="badge" :class="useUtils().bgQuestionTypeClass(quizStore.getCurrentQuestion().type)">
                            {{ quizStore.getCurrentQuestion().type }}
                        </span>
                        <span class="badge bg-success">
                            {{ quizStore.getCurrentQuestion().marks }} Marks
                        </span>
                    </div>

                    <div class="flex-grow-1">
                        <template v-if="quizStore.getCurrentQuestion().type === 'MCQ'">
                            <div v-for="option in quizStore.getCurrentQuestion().options" :key="option.id"
                                class="d-flex flex-column mb-3">
                                <button :key="option.id" class="btn btn-lg rounded-0 fw-bold" :class="{
                                    'btn-outline-primary': !isNightMode,
                                    'btn-primary text-white': quizStore.getCurrentQuestionStatus().selected_values === option.id,
                                    'btn-outline-light': quizStore.getCurrentQuestionStatus().selected_values !== option.id
                                }" @click="quizStore.handleSelectAnswer(option.id)">
                                    {{ option.text }}
                                </button>

                            </div>
                        </template>

                        <template v-if="quizStore.getCurrentQuestion().type === 'MSQ'">
                            <div v-for="option in quizStore.getCurrentQuestion().options" :key="option.id"
                                class="d-flex flex-column mb-3">
                                <div class="d-flex align-items-center">
                                    <label class="btn btn-lg w-100 position-relative rounded-0 fw-bold" :class="{
                                        'btn-primary text-white': Array.isArray(quizStore.getCurrentQuestionStatus().selected_values)
                                            && quizStore.getCurrentQuestionStatus().selected_values.includes(option.id),
                                        'btn-outline-light': !Array.isArray(quizStore.getCurrentQuestionStatus().selected_values)
                                            || !quizStore.getCurrentQuestionStatus().selected_values.includes(option.id),
                                        'btn-outline-primary': !isNightMode
                                    }" :for="option.id">

                                        <input class="position-absolute top-50 start-50 translate-middle"
                                            type="checkbox" :id="option.id" :value="option.id"
                                            :checked="Array.isArray(quizStore.getCurrentQuestionStatus().selected_values)
                                                && quizStore.getCurrentQuestionStatus().selected_values.includes(option.id)"
                                            @change="(event) => quizStore.handleMSQChange(option.id, event.target.checked)"
                                            style="opacity: 0; z-index: 1;">
                                        <!-- Lol  :) !! -->
                                        <span class="d-block">{{ option.text }}</span>
                                    </label>

                                </div>
                            </div>
                        </template>

                        <template v-if="quizStore.getCurrentQuestion().type === 'Numerical'">
                            <input class="form-control fw-bold form-control-lg rounded-0"
                                type="number"
                                :value="quizStore.getCurrentQuestionStatus().selected_values || ''"
                                @input="(event) => quizStore.handleSelectAnswer(event.target.value)">
                        </template>
                    </div>
                </div>

                <div class="d-flex flex-column flex-md-row align-items-center justify-content-between">
                    <button class="btn btn-lg rounded-0 px-5 py-3"
                        :class="{ 'btn-outline-light': isNightMode, 'btn-outline-primary': !isNightMode }"
                        @click="quizStore.moveToPreviousQuestion"
                        :disabled="quizStore.currentQuestionId === quizStore.questions[0]?.id">
                        Back
                    </button>
                    <div class="timer rounded-4">{{ quizStore.formattedTime }}</div>
                    <button v-if="!(quizStore.questions.length == quizStore.getCurrentQuestion().display_id)"
                        class="btn btn-lg rounded-0 px-5 py-3"
                        :class="{ 'btn-outline-light': isNightMode, 'btn-outline-primary': !isNightMode }"
                        @click="quizStore.handleNext">
                        Next
                    </button>
                    <button v-else class="btn btn-primary rounded-0 btn-lg px-5 py-3"
                        @click="quizStore.handleNext(); submit()">
                        Submit
                    </button>
                </div>
                <div class="text-center mt-4">
                    <button class="btn btn-lg rounded-0" v-for="question in quizStore.questions" :key="question.id"
                        :class="quizStore.currentQuestionId === question.id ? 'btn-primary' : 'btn-outline-primary'"
                        @click="quizStore.handleSelectQuestion(question.id)">
                        {{ question.display_id }}
                    </button>
                </div>
            </div>

            <div v-else>
                <div class="row">
                    <div class="col d-flex flex-column mb-4">
                        <div class="card flex-grow-1">
                            <div class="card-header">
                                <h5 class="card-title mb-0 fw-bold text-center">Practice Result</h5>
                            </div>
                            <div class="card-body text-center">
                                <div class="mb-4">
                                    <span class="display-1 fw-bold"
                                        :class="score.percentage < 40 ? 'text-danger' : 'text-success'">
                                        {{ score.scored }}
                                    </span>
                                    <span class="display-4 text-secondary"> / {{ score.total }}</span>
                                </div>
                                <div class="display-6 fw-bold mb-4"
                                    :class="score.percentage < 40 ? 'text-danger' : 'text-success'">
                                    You got {{ score.percentage }}%
                                </div>
                                <p class="lead mb-4">
                                    <i class="bi bi-clock me-2"></i>Time taken:
                                    <strong>{{ useDateFormatter().formatTimeTaken(quiz_data.time_taken) }}</strong>
                                </p>
                            </div>
                            <div class="d-flex justify-content-center mb-4">
                        <button class="btn btn-primary me-3" @click="retakeQuiz">Restart Practice</button>
                        <button class="btn btn-outline-primary" @click="router.push({ name: 'StudentDashboard' })">Back
                            to
                            Dashboard</button>
                    </div>
                        </div>
                    </div>
                    <div class="col d-flex flex-column mb-4">
                        <div class="card flex-grow-1">
                            <div class="card-header">
                                <h5 class="card-title mb-0 fw-bold text-center">Quiz Details</h5>
                            </div>
                            <div class="card-body p-0 text-center">
                                <ul class="list-group">
                                    <li class="list-group-item border-0 mb-3">
                                        <div class="mb-1">
                                            <i class="bi bi-clipboard-check text-primary me-2"></i>
                                            <span class="fw-bold text-secondary">Quiz</span>
                                        </div>
                                        <div class="text-secondary">{{ quiz_data.quiz_name }}</div>
                                    </li>
                                    <li class="list-group-item border-0 mb-3">
                                        <div class="mb-1">
                                            <i class="bi bi-list text-info me-2"></i>
                                            <span class="fw-bold text-secondary">Total Questions</span>
                                        </div>
                                        <span class="badge bg-info">
                                            {{ quiz_data.total_questions || 'NA' }}
                                        </span>
                                    </li>
                                    <li class="list-group-item border-0 mb-3">
                                        <div class="mb-1">
                                            <template v-if="quiz_data.quiz_difficulty == 'easy'">
                                                <i class="bi bi-star-fill text-success me-2"></i>
                                            </template>
                                            <template v-else-if="quiz_data.quiz_difficulty == 'medium'">
                                                <i class="bi bi-star-fill text-warning me-2"></i>
                                                <i class="bi bi-star-fill text-warning me-2"></i>
                                            </template>
                                            <template v-else-if="quiz_data.quiz_difficulty == 'hard'">
                                                <i class="bi bi-star-fill text-danger me-2"></i>
                                                <i class="bi bi-star-fill text-danger me-2"></i>
                                                <i class="bi bi-star-fill text-danger me-2"></i>
                                            </template>
                                            <span class="fw-bold text-secondary">Difficulty</span>
                                        </div>
                                        <span class="badge"
                                            :class="useUtils().bgDifficultyTypeClass(quiz_data.quiz_difficulty)">
                                            {{ quiz_data.quiz_difficulty.toUpperCase() }}
                                        </span>
                                    </li>
                                    <li class="list-group-item border-0 mb-3">
                                        <div class="mb-1">
                                            <i class="bi bi-calendar-event text-success me-2"></i>
                                            <span class="fw-bold text-secondary">Date Taken</span>
                                        </div>
                                        <span class="badge bg-success">
                                            {{ useDateFormatter().formatDate2(quiz_data.date_taken) }}
                                        </span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                <QuizResultCharts v-if="quiz_data.completed" class="mb-4" :quiz-data="quiz_data" />
                <PracticeResultDetail v-if="questions.length" :questions="questions" style="max-width: 800px;"/>
                <div class="card mx-auto mb-4" style="max-width: 800px;">
                    <!-- Action Buttons -->
                    <div class="card-footer border-0 d-flex justify-content-center">
                        <button class="btn btn-primary me-4" @click="retakeQuiz">Restart Practice</button>
                        <button class="btn btn-outline-primary" @click="router.push({ name: 'StudentDashboard' })">
                            Back to Dashboard</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useQuizStore } from '../../store/quizStore';
import axios from 'axios';
import { push } from 'notivue';
import { useNightModeStore } from '../../store/nightMode';
import router from '../../router';
import useUtils from '../../utils/useUtils';
import { useDateFormatter } from '../../utils/useDateFormatter';
import QuizResultCharts from '../../components/QuizResultCharts.vue';
import PracticeResultDetail from '../../components/PracticeResultDetail.vue';

const start = ref(false)
const isSubmitted = ref(false)
const route = useRoute()
const quizId = route.params.id;
const quizStore = useQuizStore();
const { isNightMode } = useNightModeStore();
let timerInterval = null;

const score = ref({
    scored: 0,
    total: 0,
    percentage: 0,
    timeTaken: 0,
})

const quiz_data = ref({
    student_name: '',
    student_profile_picture: '',
    quiz_id: 0,
    quiz_name: '',
    quiz_mode: '',
    quiz_difficulty: '',
    state: {},
    time_taken: 0,
    total_questions: 0,
    take_quiz_id: 0,
    completed: true,
    date_taken: null,
});
const questions = ref([]);

const startQuiz = async () => {
    try {
        const take_quiz_response = await axios.post(`/api/quizzes/${quizId}/take_quiz`);
        quizStore.resetQuiz() // Reset the quiz state so that we can start fresh
        quizStore.setTimeRemaining(take_quiz_response.data.data.time_duration);
        quizStore.setTakeQuizID(take_quiz_response.data.data.take_quiz_id)
        quizStore.setQuizID(take_quiz_response.data.data.id)
        fetchQuestions()
    } catch (error) {
        throw error
    }
    start.value = true
    startTimer()
}

const startTimer = () => {
    timerInterval = setInterval(() => {
        quizStore.decrementTimer();
        if (quizStore.timeRemaining === 0) {
            clearInterval(timerInterval);
            quizStore.handleSaveAndNext()
            submit()
            push.info("Time is up, the quiz has been submitted")
        }
    }, 1000);
};

const submit = async () => {
    try {
        // Fill skipped questions with default values
        quizStore.questions.forEach(question => {
            if (!quizStore.quizState[question.id]) {
                if (question.type === 'MCQ' || question.type === 'Numerical') {
                    quizStore.quizState[question.id] = { "answered": false, "selected_values": null };
                } else if (question.type === 'MSQ') {
                    quizStore.quizState[question.id] = { "answered": false, "selected_values": [] };
                }
            }
        });
        console.log(quizStore.quizState)
        await axios.post(`/api/take_quiz/${quizStore.take_quiz_id}/submit`, {
            "quiz_state": quizStore.quizState,
        });
        const submit_response = await axios.get('/api/students/take_quizzes/' + quizStore.take_quiz_id);
        if (submit_response.data.data.result_state && Object.keys(submit_response.data.data.result_state).length > 0) {
            score.value = submit_response.data.data.result_state.data.score;
            questions.value = submit_response.data.data.result_state.data.questions;
        }
        quiz_data.value = submit_response.data.data
        isSubmitted.value = true

    } catch (error) {
        throw error
    }
}

const fetchQuestions = async () => {
    try {
        const response = await axios.get(`/api/quizzes/${quizId}/questions`);
        const data = response.data.data;
        quizStore.setQuestions(data.questions);
        quizStore.setChapter(data.chapter_name);
    } catch (error) {
        throw error;
    }
};

const takeQuiz = async () => {
    try {
        const quiz_response = await axios.get(`/api/quizzes/${quizId}`);
        if (quiz_response.data.data.quiz_mode.toLowerCase() == "exam") {
            router.push({ name: 'StudentDashboard' })
            push.error("This quiz is not available for practice")
        }
    } catch (error) {
        throw error
    }
};

// Action handlers
const retakeQuiz = () => {
    start.value = false
    isSubmitted.value = false
    quizStore.resetQuiz()
    clearInterval(timerInterval)
    takeQuiz()
    push.info("Quiz has been reset. Good luck!")
};

onMounted(() => {
    takeQuiz()
});
onUnmounted(() => {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
});
</script>

<style scoped>
.timer {
    font-family: monospace;
    font-size: 2rem;
}
</style>