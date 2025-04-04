<template>
    <section class="section">
        <div class="row justify-content-center">
            <div class="col-lg-12">
                <div class="card shadow m-4 border-0">
                    <div class="card-body mx-4">
                        <div v-if="isEditing">
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h2 class="card-title m-0">Edit Question</h2>
                            </div>
                            <form @submit.prevent="updateQuestion">
                                <div class="row">
                                    <!-- Left Column -->
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <div class="row align-items-center mb-3">
                                                <div class="col-auto">
                                                    <label for="questionSubject" class="form-label mb-0">Subject</label>
                                                </div>
                                            </div>
                                            <select v-model="question.subject_id"
                                                class="form-select" id="questionSubject" required
                                                @change="updateQuestionChapters">
                                                <option v-for="subject in subjects" :key="subject.id"
                                                    :value="subject.id">
                                                    {{ subject.name }}
                                                </option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <div class="row align-items-center mb-3">
                                                <div class="col-auto">
                                                    <label for="questionChapter" class="form-label mb-0">Chapter</label>
                                                </div>
                                            </div>
                                            <select v-model="question.chapter_id"
                                                class="form-select" id="questionChapter" required>
                                                <option v-for="chapter in questionChapters" :key="chapter.id"
                                                    :value="chapter.id">
                                                    {{ chapter.name }}
                                                </option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <div class="row align-items-center mb-3">
                                                <div class="col-auto">
                                                    <label for="questionType" class="form-label mb-0">Question
                                                        Type</label>
                                                </div>
                                            </div>
                                            <select v-model="question.type"
                                                class="form-select" id="questionType" required>
                                                <option value="MCQ">Multiple Choice Question (MCQ)</option>
                                                <option value="MSQ">Multiple Select Question (MSQ)</option>
                                                <option value="Numerical">Numerical</option>
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label for="questionMarks" class="form-label mb-0">Marks</label>

                                            <input v-model="question.marks"
                                                type="number" class="form-control" id="questionMarks" min="1" required>
                                        </div>
                                        <div class="mb-3">
                                            <label for="questionImage" class="form-label">Question Image
                                                (optional)</label>
                                            <div class="dropzone d-flex justify-content-center align-items-center border rounded p-4"
                                                :class="{ 'dragover': isDragover }"
                                                @dragenter.prevent="isDragover = true"
                                                @dragleave.prevent="isDragover = false" @dragover.prevent
                                                @drop.prevent="onFileDrop">
                                                <div v-if="!selectedFile" class="text-center">
                                                    <i class="bi bi-cloud-upload fs-1"></i>
                                                    <p class="mt-2">Drag and drop your image here or click to select</p>
                                                    <input type="file" id="questionImage" ref="fileInput"
                                                        accept="image/*" @change="onFileSelected" class="d-none">
                                                    <button type="button" class="btn btn-outline-primary mt-2"
                                                        @click="$refs.fileInput.click()">
                                                        Select File
                                                    </button>
                                                </div>
                                                <div v-else class="text-center">
                                                    <img :src="previewImage" alt="Selected Image" class="img-fluid mb-2"
                                                        style="max-height: 200px;">
                                                    <p>{{ selectedFile.name }}</p>
                                                    <button type="button" class="btn btn-outline-danger mt-2"
                                                        @click="removeFile">
                                                        Remove File
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                        <div v-if="selectedFile" class="mb-3">
                                            <button type="button" class="btn btn-outline-success" @click="uploadFile">
                                                Upload Image
                                            </button>
                                        </div>
                                    </div>

                                    <!-- Right Column -->
                                    <div class="col-md-6">

                                        <div class="mb-3">
                                            <label for="questionText" class="form-label">Question Text</label>
                                            <textarea v-model="question.text"
                                                class="form-control" id="questionText" rows="3" required></textarea>
                                        </div>

                                        <div v-if="question.type !== 'Numerical'" class="mb-3">
                                            <label class="form-label me-2">Options</label>
                                            <div v-for="(option, index) in question.options" :key="index"
                                                class="input-group mb-2">
                                                <input
                                                    v-model="question.options[index]" type="text" class="form-control"
                                                    :placeholder="`Option ${index + 1}`" required>
                                                <button type="button" class="btn btn-outline-danger"
                                                    @click="removeOption(index)"><i
                                                        class="bi bi-trash2-fill"></i></button>
                                            </div>
                                            <button type="button" class="btn btn-outline-primary" @click="addOption"><i
                                                    class="bi bi-plus-circle-fill"></i></button>
                                        </div>
                                        <div v-if="question.type === 'MCQ'" class="mb-3">
                                            <label for="correctAnswer" class="form-label">Correct Answer</label>
                                            <select
                                                v-model="question.correctAnswer" class="form-select" id="correctAnswer"
                                                required>
                                                <option v-for="(option, index) in question.options" :key="index"
                                                    :value="index">
                                                    Option {{ index
                                                        + 1 }}
                                                </option>
                                            </select>
                                        </div>
                                        <div v-if="question.type === 'MSQ'" class="mb-3">
                                            <label class="form-label">Correct Answers</label>
                                            <div v-for="(option, index) in question.options" :key="index"
                                                class="form-check">
                                                <input class="form-check-input"
                                                    type="checkbox" :id="`correctAnswer${index}`"
                                                    v-model="question.correctAnswers" :value="index">
                                                <label class="form-check-label" :for="`correctAnswer${index}`">Option {{
                                                    index +
                                                    1 }}</label>
                                            </div>
                                        </div>
                                        <div v-if="question.type === 'Numerical'" class="mb-3">
                                            <label for="numericalAnswer" class="form-label">Numerical Answer</label>
                                            <input
                                                v-model="question.numericalAnswer" type="number" step="0.01"
                                                class="form-control" id="numericalAnswer" required>
                                        </div>
                                        <div class="mb-3">
                                            <label for="questionAnswerExplanation" class="form-label">Answer
                                                explanation</label>
                                            <textarea
                                                v-model="question.answer_explanation" class="form-control"
                                                id="questionAnswerExplanation" rows="3"></textarea>
                                        </div>
                                        <button type="submit" class="btn btn-success">Save Changes</button>
                                    </div>
                                </div>

                            </form>
                        </div>
                        <div v-else>
                            <div class="d-flex justify-content-between align-items-center mb-4">
                                <h1 class="display-6 m-0">Question</h1>
                                <div>
                                    <button @click="toggleEdit" class="btn me-2 btn-success">
                                        <i class="bi bi-pencil-fill"></i> Edit
                                    </button>
                                </div>
                            </div>
                            <div class="row mb-4">
                                <div class="col-md-6 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-book fs-4 me-2 text-primary"></i>
                                        <span>Subject: {{ subjectName }}</span>
                                    </div>
                                </div>
                                <div class="col-md-6 d-flex flex-column align-items-center">
                                    <div class="d-flex align-items-center justify-content-center">
                                        <i class="bi bi-file-earmark-text fs-4 me-2 text-primary"></i>
                                        <span>Chapter: {{ chapterName }}</span>
                                    </div>
                                </div>
                            </div>
                            <div class="container" style="max-width: 800px;">
                                <div class="d-flex flex-column gap-3 mb-5">
                                    <h4 class="text-center mb-2 mt-5">
                                        <span class="me-2">{{ question.text }}</span>
                                    </h4>
                                    <img v-if="question.image" :src="questionImageSrc + question.image"
                                        class="img-fluid mb-2" alt="Question Image"
                                        style="max-width: 100%; max-height: 400px; object-fit: contain;" />
                                    <div class="d-flex justify-content-between mb-3">
                                        <span class="badge" :class="useUtils().bgQuestionTypeClass(question.type)">
                                            {{ question.type }}
                                        </span>
                                        <span class="badge bg-success">
                                            {{ question.marks }} Marks
                                        </span>
                                    </div>
                                    <template v-if="question.type === 'MCQ'">
                                        <div v-for="(option, index) in question.options" :key="index"
                                            class="d-flex flex-column mb-3">
                                            <button :key="index"
                                                class="btn btn-lg rounded-0 fw-bold w-100 position-relative" :class="{
                                                    'btn-success': question.options[question.correctAnswer] === option,
                                                    'btn-danger': question.options[question.correctAnswer] !== option
                                                }">
                                                {{ option }}
                                            </button>
                                        </div>
                                    </template>
                                    <template v-else-if="question.type === 'MSQ'">
                                        <div v-for="(option, index) in question.options" :key="index"
                                            class="d-flex flex-column mb-3">
                                            <button :key="index"
                                                class="btn btn-lg rounded-0 fw-bold w-100 position-relative" :class="{
                                                    'btn-success': question.correctAnswers.includes(index),
                                                    'btn-danger': !question.correctAnswers.includes(index)
                                                }">
                                                {{ option }}
                                            </button>
                                        </div>
                                    </template>
                                    <template v-else-if="question.type === 'Numerical'">
                                        <div class="d-flex flex-column mb-3">
                                            <input
                                                class="form-control form-control-lg rounded-0 fw-bold is-valid bg-success text-white cursor-not-allowed"
                                                type="number" :disabled="true"
                                                :value="question.numericalAnswer">
                                        </div>
                                    </template>
                                    <div class="mt-4" v-if="question.answer_explanation">
                                        <h6 class="text-secondary">Answer Explanation:</h6>
                                        <p class="border text-secondary p-3 rounded">{{ question.answer_explanation }}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>

