<template>
    <ConfirmationModal :visible="isModalVisible" :message="ModalMessage" :title="'Start the quiz?'" :cancelText="'No'"
        :confirmText="'Yes'" @close="closeModal" @confirm="handleConfirm" />

    <!-- Instructions Panel -->
    <div v-if="!start_quiz" class="container my-4 px-0">
        <div class="card">
            <div class="card-header">
                <h4 class="card-title mb-0">Quiz Instructions</h4>
            </div>
            <div class="card-body">
                <div class="row mb-4">
                    <div class="col-md-6">
                        <h5>General Instructions:</h5>
                        <ol class="mb-4">
                            <li>Total duration of examination is {{ Math.floor(store.timeRemaining / 60) }} minutes.
                            </li>
                            <li>The clock will be set at the server. The countdown timer will display the remaining
                                time.</li>
                            <li>The question palette displayed on the right side will show the status of your questions:
                            </li>
                            <div class="ms-0 mt-2">
                                <div class="d-flex align-items-center mb-2">
                                    <div class="bg-light border rounded me-2" style="width: 20px; height: 20px;"></div>
                                    <small>Not Visited - You haven't visited the question yet</small>
                                </div>
                                <div class="d-flex align-items-center mb-2">
                                    <div class="bg-success rounded me-2" style="width: 20px; height: 20px;"></div>
                                    <small>Answered - You've answered the question</small>
                                </div>
                                <div class="d-flex align-items-center mb-2">
                                    <div class="bg-danger rounded me-2" style="width: 20px; height: 20px;"></div>
                                    <small>Not Answered - You've visited but not answered</small>
                                </div>
                                <div class="d-flex align-items-center">
                                    <div class="bg-warning rounded me-2" style="width: 20px; height: 20px;"></div>
                                    <small>Marked for Review - You want to review it later (Considered for
                                        Evaluation)</small>
                                </div>
                            </div>
                        </ol>
                        <div class="border-top pt-4">
                            <h5>Important Notes:</h5>
                            <ul class="mb-4">
                                <li>The test will automatically submit when the time expires.</li>
                                <li>Ensure stable internet connection throughout the test.</li>
                                <li>Do not refresh the page or close the browser window.</li>
                                <li>You cannot revisit this exam once submitted.</li>
                            </ul>

                            <div class="form-check mb-3">
                                <input class="form-check-input" type="checkbox" v-model="instructionsRead"
                                    id="instructionsCheck">
                                <label class="form-check-label" for="instructionsCheck">
                                    I have read and understood all the instructions
                                </label>
                            </div>

                            <div class="d-flex gap-2">
                                <button class="btn btn-success" @click="handleConfirm" :disabled="!instructionsRead">
                                    Start Quiz
                                </button>
                                <button class="btn btn-outline-danger" @click="closeModal">
                                    Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="row mb-4">
                            <div class="col-md-12">
                                <h5>Quiz Details:</h5>
                                <ul>
                                    <li><strong>Quiz Name:</strong> {{ store.quizName }}</li>
                                    <li><strong>Total Marks:</strong> {{ store.totalMarks }}</li>
                                    <li><strong>Time Duration:</strong> {{ Math.floor(store.timeRemaining / 60) }} minutes</li>
                                </ul>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <h5>Candidate Details:</h5>
                                <ul>
                                    <li><strong>Name:</strong> {{ userData.name }}</li>
                                    <li><strong>Email:</strong> {{ userData.email }}</li>
                                    <li><strong>Student ID:</strong> {{ userData.id }}</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <img :src="profilePictureSrc.value + userData.profile_picture" alt="Profile Image"
                                    class="rounded-square rounded-2"
                                    style="width: 100px; height: 100px; object-fit: cover;" />
                            </div>
                        </div>
                        <div class="border-top pt-4">
                            <h5>Navigation Instructions:</h5>
                            <ol class="mb-4">
                                <li>Click on a question number to directly go to that question.</li>
                                <li>"Save & Next" saves your answer and moves to the next question.</li>
                                <li>"Mark for Review" flags the question for later review.</li>
                                <li>"Clear" removes your selected answer.</li>
                                <li>You can use the scientific calculator for calculations.</li>
                            </ol>

                            <h5>Question Types:</h5>
                            <ul>
                                <li><strong><span class="badge me-2"
                                            :class="useUtils().bgQuestionTypeClass('MCQ')">MCQ</span>:</strong> Select
                                    one
                                    correct option</li>
                                <li><strong><span class="badge me-2"
                                            :class="useUtils().bgQuestionTypeClass('MSQ')">MSQ</span>:</strong> Select
                                    multiple correct options</li>
                                <li><strong><span class="badge me-2"
                                            :class="useUtils().bgQuestionTypeClass('Numerical')">Numerical</span>:</strong>
                                    Enter a numerical value</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Existing Quiz Interface -->
    <div v-else class="container my-4 px-0">
        <!-- Quiz Header -->
        <div class="card shadow mb-4">
            <div class="card-body px-4">
                <div class="row align-items-center">
                    <div class="col-auto">
                        <div class="d-flex align-items-center">
                            <img :src="profilePictureSrc.value + userData.profile_picture" alt="Profile Image"
                                class="rounded-circle me-3" style="width: 50px; height: 50px; object-fit: cover;" />
                            <div>
                                <div>Candidate Name: {{ userData.name }}</div>
                                <div>Quiz Name: {{ store.quizName }}</div>
                            </div>
                        </div>
                    </div>
                    <div class="col text-end">
                        <div class="timer">{{ store.formattedTime }}</div>
                        <div>Remaining Time</div>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-primary" @click="toggleCalculator">
                            <i class="bi bi-calculator"></i>
                        </button>
                    </div>

                    <!-- Calculator Modal -->
                    <div v-show="isCalculatorVisible">
                        <div class="modal d-block rounded-0" style="background-color: rgba(0, 0, 0, 0.4);">
                            <div class="modal-dialog">
                                <div class="modal-content rounded-0">
                                    <div class="modal-header">
                                        <h5 class="modal-title">Scientific Calculator</h5>
                                        <button type="button" class="btn-close" @click="toggleCalculator"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="container d-flex p-0 m-0">
                                        <iframe src="https://mynkpdr.github.io/scientific-calculator/"
                                            style="width: 100%; height: 301px; border: none;"></iframe>
                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-9 mb-4">
                <!-- Question Panel -->

                <div class="card shadow">
                    <div class="card-body px-4">
                        <div class="d-flex justify-content-between align-items-center mb-4">
                            <h5 class="card-title m-0">Q. {{ store.getCurrentQuestion().display_id }}</h5>
                            <div class="d-flex justify-content-between mb-3">
                                <span class="badge me-2"
                                    :class="useUtils().bgQuestionTypeClass(store.getCurrentQuestion().type)">
                                    {{ store.getCurrentQuestion().type }}
                                </span>
                                <span class="badge bg-success">
                                    {{ store.getCurrentQuestion().marks }} Marks
                                </span>
                            </div>
                        </div>

                        <p class="card-text">{{ store.getCurrentQuestion().statement }}</p>
                        <img v-if="store.getCurrentQuestion().question_image"
                            :src="questionImageSrc.value + (store.getCurrentQuestion().question_image)"
                            class="img-fluid mb-4" alt="Question Image"
                            style="max-width: 100%; max-height: 400px; object-fit: contain;" />

                        <div class="options flex-grow-1">
                            <!-- MCQ -->
                            <template v-if="store.getCurrentQuestion().type === 'MCQ'">
                                <div v-for="option in store.getCurrentQuestion().options" :key="option.id"
                                    class="form-check mb-3">
                                    <input class="form-check-input" type="radio"
                                        :name="'question' + store.getCurrentQuestion().id" :id="option.id"
                                        :value="option.id"
                                        :checked="store.getCurrentQuestionStatus().selected_values === option.id"
                                        @change="store.handleSelectAnswer(option.id)">
                                    <label class="form-check-label" :for="option.id">
                                        {{ option.text }}
                                    </label>
                                </div>
                            </template>

                            <!-- MSQ -->
                            <template v-if="store.getCurrentQuestion().type === 'MSQ'">
                                <div v-for="option in store.getCurrentQuestion().options" :key="option.id"
                                    class="form-check mb-3">
                                    <input class="form-check-input" type="checkbox" :id="option.id" :value="option.id"
                                       
                                        :checked="Array.isArray(store.getCurrentQuestionStatus().selected_values) && store.getCurrentQuestionStatus().selected_values.includes(option.id)"
                                        @change="(event) => store.handleMSQChange(option.id, event.target.checked)">
                                    <label class="form-check-label" :for="option.id">
                                        {{ option.text }}
                                    </label>
                                </div>
                            </template>

                            <!-- Numerical -->
                            <template v-if="store.getCurrentQuestion().type === 'Numerical'">
                                <input class="form-control" type="number"
                                    :value="store.getCurrentQuestionStatus().selected_values || ''"
                                    @input="(event) => store.handleSelectAnswer(event.target.value)">
                            </template>
                        </div>

                        <div class="d-flex gap-2 mt-4">
                            <button class="btn btn-success px-4" @click="store.handleSaveAndNext">
                                Save & Next
                            </button>
                            <button class='btn btn-warning' @click="store.handleMarkForReview">
                                Mark for Review & Next
                            </button>
                            <button class="btn btn-outline-danger" @click="store.handleClearResponse"
                                :disabled="!store.getCurrentQuestionStatus().selected_values">
                                Clear
                            </button>
                        </div>
                    </div>
                </div>

            </div>

            <!-- Question Grid -->
            <div class="col-md-3 mb-4">
                <div class="card shadow">
                    <div class="card-body px-4">
                        <h5 class="card-title mb-4">Question Overview</h5>
                        <div class="question-grid mb-4 flex-grow-1 overflow-auto">
                            <button v-for="question in store.questions" :key="question.id" class="btn"
                                :class="useUtils().btnQuestionStatusClass(store.quizState[question.id])"
                                @click="store.handleSelectQuestion(question.id)">
                                {{ question.display_id }}
                            </button>
                        </div>

                        <h6 class="mb-3 fw-bold">Question Summary</h6>
                        <div class="row row-cols-1 g-3">
                            <div class="col">
                                <div class="d-flex align-items-center">
                                    <div class="bg-light border rounded me-2" style="width: 20px; height: 20px;">
                                    </div>
                                    <small>Not Visited ({{ store.questionCounts.notVisited }})</small>
                                </div>
                            </div>
                            <div class="col">
                                <div class="d-flex align-items-center">
                                    <div class="bg-success rounded me-2" style="width: 20px; height: 20px;">
                                    </div>
                                    <small>Answered ({{ store.questionCounts.answered }})</small>
                                </div>
                            </div>
                            <div class="col">
                                <div class="d-flex align-items-center">
                                    <div class="bg-danger rounded me-2" style="width: 20px; height: 20px;">
                                    </div>
                                    <small>Not Answered ({{ store.questionCounts.notAnswered }})</small>
                                </div>
                            </div>
                            <div class="col">
                                <div class="d-flex align-items-center">
                                    <div class="bg-warning rounded me-2" style="width: 20px; height: 20px;">
                                    </div>
                                    <small>Marked ({{ store.questionCounts.markedForReview }})</small>
                                </div>
                            </div>
                        </div>


                        <button @click="showSubmitConfirmation()" class="btn btn-success mt-4">
                            Submit Quiz
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Submit Confirmation Modal -->
        <ConfirmationModal :visible="submitConfirmationVisible" title="Submit Quiz"
            message="Are you sure you want to submit your quiz? No changes will be allowed after submission."
            @close="closeSubmitModal" @confirm="submitQuiz">
            <div class="question-summary mt-3">
                <div class="row row-cols-2 g-3">
                    <div class="col">
                        <div class="d-flex align-items-center">
                            <div class="bg-light border rounded me-2" style="width: 20px; height: 20px;"></div>
                            <small>Not Visited ({{ store.questionCounts.notVisited }})</small>
                        </div>
                    </div>
                    <div class="col">
                        <div class="d-flex align-items-center">
                            <div class="bg-success rounded me-2" style="width: 20px; height: 20px;"></div>
                            <small>Answered ({{ store.questionCounts.answered }})</small>
                        </div>
                    </div>
                    <div class="col">
                        <div class="d-flex align-items-center">
                            <div class="bg-danger rounded me-2" style="width: 20px; height: 20px;"></div>
                            <small>Not Answered ({{ store.questionCounts.notAnswered }})</small>
                        </div>
                    </div>
                    <div class="col">
                        <div class="d-flex align-items-center">
                            <div class="bg-warning rounded me-2" style="width: 20px; height: 20px;"></div>
                            <small>Marked ({{ store.questionCounts.markedForReview }})</small>
                        </div>
                    </div>
                </div>
            </div>
        </ConfirmationModal>
    </div>
