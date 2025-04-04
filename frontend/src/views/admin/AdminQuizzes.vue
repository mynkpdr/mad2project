<template>
    <section class="section">
        <div class="row">
            <div class="col-lg-12">
                <div class="card shadow m-4 border-0">
                    <div class="card-body">

                        <div class="row px-2">
                            <div class="col text-start">
                                <h3 class="card-title">Quizzes <router-link
                                        :to="{ 'name': 'AdminAdd', query: { 'tab': 'quiz' } }"><i
                                            class="bi bi-plus-circle-fill text-success"></i></router-link></h3>
                            </div>

                            <div class="col text-end">
                                <button @click.prevent="openCSVModal" class="btn export_csv btn-secondary"><i
                                        class="bi bi-filetype-csv"></i></button>
                                <button @click.prevent="openJSONModal" class="btn export_json btn-secondary mx-2"><i
                                        class="bi bi-filetype-json"></i></button>
                            </div>
                        </div>
                        <div class="row mb-3">
                            <div class="col-md-3">
                                <select class="form-select" v-model="selectedDifficulty" @change="applyFilters">
                                    <option value="">All Difficulties</option>
                                    <option value="easy">Easy</option>
                                    <option value="medium">Medium</option>
                                    <option value="hard">Hard</option>
                                    <option value="unset">Unset</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <select class="form-select" v-model="selectedQuizMode" @change="applyFilters">
                                    <option value="">All Quiz Modes</option>
                                    <option value="practice">Practice</option>
                                    <option value="exam">Exam</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <select class="form-select" v-model="selectedStatus" @change="applyFilters">
                                    <option value="">All Status</option>
                                    <option value="upcoming">Upcoming</option>
                                    <option value="live">Live</option>
                                    <option value="completed">Completed</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <button v-if="selectedStatus || selectedDifficulty || selectedQuizMode"
                                    @click="resetFilters" class="btn btn-danger">Reset</button>
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
                                    <th>Name</th>
                                    <th>Difficulty</th>
                                    <th>Quiz Mode</th>
                                    <th>Status</th>
                                    <th data-type="date" data-format="MMMM DD, YYYY hh:mm A">Date of Quiz</th>
                                    <th>Time Duration</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(quiz, index) in tableData" :key="index">
                                    <td>{{ quiz.id }}</td>
                                    <td>{{ quiz.name }}</td>
                                    <td>
                                        <span class="badge"
                                            :class="useUtils().bgDifficultyTypeClass(quiz.difficulty_level)">
                                            {{ quiz.difficulty_level }}
                                        </span>
                                    </td>
                                    <td>
                                        <span class="badge" :class="useUtils().bgQuizModeClass(quiz.quiz_mode)">
                                            {{ quiz.quiz_mode }}
                                        </span>

                                    </td>
                                    <td>
                                        <span class="badge" :class="useUtils().bgQuizStatusClass(quiz.status)">
                                            {{ quiz.status }}
                                        </span>
                                    </td>
                                    <td>{{ useDateFormatter().formatDate2(quiz.date_of_quiz) }}
                                    </td>
                                    <td>{{ quiz.time_duration / 60 }}</td>
                                    <td class="col d-flex align-items-center justify-content-center">
                                        <button data-action='AdminQuiz' :data-id=quiz.id
                                            class="btn btn-success btn-sm view-btn">
                                            <i class="bi bi-eye-fill"></i></button>
                                        <button data-action='AdminQuiz' :data-id=quiz.id
                                            class="btn btn-info btn-sm edit-btn">
                                            <i class="bi bi-pencil-square text-white"></i></button>
                                        <button
                                            :data-confirmation_message="`Are you sure you want to delete this quiz with ID ${quiz.id} ?`"
                                            :data-success_message="'Quiz with ID ' + quiz.id + ' has been deleted'"
                                            :data-delete_url="'/api/quizzes/' + quiz.id" :data-id=quiz.id
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
    </section>
    <ConfirmationModal :visible="isCSVModalVisible" :message="CSVModalMessage" :title="'CSV File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeCSVModal" @confirm="handleCSVConfirm" />
    <ConfirmationModal :visible="isJSONModalVisible" :message="JSONModalMessage" :title="'JSON File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeJSONModal" @confirm="handleJSONConfirm" />

</template>

<script setup>
import { onMounted, ref, nextTick } from "vue";
import { dataTableDefaults } from "@/utils/dataTableDefaults";
import axios from "axios";
import { useExport } from "../../utils/useExport";
import ConfirmationModal from "../../components/modals/ConfirmationModal.vue";

import { useDateFormatter } from "../../utils/useDateFormatter";
import useUtils from "../../utils/useUtils";

const loading = ref(true);

const datatable = ref(null);

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


// Store the table data
const tableData = ref([]);
const selectedDifficulty = ref('');
const selectedQuizMode = ref('');
const selectedStatus = ref('');
// Labels for DataTable
const labels = {
    placeholder: "Search for quizzes...",
    searchTitle: "Search within table",
    pageTitle: "Page {page}",
    perPage: "Quizzes per page",
    noRows: "No quizzes found",
    info: "Showing {start} to {end} of {rows} quizzes",
    noResults: "No quiz match your search query",
};

// Columns configuration
const columns = [
    {
        select: 0,
        sort: "desc", // Default sorted by id
    },
    {
        select: 7,
        sortable: false
    },
];


// Function to apply filters
const applyFilters = () => {
    if (datatable.value && datatable.value.simpleDatatables) {
        const dt = datatable.value.simpleDatatables;
        if (!selectedDifficulty.value && !selectedQuizMode.value && !selectedStatus.value) {
            dt.multiSearch([{ terms: [''], columns: [] }]);  // Clear search
        } else {
            const filters = [];
            if (selectedDifficulty.value) {
                filters.push({
                    terms: [selectedDifficulty.value],
                    columns: [2]
                });
            }
            if (selectedQuizMode.value) {
                filters.push({
                    terms: [selectedQuizMode.value],
                    columns: [3]
                });
            }
            if (selectedStatus.value) {
                filters.push({
                    terms: [selectedStatus.value],
                    columns: [4]
                });
            }

            if (filters.length) {
                dt.multiSearch(filters);
            }
        }
    }
};

const resetFilters = () => {
    selectedDifficulty.value = '';
    selectedQuizMode.value = '';
    selectedStatus.value = '';
    applyFilters();
};


// Function to fetch quiz data
const getQuizzes = async () => {
    loading.value = true;
    try {
        const response = await axios.get("/api/quizzes");
        tableData.value = response.data.data;
        loading.value = false;
        // Initialize DataTable after DOM is updated
        await nextTick();
        dataTableDefaults(datatable, labels, columns);
    } catch (error) {
        loading.value = false;
        throw error;
    }
};


onMounted(() => {
    getQuizzes();
});
</script>
