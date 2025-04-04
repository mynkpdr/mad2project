<template>
    <div class="container my-4 px-0">
        <div class="row">
            <StudentSidebar />
            <div class="col-md-10">

                <!-- Quiz List -->
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0" v-if="props.isAdmin">Student's Quizzes <span class="fs-6 text-warning"
                            v-if="pending_result">( Pending Results )</span></h5>
                        <h5 class="card-title mb-0" v-else>My Quizzes <span class="fs-6 text-warning"
                            v-if="pending_result">( Pending Results )</span></h5>
                        <div class="d-flex gap-2">
                            <button v-if="selectedQuizMode || selectedStatus" @click="resetFilters"
                                class="btn btn-danger w-100 btn-sm">Reset</button>
                            <select @change="applyFilters" v-model="selectedQuizMode"
                                class="form-select ms-2 form-select-sm w-auto">
                                <option value="">All Types</option>
                                <option value="exam">Exam</option>
                                <option value="practice">Practice</option>
                            </select>
                            <select @change="applyFilters" v-model="selectedStatus"
                                class="form-select ms-0 form-select-sm w-auto">
                                <option value="">All Status</option>
                                <option value="completed">Completed</option>
                                <option value="incomplete">Incomplete</option>
                            </select>
                            <button @click.prevent="openCSVModal" class="btn btn-secondary border-light btn-sm mx-0"><i
                                    class="bi bi-filetype-csv"></i></button>
                            <button @click.prevent="openJSONModal" class="btn btn-secondary border-light btn-sm mx-0"><i
                                    class="bi bi-filetype-json"></i></button>
                        </div>
                    </div>

                    <div class="card-body">
                        <p class="text-secondary">Here you can find a list of all your quizzes. You can filter the quizzes
                            by type (Exam or Practice) and status (Completed or Incomplete). You can also export the
                            quiz data in CSV or JSON format.</p>
                            <!-- Loader (spinner) -->
                            <div v-if="loading" class="d-flex justify-content-center align-items-center">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </div>
                        <!-- DataTable -->
                        <table v-else ref="datatable" v-if="!loading">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Quiz Name</th>
                                    <th>Type</th>
                                    <th data-type="date" data-format="MMMM DD, YYYY hh:mm A">Date Taken</th>
                                    <th>Score</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="quiz in tableData" :key="quiz.quiz_id">
                                    <td>{{ quiz.take_quiz_id }}</td>
                                    <td>{{ quiz.quiz_name }}</td>
                                    <td>
                                        <span class="badge"
                                            :class="quiz.quiz_mode === 'exam' ? 'bg-danger' : 'bg-success'">
                                            {{ quiz.quiz_mode.charAt(0).toUpperCase() + quiz.quiz_mode.slice(1) }}
                                        </span>
                                    </td>
                                    <td>{{ useDateFormatter().formatDate2(quiz.date_taken) }}</td>
                                    <td>
                                        <div class="progress-wrapper">
                                            <div class="progress" style="height: 20px;">
                                                <div class="progress-bar" role="progressbar"
                                                    :style="useUtils().scoreStyle(quiz.total_scored)"></div>
                                            </div>
                                            <span class="score-text">{{ quiz.total_scored || quiz.total_scored == 0 ?
                                                quiz.total_scored : 'NA'
                                                }}%</span>
                                        </div>
                                    </td>
                                    <td>
                                        <span class="badge" :class="quiz.completed ? 'bg-success' : 'bg-warning'">
                                            {{ quiz.completed ? 'Completed' : 'Incomplete' }}
                                        </span>
                                    </td>
                                    <td>
                                        <button data-action='StudentQuizResults' :data-id=quiz.take_quiz_id
                                            class="btn btn-sm view-btn btn-success me-2">
                                            <i class="bi bi-eye-fill"></i></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <ConfirmationModal :visible="isCSVModalVisible" :message="CSVModalMessage" :title="'CSV File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeCSVModal" @confirm="handleCSVConfirm" />
    <ConfirmationModal :visible="isJSONModalVisible" :message="JSONModalMessage" :title="'JSON File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeJSONModal" @confirm="handleJSONConfirm" />
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import StudentSidebar from '../../../components/StudentSidebar.vue';
import { dataTableDefaults } from "@/utils/dataTableDefaults";
import { useDateFormatter } from '../../../utils/useDateFormatter';
import axios from 'axios';
import useUtils from '../../../utils/useUtils';
import { useExport } from "../../../utils/useExport";
import ConfirmationModal from '../../../components/modals/ConfirmationModal.vue';
import { useRoute } from 'vue-router';
const datatable = ref(null);
const loading = ref(true);
const selectedQuizMode = ref('');
const selectedStatus = ref('');
const pending_result = ref(false);
const route = useRoute()
const tableData = ref([])
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
// Labels for DataTable
const labels = {
    placeholder: "Search quizzes...",
    searchTitle: "Search within table",
    pageTitle: "Page {page}",
    perPage: "Quizzes per page",
    noRows: "No quizzes found",
    info: "Showing {start} to {end} of {rows} quizzes",
    noResults: "No results match your search criteria",
};

const props = defineProps({
    isAdmin: {
        type: Boolean,
        default: false
    },
    studentId: {
        type: Number,
        default: null
    }
});

// Columns configuration
const columns = [
    {
        select: 3,
        sort: "desc", // Default sorted by date
    },
    {
        select: 6, // Actions column
        sortable: false,
    }
];


const resetFilters = () => {
    selectedQuizMode.value = '';
    selectedStatus.value = '';

    applyFilters();
};

// Function to apply filters
const applyFilters = () => {
    if (datatable.value && datatable.value.simpleDatatables) {
        const dt = datatable.value.simpleDatatables;
        if (!selectedQuizMode.value && !selectedStatus.value) {
            dt.multiSearch([{ terms: [''], columns: [] }]);  // Clear search
        } else {
            const filters = []
            if (selectedQuizMode.value) {
                filters.push({
                    terms: [selectedQuizMode.value],
                    columns: [2] // Type column
                });
            }

            if (selectedStatus.value) {
                filters.push({
                    terms: [selectedStatus.value],
                    columns: [5] // Status column
                });
            }
            if (filters.length) {
                dt.multiSearch(filters);
            }
        }
    }
};

// Function to fetch quiz data
const getQuizzes = async () => {
    loading.value = true;
    try {
        if (props.isAdmin) {
            const response = await axios.get("/api/students/take_quizzes", {
                params: {
                    student_id: props.studentId
                }
            });
            tableData.value = response.data.data;
            loading.value = false;
            pending_result.value = response.data.data.some(quiz => quiz.pending_result);
            await nextTick();
            dataTableDefaults(datatable, labels, columns);
        } else {
            const response = await axios.get("/api/students/take_quizzes");
            tableData.value = response.data.data;
            loading.value = false;
            pending_result.value = response.data.data.some(quiz => quiz.pending_result);
            await nextTick();
            dataTableDefaults(datatable, labels, columns);
        }

    } catch (error) {
        loading.value = false;
        throw error;
    }
};

onMounted(() => {
    getQuizzes();
});
</script>
<style scoped>
.progress-wrapper {
    position: relative;
    width: 100%;
}

.score-text {
    position: absolute;
    left: 50%;
    top: 50%;
    font-size: 12px;
    transform: translate(-50%, -50%);
    color: #000;
}
</style>