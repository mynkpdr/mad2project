<template>
    <div class="container py-4">
        <div class="row">
            <div class="col-md-12 p-0">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h3 class="card-title">Leaderboard</h3>
                        <div class="d-flex gap-2">
                            <select @change="getLeaderboard"
                                class="form-select ms-4 form-select-sm w-auto" v-model="selected_quiz_mode"
                                aria-label="Select quiz mode">
                                <option value="exam">Exam</option>
                                <option value="practice">Practice</option>
                            </select>
                            <select @change="getLeaderboard"
                                class="form-select ms-2 form-select-sm w-auto" v-model="selected_days_ago"
                                aria-label="Select time range">
                                <option value="1">Past 24 hours</option>
                                <option value="7">Past week</option>
                                <option value="30">Past month</option>
                                <option value="90">Past 3 months</option>
                                <option value="180">Past 6 months</option>
                                <option value="365">Past 1 year</option>
                            </select>
                        </div>
                    </div>
                    <div class="card-body">
                        <!-- Loader (spinner) -->
                        <div v-if="loading" class="d-flex justify-content-center align-items-center">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>

                        <table v-else ref="datatable" v-if="!loading">
                            <thead>
                                <tr>
                                    <th class="text-center">Rank</th>
                                    <th class="text-center">Name</th>
                                    <th class="text-center">Total Points</th>
                                    <th class="text-center">Total Quizzes</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(student, index) in tableData" :key="index"
                                    :style="useUtils().rankStyle(index + 1)">
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
                                    <td class="text-center">
                                        <span class="badge bg-primary px-3 py-2">{{ student.points_earned }} pts</span>
                                    </td>
                                    <td class="text-center">{{ student.total_quizzes }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, nextTick } from "vue";
import axios from "axios";
import useUtils from "../../utils/useUtils";
import { dataTableDefaults } from "@/utils/dataTableDefaults";
const selected_days_ago = ref(1);
const selected_quiz_mode = ref('exam');
const tableData = ref([]);
const loading = ref(true);
const datatable = ref(null);

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
const columns = [];

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
        throw error
    }
};

onMounted(() => {
    getLeaderboard();
});
</script>
