<template>
    <section class="section">
        <div class="row">
            <div class="col-lg-12">
                <div class="card shadow m-4 border-0">
                    <div class="card-body">

                        <div class="row px-2">
                            <div class="col text-start">
                                <h3 class="card-title">Students</h3>
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
                                    <th>Picture</th>
                                    <th>Name</th>
                                    <th>Username</th>
                                    <th>Email</th>
                                    <th>Status</th>
                                    <th data-type="date" data-format="MMMM DD, YYYY hh:mm A">Date Created</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(student, index) in tableData" :key="index">
                                    <td>{{ student.id }}</td>
                                    <td><img :src="profilePictureSrc.value + student.profile_picture"
                                            alt="Profile Image" class="rounded-circle"
                                            style="width: 50px; height: 50px; object-fit: cover;" />
                                    </td>
                                    <td>{{ student.name }}</td>
                                    <td>{{ student.username }}</td>
                                    <td>{{ student.email }}</td>
                                    <td><span :class="{
                                        'badge': true,
                                        'bg-success': student.status.toLowerCase() === 'active',
                                        'bg-danger': student.status.toLowerCase() === 'suspended',
                                    }">
                                            {{ student.status }}
                                        </span></td>

                                    <td>{{ useDateFormatter().formatDate2(student.date_created) }}</td>
                                    <td class="col d-flex align-items-center justify-content-center">
                                        <button data-action='AdminStudentProfile' :data-id=student.id
                                            class="btn btn-success btn-sm view-btn">
                                            <i class="bi bi-eye-fill"></i></button>
                                        <button data-action='AdminStudentProfile' :data-id=student.id
                                            class="btn btn-info btn-sm edit-btn">
                                            <i class="bi bi-pencil-square text-white"></i></button>
                                        <button
                                            :data-confirmation_message="`Are you sure you want to delete this student with ID ${student.id} ?`"
                                            :data-success_message="'Student with ID ' + student.id + ' has been deleted'"
                                            :data-delete_url="'/api/students/' + student.id" :data-id=student.id
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



// Store the table data
const tableData = ref([]);

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
        select: 6,
        sort: "desc", // Default sorted by date_created
    },
    {
        select: 7,
        sortable: false
    },
    {
        select: 1,
        sortable: false
    },
];

// Function to fetch student data
const getStudents = async () => {
    loading.value = true;
    try {
        const response = await axios.get("/api/students");
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
    getStudents();
});
</script>