</template>
<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useQuizStore } from '@/store/quizStore';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '../../store/user';
import ConfirmationModal from '../../components/modals/ConfirmationModal.vue';
import { push } from 'notivue';
import useUtils from '../../utils/useUtils';
const start_quiz = ref(false)

const isCalculatorVisible = ref(false);
const toggleCalculator = () => {
    isCalculatorVisible.value = !isCalculatorVisible.value;
};
const instructionsRead = ref(false);

const isModalVisible = ref(false);
const ModalMessage = ref('');

const closeModal = () => {
    if (start_quiz.value) {
        isModalVisible.value = false;
    } else {
        isModalVisible.value = false;
        router.back() || router.push({ name: 'StudentDashboard' })
        push.info('Quiz cancelled')
    }
};

const handleConfirm = () => {
    if (!instructionsRead.value && !start_quiz.value) {
        push.error('Please read and accept the instructions to start the quiz');
        isModalVisible.value = false;
        return;
    }
    isModalVisible.value = false;
    takeQuiz();
    startTimer();
    start_quiz.value = true;
};

const userStore = useUserStore();
const userData = userStore.userData
const route = useRoute()
const router = useRouter()
const quizId = route.params.id;
const store = useQuizStore();
const submitConfirmationVisible = ref(false)
let timerInterval = null;



