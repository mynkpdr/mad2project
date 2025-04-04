<template>
    <section class="section">
        <div class="row justify-content-center">
            <div class="col-lg-12">
                <div class="card shadow m-4 border-0">
                    <div class="card-body mx-4">
                        <div v-if="isEditing">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h2 class="card-title m-0">Edit Quiz</h2>
                            </div>
                            <form @submit.prevent="updateQuiz">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="quizName" class="form-label">Quiz Name</label>
                                            <input v-model="quiz.name"
                                                type="text" class="form-control" id="quizName" required>
                                        </div>
                                        <div class="mb-3">
                                            <label for="quizSubject" class="form-label">Subject</label>
                                            <select v-model="quiz.subject_id"
                                                class="form-select" id="quizSubject" required
                                                @change="updateQuizChapters">
                                                <option v-for="subject in subjects" :key="subject.id"
                                                    :value="subject.id">
                                                    {{ subject.name }}
                                                </option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label for="quizChapter" class="form-label">Chapter</label>
                                            <select v-model="quiz.chapter_id"
                                                class="form-select" id="quizChapter" required>
                                                <option v-for="chapter in quizChapters" :key="chapter.id"
                                                    :value="chapter.id">
                                                    {{ chapter.name }}
                                                </option>
                                            </select>
                                        </div>
                                        <div class="col">
                                            <div class="row">
                                                <div class="col-md-6 mb-3">
                                                    <label for="quizDifficultyLevel" class="form-label">Difficulty
                                                        Level</label>
                                                    <select
                                                        v-model="quiz.difficulty_level" class="form-select"
                                                        id="quizDifficultyLevel" required>
                                                        <option value="easy" class="text-success">
                                                            Easy
                                                        </option>
                                                        <option value="medium" class="text-warning">
                                                            Medium
                                                        </option>
                                                        <option value="hard" class="text-danger">
                                                            Hard
                                                        </option>
                                                        <option value="unset" class="text-secondary">
                                                            Unset
                                                        </option>
                                                    </select>

                                                </div>
                                                <div class="col-md-6 mb-3">
                                                    <label for="quizMode" class="form-label">Quiz Mode</label>
                                                    <select
                                                        v-model="quiz.quizMode" class="form-select" id="quizMode"
                                                        required>
                                                        <option value="practice">
                                                            Practice
                                                        </option>
                                                        <option value="exam">
                                                            Exam
                                                        </option>
                                                    </select>
                                                </div>

                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="col">
                                            <div class="row">
                                                <div class="col-md-6 mb-3">
                                                    <label for="quizDate" class="form-label">Date of Quiz</label>
                                                    <input v-model="quiz.date"
                                                        type="datetime-local" class="form-control" id="quizDate"
                                                        required :min="useDateFormatter().minDate()">
                                                </div>
                                                <div class="col-md-6 mb-3">
                                                    <label for="quizDuration" class="form-label">Time Duration
                                                        (minutes)</label>
                                                    <input
                                                        v-model="quiz.duration" type="number" class="form-control"
                                                        id="quizDuration" required>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mb-3">
                                            <label for="quizDescription" class="form-label">Description</label>
                                            <textarea v-model="quiz.description"
                                                class="form-control" id="quizDescription" rows="3" required></textarea>
                                        </div>
                                        <div class="d-flex justify-content-end gap-2">
                                            <button type="button" @click="router.back()"
                                                class="btn btn-outline-danger">Back</button>
                                            <button type="submit" class="btn btn-success">Save Changes</button>
                                        </div>
                                    </div>
                                </div>

                            </form>
                        </div>
                        <div v-else>
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h1 class="display-6 m-0">{{ quiz.name }}</h1>
                                <div>
                                    <button @click="toggleEdit" class="btn me-2 btn-success">
                                        <i class="bi bi-pencil-fill"></i> Edit
                                    </button>
                                    <button @click.prevent="openQuizDeleteModal(quiz.id)" class="btn btn-danger">
                                        <i class="bi bi-trash2-fill text-white"></i>
                                    </button>
                                </div>
                            </div>
                            <p class="lead mb-4">{{ quiz.description }}</p>
                            <div class="row mb-4">
                                <div class="col-md-4 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-calendar3 fs-4 me-2 text-primary"></i>
                                        <span>Created on {{ useDateFormatter().formatDate2(quiz.date_created) }}</span>
                                    </div>
                                </div>
                                <div class="col-md-4 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-calendar3 fs-4 me-2 text-primary"></i>
                                        <span>Quiz Starting on {{ useDateFormatter().formatDate2(quiz.date_of_quiz)
                                            }}</span>
                                    </div>
                                </div>
                                <div class="col-md-4 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-file-earmark-text fs-4 me-2 text-primary"></i>
                                        <span>{{ quiz.questions }} Questions</span>
                                    </div>
                                </div>
                            </div>
                            <div class="row px-2">
                                <div class="col text-start">
                                    <h3 class="card-title">Questions <router-link
                                            :to="{ 'name': 'AdminAdd', query: { 'tab': 'question', 'subject_id': quiz.subject_id, 'chapter_id': quiz.chapter_id } }"><i
                                                class="bi bi-plus-circle-fill text-success"></i></router-link></h3>
                                </div>

                                <div class="col text-end">
                                    <button @click.prevent="openCSVModal" class="btn btn-secondary"><i
                                            class="bi bi-filetype-csv"></i></button>
                                    <button @click.prevent="openJSONModal" class="btn btn-secondary mx-2"><i
                                            class="bi bi-filetype-json"></i></button>
                                </div>
                            </div>
                            <!-- Loader (spinner) -->
                            <div v-if="loading" class="d-flex justify-content-center align-items-center">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </div>
                            <table v-else ref="datatable" v-if="!loading">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Statement</th>
                                        <th>Type</th>
                                        <th>Marks</th>
                                        <th data-type="date" data-format="MMMM DD, YYYY hh:mm A">Date Created</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(question, index) in tableData" :key="index">
                                        <td>{{ question.id }}</td>
                                        <td>{{ question.question_statement }}</td>
                                        <td>{{ question.question_type }}</td>
                                        <td>{{ question.marks }}</td>
                                        <td>{{ useDateFormatter().formatDate2(question.date_created) }}</td>
                                        <td class="col d-flex align-items-center justify-content-center">
                                            <button data-action='AdminQuestion' :data-id=question.id
                                                class="btn btn-success btn-sm view-btn">
                                                <i class="bi bi-eye-fill"></i></button>
                                            <button data-action='AdminQuestion' :data-id=question.id
                                                class="btn btn-info btn-sm edit-btn">
                                                <i class="bi bi-pencil-square text-white"></i></button>
                                            <button
                                                :data-confirmation_message="`Are you sure you want to delete this question with ID ${question.id} ?`"
                                                :data-success_message="'Question with ID ' + question.id + ' has been deleted'"
                                                :data-delete_url="'/api/questions/' + question.id" :data-id=question.id
                                                class="btn btn-danger delete-btn btn-sm">
                                                <i class="bi bi-trash2-fill text-white"></i>
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <ConfirmationModal :visible="isQuizDeleteModalVisible" :message="QuizDeleteModalMessage"
        :title="'Confirm Deletion?'" :cancelText="'No'" :confirmText="'Yes'" @close="closeQuizDeleteModal"
        @confirm="handleQuizDeleteConfirm" />
    <ConfirmationModal :visible="isCSVModalVisible" :message="CSVModalMessage" :title="'CSV File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeCSVModal" @confirm="handleCSVConfirm" />
    <ConfirmationModal :visible="isJSONModalVisible" :message="JSONModalMessage" :title="'JSON File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeJSONModal" @confirm="handleJSONConfirm" />
