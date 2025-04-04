<template>
    <section class="section">
        <div class="row justify-content-center">
            <div class="col-lg-12">
                <div class="card shadow m-4 border-0">
                    <div class="card-body mx-4">
                        <div v-if="isEditing">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h2 class="card-title m-0">Edit Subject</h2>
                            </div>
                            <form @submit.prevent="updateSubject">
                                <div class="mb-3">
                                    <label for="subjectName" class="form-label">Subject Name</label>
                                    <input v-model="subject.name" type="text" class="form-control"
                                        id="subjectName" required>
                                </div>
                                <div class="mb-3">
                                    <label for="subjectDescription" class="form-label">Description</label>
                                    <textarea v-model="subject.description"
                                        class="form-control" id="subjectDescription" rows="3" required></textarea>
                                </div>
                                <div class="d-flex justify-content-end gap-2">
                                    <button type="button" @click="router.back()"
                                        class="btn btn-outline-danger">Cancel</button>
                                    <button type="submit" class="btn btn-success">Save Changes</button>
                                </div>
                            </form>
                        </div>
                        <div v-else>
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h1 class="display-6 m-0">{{ subject.name }}</h1>
                                <div>
                                    <button @click="toggleEdit" class="btn me-2 btn-success">
                                        <i class="bi bi-pencil-fill"></i> Edit
                                    </button>
                                </div>
                            </div>
                            <p class="lead mb-4">{{ subject.description }}</p>
                            <div class="row mb-4">
                                <div class="col-md-6 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-calendar3 fs-4 me-2 text-primary"></i>
                                        <span>Created on {{ useDateFormatter().formatDate2(subject.date_created)
                                            }}</span>
                                    </div>
                                </div>
                                <div class="col-md-6 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-file-earmark-text fs-4 me-2 text-primary"></i>
                                        <span>{{ subject.chapters.length }} Questions</span>
                                    </div>
                                </div>
                            </div>
                            <div class="row px-2">
                                <div class="col text-start">
                                    <h3 class="card-title">Chapters <router-link
                                            :to="{ 'name': 'AdminAdd', query: { 'tab': 'chapter', 'subject_id': subject.id } }"><i
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
                                        <th>Name</th>
                                        <th data-type="date" data-format="MMMM DD, YYYY hh:mm A">Date Created</th>
                                        <th>Questions</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(chapter, index) in tableData" :key="index">
                                        <td>{{ chapter.id }}</td>
                                        <td>{{ chapter.name }}</td>
                                        <td>{{ useDateFormatter().formatDate2(chapter.date_created) }}</td>
                                        <td>{{ chapter.questions_count }}</td>
                                        <td class="col d-flex align-items-center justify-content-center">
                                            <button data-action='AdminChapter' :data-id=chapter.id
                                                class="btn btn-success btn-sm view-btn">
                                                <i class="bi bi-eye-fill"></i></button>
                                            <button data-action='AdminChapter' :data-id=chapter.id
                                                class="btn btn-info btn-sm edit-btn">
                                                <i class="bi bi-pencil-square text-white"></i></button>
                                            <button
                                                :data-confirmation_message="`Are you sure you want to delete this chapter with ID ${chapter.id} ?`"
                                                :data-success_message="'Chapter with ID ' + chapter.id + ' has been deleted'"
                                                :data-delete_url="'/api/chapters/' + chapter.id" :data-id=chapter.id
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
    <ConfirmationModal :visible="isCSVModalVisible" :message="CSVModalMessage" :title="'CSV File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeCSVModal" @confirm="handleCSVConfirm" />
    <ConfirmationModal :visible="isJSONModalVisible" :message="JSONModalMessage" :title="'JSON File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeJSONModal" @confirm="handleJSONConfirm" />
</template>

<script setup>
import ConfirmationModal from '../../components/modals/ConfirmationModal.vue';
import { ref, nextTick, onMounted, watch } from 'vue'
import { dataTableDefaults } from "@/utils/dataTableDefaults";
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { push } from 'notivue'
import { useDateFormatter } from '../../utils/useDateFormatter';
import { useExport } from '../../utils/useExport';

const route = useRoute()
const router = useRouter()

// Store the table data
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
    placeholder: "Search for chapters...",
    searchTitle: "Search within table",
    pageTitle: "Page {page}",
    perPage: "Chapters per page",
    noRows: "No chapters found",
    info: "Showing {start} to {end} of {rows} chapters",
    noResults: "No chapter match your search query",
};

// Columns configuration
const columns = [
    {
        select: 3,
        sort: "desc", // Default sorted by date_created
    },
    {
        select: 4,
        sortable: false,
        headerClass: "text-center",
        cellClass: "text-center"
    },
];


const isEditing = ref(route.query.edit?.toLowerCase() === 'true')
const subject = ref({
    id: null,
    name: '',
    description: '',
    date_created: '',
    chapters: []
})

const updateSubject = async () => {
    try {
        await axios.put(`/api/subjects/${route.params.id}`, subject.value)
        router.back()
        push.success("Successfully edited the subject")
    } catch (error) {
        throw error;
    }
}

const fetchSubject = async () => {
    loading.value = true;
    try {
        const response = await axios.get(`/api/subjects/${route.params.id}`)
        subject.value = response.data.data
        tableData.value = response.data.data.chapters;
        loading.value = false;
        // Initialize DataTable after DOM is updated
        await nextTick();
        dataTableDefaults(datatable, labels, columns);
    } catch (error) {
        loading.value = false;
        throw error;
    }
}

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


onMounted(() => {
    fetchSubject();
})
</script>