const showSubmitConfirmation = () => {
    submitConfirmationVisible.value = true
};

const closeSubmitModal = () => {
    submitConfirmationVisible.value = false
};

const startTimer = () => {
    timerInterval = setInterval(() => {
        store.decrementTimer();
        if (store.timeRemaining === 0) {
            clearInterval(timerInterval);
            store.handleSaveAndNext()
            submitQuiz()
            push.info("Time is up, the quiz has been submitted")
        }
    }, 1000);
};

const takeQuiz = async () => {
    try {
        const take_quiz_response = await axios.post(`/api/quizzes/${quizId}/take_quiz`);

        if (take_quiz_response.data.data.existing && take_quiz_response.data.data.existing_take_quiz_time_remaining > 0) {
            store.setTimeRemaining(take_quiz_response.data.data.existing_take_quiz_time_remaining);
            store.setTakeQuizID(take_quiz_response.data.data.existing_take_quiz_id)
            store.setQuizID(take_quiz_response.data.data.id)
            push.info("Quiz have been resumed")
            fetchQuestions();
        } else if (!take_quiz_response.data.data.existing && take_quiz_response.data.data.time_duration) {
            store.setTimeRemaining(take_quiz_response.data.data.time_duration);
            store.setTakeQuizID(take_quiz_response.data.data.take_quiz_id)
            store.setQuizID(take_quiz_response.data.data.id)
            fetchQuestions();
        }

    } catch (error) {
        throw error
    }
};