</template>

<script setup>

import { computed, nextTick, onMounted, reactive, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { push } from 'notivue';
import axios from 'axios';
import { dataTableDefaults } from "@/utils/dataTableDefaults";
import ConfirmationModal from '../../components/modals/ConfirmationModal.vue';
import { useDateFormatter } from '../../utils/useDateFormatter';
import { useExport } from "../../utils/useExport";

const route = useRoute()
const router = useRouter()

const isEditing = ref(route.query.edit?.toLowerCase() === 'true')

const tableData = ref([]);
const datatable = ref(null);
const loading = ref(true);

const isQuizDeleteModalVisible = ref(false);
const QuizDeleteModalMessage = ref('');
const deleteQuizID = ref(null)
const openQuizDeleteModal = (id) => {
    deleteQuizID.value = id
    QuizDeleteModalMessage.value = 'Are you sure you want to delete this quiz?';
    isQuizDeleteModalVisible.value = true;
};

const closeQuizDeleteModal = () => {
    isQuizDeleteModalVisible.value = false;
};

const handleQuizDeleteConfirm = async () => {
    try {
        const response = await axios.delete(`/api/quizzes/${deleteQuizID.value}`);
        push.success("Successfully deleted the quiz")
        closeQuizDeleteModal()
        router.push({ name: 'AdminQuizzes' })
    } catch (error) {
        closeQuizDeleteModal();
        throw error;
    }
};

const {
    CSVModalMessage,
    JSONModalMessage,
    isCSVModalVisible,
    isJSONModalVisible,
    openCSVModal,
    openJSONModal,
    closeCSVModal,
    closeJSONModal,
    handleCSVConfirm,
    handleJSONConfirm,
} = useExport(datatable);


const quiz = reactive({
    id: '',
    name: '',
    subject_id: '',
    chapter_id: '',
    difficulty_level: '',
    date: '',
    date_of_quiz: '',
    duration: '',
    description: '',
    date_created: '',
    questions: 0,
    quizMode: ''
})
const quizChapters = computed(() => {
    const subject = subjects.value.find(s => s.id === quiz.subject_id)
    return subject ? subject.chapters : []
})
const subjects = ref([])
// Labels for DataTable
const labels = {
    placeholder: "Search for questions...",
    searchTitle: "Search within table",
    pageTitle: "Page {page}",
    perPage: "Questions per page",
    noRows: "No questions found",
    info: "Showing {start} to {end} of {rows} questions",
    noResults: "No question match your search query",
};

// Columns configuration
const columns = [
    {
        select: 4,
        sort: "desc" //default by date_created
    },
    {
        select: 5,
        sortable: false
    },
];

const toggleEdit = () => {
    router.push({ query: { ...route.query, edit: 'true' } })
}
watch(() => route.query.edit,
    (newEdit) => {
        isEditing.value = newEdit === 'true';
        if (!isEditing.value) {
            nextTick(() => {
                dataTableDefaults(datatable, labels, columns);
            });
        }
    }
);

const fetchQuiz = async () => {
    loading.value = true;
    try {
        const response = await axios.get(`/api/quizzes/${route.params.id}`)
        const data = response.data.data
        tableData.value = data.questions
        loading.value = false;
        // Initialize DataTable after DOM is updated
        await nextTick();
        dataTableDefaults(datatable, labels, columns);
        quiz.id = data.id
        quiz.name = data.name
        quiz.subject_id = data.subject_id
        quiz.chapter_id = data.chapter_id
        quiz.difficulty_level = data.difficulty_level.toLowerCase()
        quiz.date = useDateFormatter().convertToISOFormat(data.date_of_quiz)
        quiz.date_of_quiz = data.date_of_quiz
        quiz.duration = data.time_duration / 60
        quiz.description = data.description
        quiz.date_created = data.date_created
        quiz.quizMode = data.quiz_mode.toLowerCase()
        quiz.questions = data.questions.length
    } catch (error) {
        loading.value = false;
        throw error;
    }
}

const fetchSubjectsData = async () => {
    try {
        const response = await axios.get('/api/subjects')
        subjects.value = response.data.data
    } catch (error) {
        throw error;
    }
}
const updateQuiz = async () => {
    try {
        await axios.put(`/api/quizzes/${route.params.id}`, {
            name: quiz.name,
            chapter_id: quiz.chapter_id,
            difficulty_level: quiz.difficulty_level,
            date_of_quiz: quiz.date,
            time_duration: quiz.duration,
            description: quiz.description,
            quiz_mode: quiz.quizMode
        })
        push.success("Successfully edited the quiz")
    } catch (error) {
        throw error;
    }
}

onMounted(async () => {
    await fetchSubjectsData();
    fetchQuiz();
})
</script>