import { onMounted, ref, reactive, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { push } from 'notivue';
import axios from 'axios';
import router from '../../router';
import useUtils from '../../utils/useUtils';
const route = useRoute()

const subjects = ref([])
const question = reactive({
    subject_id: '',
    chapter_id: '',
    type: 'MCQ',
    text: '',
    options: [],
    image: null,
    marks: null,
    correctAnswer: null,
    correctAnswers: [],
    numericalAnswer: null,
    answer_explanation: ''
})

const questionChapters = computed(() => {
    const subject = subjects.value.find(s => s.id === question.subject_id)
    return subject ? subject.chapters : []
})

const updateQuestionChapters = () => {
    question.chapter_id = ''
}


const addOption = () => {
    question.options.push('')
}
const removeOption = (index) => {
    question.options.splice(index, 1)
    if (question.type === 'MCQ' && question.correctAnswer >= question.options.length) {
        question.correctAnswer = null
    }
    question.correctAnswers = question.correctAnswers.filter(i => i !== index)
}

const toggleEdit = () => {
    router.push({ query: { ...route.query, edit: 'true' } })
}
watch(() => route.query.edit,
    (newEdit) => {
        isEditing.value = newEdit === 'true';
    }
);
const isDragover = ref(false)
const selectedFile = ref(null)
const previewImage = ref(null)
const fileInput = ref(null)

const onFileSelected = (event) => {
    const file = event.target.files[0]
    if (file) {
        selectedFile.value = file
        previewImage.value = URL.createObjectURL(file)
        imageUploaded.value = false
    }
}

const onFileDrop = (event) => {
    isDragover.value = false
    const file = event.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
        selectedFile.value = file
        previewImage.value = URL.createObjectURL(file)
        imageUploaded.value = false
    }
}