const isExistingTakeQuiz = async () => {
    try {
        const is_existing_response = await axios.post(`/api/quizzes/${quizId}/take_quiz/is_existing`);
        store.resetQuiz() // Reset the quiz state so that we can start fresh
        if (is_existing_response.data.data.quiz_mode.toLowerCase() === 'practice') {
            router.back() || router.push({ name: 'StudentDashboard' })
            push.error("This quiz is not available for exam")
        } else if (is_existing_response.data.data.quiz_mode.toLowerCase() === 'exam') {
            if (is_existing_response.data.data.existing) {
                ModalMessage.value = 'You were already doing this quiz. Do you want to resume?';
                isModalVisible.value = true;
                instructionsRead.value = true;
                start_quiz.value = true;
                store.quizState = is_existing_response.data.data.quiz_state
                store.totalMarks = is_existing_response.data.data.total_marks
            } else {
                ModalMessage.value = 'Are you sure you want to take this quiz?';
                store.setTimeRemaining(is_existing_response.data.data.time_duration);
                store.setQuiz(is_existing_response.data.data.name)
                store.totalMarks = is_existing_response.data.data.total_marks
            }



        } else {
            push.error("Quiz not available")
            router.back() || router.push({ name: 'StudentDashboard' })
        }


    } catch (error) {
        if (error.response.data.message === 'The quiz has expired') {
            router.back() || router.push({ name: 'StudentDashboard' })
            return;
        } else if (error.response.data.message === 'You have already completed this quiz') {
            router.back() || router.push({ name: 'StudentDashboard' })
            return;
        } else if (error.response.data.message === 'The quiz has not started yet') {
            router.back() || router.push({ name: 'StudentDashboard' })
            return;
        } else {
            throw error
        }
    }
};

const fetchQuestions = async () => {
    try {
        const response = await axios.get(`/api/quizzes/${quizId}/questions`);
        const data = response.data.data;
        store.setQuestions(data.questions);
        store.setStudent(userData.name);
        store.setChapter(data.chapter_name);
        store.setQuiz(data.name);

    } catch (error) {
        throw error
    }
};

const submitQuiz = async () => {
    try {
        // Fill skipped questions with default values
        store.questions.forEach(question => {
            if (!store.quizState[question.id]) {
                store.quizState[question.id] = { "answered": false, "selected_values": null };
            }
        });
        await axios.post(`/api/take_quiz/${store.take_quiz_id}/submit`, {
            "quiz_state": store.quizState,
        });
        store.resetQuiz();
        push.success("Quiz submitted successfully")
        push.info("You will be able to see your result after the quiz ends")
        router.push({ name: 'StudentDashboard' })
    } catch (error) {
        closeSubmitModal();
        throw error
    }
    submitConfirmationVisible.value = false
};

onMounted(() => {
    isExistingTakeQuiz()
});
onUnmounted(() => {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
});
</script>

<style scoped>
.modal.fade.show {
    display: block;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    transition: all 0.3s ease-in-out;
}


.question-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
    gap: 0.5rem;
}

.question-number {
    aspect-ratio: 1;
    min-width: 40px;
    font-weight: 500;
}

.current {
    outline: 3px solid #0d6efd !important;
    outline-offset: -3px;
}

.timer {
    font-family: monospace;
    font-size: 1.5rem;
    color: #0d6efd;
}
</style>