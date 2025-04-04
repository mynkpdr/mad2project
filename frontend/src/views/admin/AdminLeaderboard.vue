<template>
    <section class="section">
        <div class="row">
            <div class="col-lg-12">
                <div class="card shadow m-4 border-0">
                    <div class="card-body">
                        <div class="row px-2">
                            <div class="col text-start">
                                <h3 class="card-title">Leaderboard</h3>
                            </div>
                            <div class="col text-end">
                                <select @change="getLeaderboard" class="form-select d-inline-block w-auto me-4"
                                    v-model="selected_quiz_mode" aria-label="Select quiz mode">
                                    <option value="exam">Exam</option>
                                    <option value="practice">Practice</option>
                                </select>
                                <select @change="getLeaderboard" class="form-select d-inline-block w-auto me-4"
                                    v-model="selected_days_ago" aria-label="Select time range">
                                    <option value="1">Today</option>
                                    <option value="7">Past week</option>
                                    <option value="30">Past month</option>
                                    <option value="90">Past 3 months</option>
                                    <option value="180">Past 6 months</option>
                                    <option value="365">Past 1 year</option>
                                </select>
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
                                    <th>Rank</th>
                                    <th>Name</th>
                                    <th>Total Points</th>
                                    <th>Total Quizzes</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(student, index) in tableData" :key="index"
                                    :style="useUtils().rankStyle(index + 1)">
                                    <td class="col-1">{{ student.student_id }}</td>
                                    <td class="col-1">{{ index + 1 }}<sup>{{ useUtils().getOrdinalSuffix(index + 1) }}</sup></td>
                                    <td style="vertical-align: middle; display: flex;">
                                        <div class="d-flex align-items-center justify-content-center">
                                            <img :src="profilePictureSrc.value + student.profile_picture"
                                                alt="Profile Image" class="rounded-circle me-3"
                                                style="width: 50px; height: 50px; object-fit: cover;" />
                                            <div>
                                                <div class="fw-bold">{{ student.name }}</div>
                                                <small class="text-secondary">
                                                    {{ student.username }}
                                                </small>
                                            </div>
                                        </div>
                                    </td>

                                    <td>
                                        <span class="badge bg-primary">{{ student.points_earned }}
                                            pts</span>
                                    </td>
                                    <td>
                                        {{ student.total_quizzes }}
                                    </td>
                                    <td class="col d-flex align-items-center justify-content-center">
                                        <button data-action='AdminStudentProfile' :data-id=student.student_id
                                            class="btn btn-success btn-sm view-btn">
                                            <i class="bi bi-eye-fill"></i></button>
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
import axios from "axios";
import useUtils from "../../utils/useUtils";
import { dataTableDefaults } from "@/utils/dataTableDefaults";
import { useExport } from "../../utils/useExport";
import ConfirmationModal from "../../components/modals/ConfirmationModal.vue";
const selected_days_ago = ref(1);
const selected_quiz_mode = ref('exam');
const tableData = ref([]);
const datatable = ref(null);
const loading = ref(true);

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
    placeholder: "Search for students...",
    searchTitle: "Search within table",
    pageTitle: "Page {page}",
    perPage: "Students per page",
    noRows: "No students found",
    info: "Showing {start} to {end} of {rows} students",
    noResults: "No student match your search query",
};

// Columns configuration
const columns = [
    {
        select: 4,
        sortable: false
    },
];


// Function to fetch leaderboard data
const getLeaderboard = async () => {
    loading.value = true;
    try {
        const response = await axios.get('/api/students/leaderboard', {
            params: {
                days_ago: selected_days_ago.value,
                quiz_mode: selected_quiz_mode.value
            }
        });
        tableData.value = response.data.data;
        loading.value = false;
        // Initialize DataTable after data is loaded
        await nextTick()
        dataTableDefaults(datatable, labels, columns);
    } catch (error) {
        loading.value = false;
        throw error;
    }
};

onMounted(() => {
    getLeaderboard();
});
</script>