const removeFile = () => {
    selectedFile.value = null
    previewImage.value = null
    question.image = null
    if (fileInput.value) {
        fileInput.value.value = ''
    }
}

const uploadFile = async () => {
    if (!selectedFile.value) return
    if (imageUploaded.value == true) {
        push.info("Image is already uploaded")
        return
    }
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('type', 'question_image');

    try {
        const response = await axios.post('/api/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
        })
        push.success("Image uploaded successfully")
        question.image = response.data.filename
        console.log(question.image)
    } catch (error) {
        throw error;
    }
}

const validateForm = () => {
    if (question.type !== 'Numerical' && question.options.length < 2) {
        push.error('Add at least 2 options')
        return false
    }
    if (question.type === 'MSQ' && question.correctAnswers.length === 0) {
        push.error('Select at least one correct answer')
        return false
    }
    return true
}


const updateQuestion = async () => {
    if (!validateForm()) return
    try {
        await axios.put(`/api/questions/${route.params.id}`, {
            chapter_id: question.chapter_id,
            question_type: question.type,
            question_statement: question.text,
            answer_explanation: question.answer_explanation,
            options: question.options,
            marks: question.marks,
            correct_answer: question.correctAnswer,
            question_image: question.image,
            correct_answers: question.correctAnswers,
            numerical_answer: question.numericalAnswer,
        })
        push.success("Successfully edited the question")
    } catch (error) {
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
const subjectName = ref(null)
const chapterName = ref(null)
const imageUploaded = ref(false)
const questionImageSrc = computed(() =>
    import.meta.env.VITE_CDN_URL + import.meta.env.VITE_QUESTION_IMAGE_UPLOAD_FOLDER
);
const fetchQuestion = async () => {
    try {
        const response = await axios.get(`/api/questions/${route.params.id}`)
        question.subject_id = response.data.data.subject_id
        question.chapter_id = response.data.data.chapter_id
        question.type = response.data.data.type
        question.text = response.data.data.statement
        question.answer_explanation = response.data.data.answer_explanation
        question.image = response.data.data.question_image
        question.marks = response.data.data.marks
        if (question.image) {
            const fullImageURL = questionImageSrc.value + response.data.data.question_image
            previewImage.value = fullImageURL
            selectedFile.value = fullImageURL
            selectedFile.name = fullImageURL
            imageUploaded.value = true
        }
        subjectName.value = subjects.value.find(s => s.id === question.subject_id).name
        chapterName.value = questionChapters.value.find(c => c.id === question.chapter_id).name
        let count = 0
        for (const option of response.data.data.options) {
            question.options.push(option.text)
            if (option.is_correct && response.data.data.type == "MCQ") {
                question.correctAnswer = count
            } else if (option.is_correct && response.data.data.type == "MSQ") {
                question.correctAnswers.push(count)
            }
            count += 1
        }
        if (response.data.data.type == "Numerical") {
            for (const numericalAnswer of response.data.data.correct_answers) {
                question.numericalAnswer = numericalAnswer
            }
        }
    } catch (error) {
        throw error;
    }
}


const isEditing = ref(route.query.edit?.toLowerCase() === 'true')

onMounted(async () => {
    await fetchSubjectsData();
    fetchQuestion();
})
</script>