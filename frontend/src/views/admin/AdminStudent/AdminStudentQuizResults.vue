<template>
    <div v-if="quiz_data.quiz_mode == 'practice'" class="container my-4 px-0">
        <div class="row">
            <StudentSidebar />
            <div class="col-md-10">
                <div class="row align-items-stretch">
                <div v-if="quiz_data.completed" class="col d-flex flex-column mb-4">
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
                                    <button class="btn btn-outline-primary"
                                        @click="router.back()">Back</button>
                            </div>
                        </div>
                    
                </div>
                <div v-else class="col flex-column mb-4">
                        <div class="card mx-auto">
                            <!-- Score Card -->
                            <div class="card-header">
                                <h5 class="card-title mb-0 fw-bold text-center">Practice Result</h5>
                            </div>
                            <div class="card-body text-center">
                                You didn't complete the practice. Please retake the quiz to see the result.
                            </div>
                        </div>
                    </div>
                    <div v-if="quiz_data && quiz_data.completed" class="col d-flex flex-column mb-4">
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
                <PracticeResultDetail v-if="questions.length" :questions="questions" />
                <div class="card mx-auto mb-4">
                    <!-- Action Buttons -->
                    <div class="card-footer border-0 d-flex justify-content-center">
                        <button class="btn btn-outline-primary" @click="router.back()">
                            Back</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-else-if="quiz_data.quiz_mode == 'exam'">
        <div class="container my-4 px-0">
            <div class="row">
                <StudentSidebar />
                <div class="col-md-10">
                    <div class="row align-items-stretch">
                        <div v-if="quiz_data.completed && Object.keys(quiz_data.result_state).length"
                            class="col d-flex flex-column mb-4">
                            <div class="card flex-grow-1">
                                <div class="card-header">
                                    <h5 class="card-title mb-0 fw-bold text-center">Exam Result</h5>
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
                            </div>
                        </div>
                        <div v-else-if="quiz_data.completed && !Object.keys(quiz_data.result_state).length"
                            class="col d-flex flex-column mb-4">
                            <div class="card mx-auto mb-4">
                                <div class="card-header">
                                    <h5 class="card-title mb-0 fw-bold text-center">Exam Result</h5>
                                </div>
                                <div class="card-body text-center">
                                <p>The result is still not published. Kindly wait for the result to be published.</p>
                                <button class="btn btn-outline-primary" @click="router.back()">Back</button>
                            </div>
                            </div>
                        </div>
                        <div v-else class="col flex-column mb-4">
                            <div class="card mx-auto">
                                <!-- Score Card -->
                                <div class="card-header">
                                    <h5 class="card-title mb-0 fw-bold text-center">Exam Result</h5>
                                </div>
                                <div class="card-body text-center">
                                    <p>The quiz was not submitted</p>
                                    <button class="btn btn-outline-primary" @click="router.back()">Back</button>
                                </div>
                            </div>
                        </div>
                        <div v-if="quiz_data" class="col d-flex flex-column mb-4">
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
                </div>
            </div>
            <QuizResultCharts v-if="quiz_data.completed && Object.keys(quiz_data.result_state).length" class="mb-4"
                :quiz-data="quiz_data" />
                <div v-if="quiz_data.completed && Object.keys(quiz_data.result_state).length">
                <ExamResultHeader v-if="quiz_data.completed && Object.keys(quiz_data.result_state).length"
                    :quiz-data="quiz_data" />
                <div class="row">
                    <div class="col-md-9 mb-4">
                        <ExamResultQuestionPanel :questions="questions"
                            :current-question-index="currentQuestionIndex" :quiz-data="quiz_data"
                            @update:current-question-index="handleCurrentQuestionIndex" />
                    </div>
                    <div class="col-md-3 mb-4">
                        <ExamResultQuestionOverview :questions="questions" :quiz-data="quiz_data"
                            @update:current-question-index="handleCurrentQuestionIndex" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import router from '../../../router';
import StudentSidebar from '../../../components/StudentSidebar.vue';
import { useDateFormatter } from '../../../utils/useDateFormatter';
import useUtils from '../../../utils/useUtils';
import QuizResultCharts from '../../../components/QuizResultCharts.vue';
import ExamResultQuestionPanel from '../../../components/ExamResultQuestionPanel.vue';
import ExamResultQuestionOverview from '../../../components/ExamResultQuestionOverview.vue';
import ExamResultHeader from '../../../components/ExamResultHeader.vue';
import PracticeResultDetail from '../../../components/PracticeResultDetail.vue';
const route = useRoute()
const takeQuizId = route.params.take_quiz_id;
const currentQuestionIndex = ref(0);

const handleCurrentQuestionIndex = (index) => {
    currentQuestionIndex.value = index;
};

const score = ref({
    scored: 0,
    total: 0,
    percentage: 0,
    time_taken: 0,
});

const questions = ref([]);

const quiz_data = ref({
    student_name: '',
    student_profile_picture: '',
    quiz_id: 0,
    quiz_name: '',
    quiz_mode: '',
    quiz_difficulty: '',
    state: {},
    total_scored: 0,
    time_taken: 0,
    total_questions: 0,
    take_quiz_id: 0,
    completed: true,
    date_taken: null,
});

const getResult = async () => {
    try {
        const submit_response = await axios.get('/api/students/take_quizzes/' + takeQuizId);
        if (submit_response.data.data.result_state && Object.keys(submit_response.data.data.result_state).length > 0) {
            score.value = submit_response.data.data.result_state.data.score;
            questions.value = submit_response.data.data.result_state.data.questions;
        }
        quiz_data.value = submit_response.data.data
        console.log(quiz_data)
    } catch (error) {
        throw error
    }
}

onMounted(() => {
    getResult()
});
</script>
