<template>
    <section class="section">
        <div class="row justify-content-center">
            <div class="col-lg-12">
                <div class="card shadow m-4 border-0">
                    <div class="card-body mx-4">
                        <div v-if="isEditing">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h2 class="card-title m-0">Edit Chapter</h2>
                            </div>
                            <form @submit.prevent="updateChapter">
                                <div class="mb-3">
                                    <label for="chapterName" class="form-label">Chapter Name</label>
                                    <input v-model="chapter.name" type="text" class="form-control" id="chapterName"
                                        required>
                                </div>
                                <div class="mb-3">
                                    <label for="chapterDescription" class="form-label">Description</label>
                                    <textarea v-model="chapter.description" class="form-control" id="chapterDescription"
                                        rows="3" required></textarea>
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
                                <h1 class="display-6 m-0">{{ chapter.name }}</h1>
                                <div>
                                    <button @click="toggleEdit" class="btn me-2 btn-success">
                                        <i class="bi bi-pencil-fill"></i> Edit
                                    </button>
                                </div>
                            </div>
                            <p class="lead mb-4">{{ chapter.description }}</p>
                            <div class="row mb-4">
                                <div class="col-md-4 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-book fs-4 me-2 text-primary"></i>
                                        <span>Subject: {{ chapter.subject_name }}</span>
                                    </div>
                                </div>
                                <div class="col-md-4 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-calendar3 fs-4 me-2 text-primary"></i>
                                        <span>Created on {{ useDateFormatter().formatDate2(chapter.date_created)
                                            }}</span>
                                    </div>
                                </div>
                                <div class="col-md-4 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-clipboard fs-4 me-2 text-primary"></i>
                                        <span>{{ chapter.questions.length }} Questions</span>
                                    </div>
                                </div>
                            </div>

                            <div class="row px-2">
                                <div class="col text-start">
                                    <h3 class="card-title">Questions <router-link
                                            :to="{ 'name': 'AdminAdd', query: { 'tab': 'question', 'subject_id': chapter.subject_id, 'chapter_id': chapter.id } }"><i
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
    <ConfirmationModal :visible="isCSVModalVisible" :message="CSVModalMessage" :title="'CSV File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeCSVModal" @confirm="handleCSVConfirm" />
    <ConfirmationModal :visible="isJSONModalVisible" :message="JSONModalMessage" :title="'JSON File Confirmation'"
        :cancelText="'No'" :confirmText="'Yes'" @close="closeJSONModal" @confirm="handleJSONConfirm" />
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { push } from 'notivue'
import { dataTableDefaults } from "@/utils/dataTableDefaults";
import ConfirmationModal from '../../components/modals/ConfirmationModal.vue';
import { useDateFormatter } from '../../utils/useDateFormatter';
import { useExport } from '../../utils/useExport';
const route = useRoute()
const router = useRouter()

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
        sortable: false,
    },
];

const isEditing = ref(route.query.edit?.toLowerCase() === 'true')
const chapter = ref({
    id: null,
    name: '',
    description: '',
    date_created: '',
    questions: []
})

const updateChapter = async () => {
    try {
        await axios.put(`/api/chapters/${route.params.id}`, chapter.value)
        router.back()
        push.success("Successfully edited the chapter")
    } catch (error) {
        throw error;
    }
}

const fetchChapter = async () => {
    loading.value = true;
    try {
        const response = await axios.get(`/api/chapters/${route.params.id}`)
        chapter.value = response.data.data;
        tableData.value = response.data.data.questions;
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
watch(
    () => route.query.edit,
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
    fetchChapter();
})
</script>
