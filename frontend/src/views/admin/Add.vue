<template>
  <section class="section">
    <div class="row">
      <div class="col-lg-12">
        <div class="card shadow m-4 border-0">
          <div class="card-body">
      
              <!-- Navigation Tabs -->
              <ul class="nav nav-tabs mb-4">
                <li class="nav-item" v-for="tab in tabs" :key="tab">
                  <a class="nav-link" :class="{ active: activeTab === tab }" href="#" @click.prevent="activeTab = tab">
                    {{ tab }}
                  </a>
                </li>
              </ul>

              <!-- Subject Form -->
              <div v-if="activeTab === 'Subject'" class="card">
                <div class="card-body">
                  <h2 class="card-title mb-4">Add a Subject</h2>
                  <form @submit.prevent="addSubject">
                    <div class="mb-3">
                      <label for="subjectName" class="form-label">Subject Name</label>
                      <input v-model="subject.name" type="text"
                        class="form-control" id="subjectName" required>
                    </div>
                    <div class="mb-3">
                      <label for="subjectDescription" class="form-label">Description</label>
                      <textarea v-model="subject.description"
                        class="form-control" id="subjectDescription" rows="3" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-outline-success">Add Subject</button>
                  </form>
                </div>
              </div>

              <!-- Chapter Form -->
              <div v-if="activeTab === 'Chapter'" class="card">
                <div class="card-body">
                  <h2 class="card-title mb-4">Add a Chapter</h2>
                  <form @submit.prevent="addChapter">
                    <div class="mb-3">
                      <label for="chapterSubject" class="form-label">Subject</label>
                      <select v-model="chapter.subject_id" class="form-select"
                        id="chapterSubject" required>
                        <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                          {{ subject.name }}
                        </option>
                      </select>
                    </div>
                    <div class="mb-3">
                      <label for="chapterName" class="form-label">Chapter Name</label>
                      <input v-model="chapter.name" type="text"
                        class="form-control" id="chapterName" required>
                    </div>
                    <div class="mb-3">
                      <label for="chapterDescription" class="form-label">Description</label>
                      <textarea v-model="chapter.description"
                        class="form-control" id="chapterDescription" rows="3" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-outline-success">Add Chapter</button>
                  </form>
                </div>
              </div>

              <!-- Quiz Form -->
              <div v-if="activeTab === 'Quiz'" class="card">
                <div class="card-body">
                  <h2 class="card-title mb-4">Add a Quiz</h2>
                  <form @submit.prevent="addQuiz">
                    <div class="row">
                      <div class="col-md-6">
                        <div class="mb-3">
                          <label for="quizName" class="form-label">Quiz Name</label>
                          <input v-model="quiz.name" type="text"
                            class="form-control" id="quizName" required>
                        </div>
                        <div class="mb-3">
                          <label for="quizSubject" class="form-label">Subject</label>
                          <select v-model="quiz.subject_id" class="form-select"
                            id="quizSubject" required @change="updateQuizChapters">
                            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                              {{ subject.name }}
                            </option>
                          </select>
                        </div>
                        <div class="mb-3">
                          <label for="quizChapter" class="form-label">Chapter</label>
                          <select v-model="quiz.chapter_id" class="form-select"
                            id="quizChapter" required>
                            <option v-for="chapter in quizChapters" :key="chapter.id" :value="chapter.id">
                              {{ chapter.name }}
                            </option>
                          </select>
                        </div>
                        <div class="col">
                          <div class="row">
                            <div class="col-md-6 mb-3">
                              <label for="quizDifficultyLevel" class="form-label">Difficulty Level</label>
                              <select v-model="quiz.difficulty_level"
                                class="form-select" id="quizDifficultyLevel" required>
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
                              <select v-model="quiz.quizMode"
                                class="form-select" id="quizMode" required>
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
                              <input v-model="quiz.date" type="datetime-local"
                                class="form-control" id="quizDate" required :min="useDateFormatter().minDate()">
                            </div>
                            <div class="col-md-6 mb-3">
                              <label for="quizDuration" class="form-label">Time Duration (minutes)</label>
                              <input v-model="quiz.duration" type="number"
                                class="form-control" id="quizDuration" required>
                            </div>
                          </div>
                        </div>
                        <div class="mb-3">
                          <label for="quizDescription" class="form-label">Description</label>
                          <textarea v-model="quiz.description"
                            class="form-control" id="quizDescription" rows="3" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-outline-success">Add Quiz</button>
                      </div>
                    </div>

                  </form>
                </div>
              </div>

              <!-- Question Form -->
              <div v-if="activeTab === 'Question'" class="card">
                <div class="card-body">
                  <h2 class="card-title mb-4">Add a Question</h2>
                  <form @submit.prevent="addQuestion">
                    <div class="row">
                      <!-- Left Column -->
                      <div class="col-md-6">
                        <div class="mb-3">
                          <div class="row align-items-center mb-3">
                            <div class="col-auto">
                              <label for="questionSubject" class="form-label mb-0">Subject</label>
                            </div>
                            <div class="col-auto ms-auto">
                              <button @click.prevent="subjectLock = !subjectLock" class="btn btn-sm"
                                :class="subjectLock ? 'btn-danger' : 'btn-outline-success'">
                                <span class="bi" :class="subjectLock ? 'bi-lock' : 'bi-unlock'"></span>
                              </button>
                            </div>
                          </div>
                          <select v-model="question.subject_id"
                            class="form-select" :disabled="subjectLock" id="questionSubject" required
                            @change="updateQuestionChapters">
                            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                              {{ subject.name }}
                            </option>
                          </select>
                        </div>

                        <div class="mb-3">
                          <div class="row align-items-center mb-3">
                            <div class="col-auto">
                              <label for="questionChapter" class="form-label mb-0">Chapter</label>
                            </div>
                            <div class="col-auto ms-auto">
                              <button @click.prevent="chapterLock = !chapterLock" class="btn btn-sm"
                                :class="chapterLock ? 'btn-danger' : 'btn-outline-success'">
                                <span class="bi" :class="chapterLock ? 'bi-lock' : 'bi-unlock'"></span>
                              </button>
                            </div>
                          </div>
                          <select v-model="question.chapter_id"
                            class="form-select" :disabled="chapterLock" id="questionChapter" required>
                            <option v-for="chapter in questionChapters" :key="chapter.id" :value="chapter.id">
                              {{ chapter.name }}
                            </option>
                          </select>
                        </div>

                        <div class="mb-3">
                          <div class="row align-items-center mb-3">
                            <div class="col-auto">
                              <label for="questionType" class="form-label mb-0">Question Type</label>
                            </div>
                            <div class="col-auto ms-auto">
                              <button @click.prevent="questionTypeLock = !questionTypeLock" class="btn btn-sm"
                                :class="questionTypeLock ? 'btn-danger' : 'btn-outline-success'">
                                <span class="bi" :class="questionTypeLock ? 'bi-lock' : 'bi-unlock'"></span>
                              </button>
                            </div>
                          </div>
                          <select v-model="question.type" class="form-select"
                            :disabled="questionTypeLock" id="questionType" required>
                            <option value="MCQ">Multiple Choice Question (MCQ)</option>
                            <option value="MSQ">Multiple Select Question (MSQ)</option>
                            <option value="Numerical">Numerical</option>
                          </select>
                        </div>

                        <div class="mb-3">
                          <div class="row align-items-center mb-3">
                            <div class="col-auto">
                              <label for="questionMarks" class="form-label mb-0">Marks</label>
                            </div>
                            <div class="col-auto ms-auto">
                              <button @click.prevent="marksLock = !marksLock" class="btn btn-sm"
                                :class="marksLock ? 'btn-danger' : 'btn-outline-success'">
                                <span class="bi" :class="marksLock ? 'bi-lock' : 'bi-unlock'"></span>
                              </button>
                            </div>
                          </div>
                          <input v-model="question.marks" type="number"
                            :disabled="marksLock" class="form-control" id="questionMarks" min="1" required>
                        </div>

                        <div class="mb-3">
                          <label for="questionImage" class="form-label">Question Image (optional)</label>
                          <div class="dropzone d-flex justify-content-center align-items-center border rounded p-4"
                            :class="{ 'dragover': isDragover }" @dragenter.prevent="isDragover = true"
                            @dragleave.prevent="isDragover = false" @dragover.prevent @drop.prevent="onFileDrop">
                            <div v-if="!selectedFile" class="text-center">
                              <i class="bi bi-cloud-upload fs-1"></i>
                              <p class="mt-2">Drag and drop your image here or click to select</p>
                              <input type="file" id="questionImage" ref="fileInput" accept="image/*"
                                @change="onFileSelected" class="d-none">
                              <button type="button" class="btn btn-outline-primary mt-2"
                                @click="$refs.fileInput.click()">
                                Select File
                              </button>
                            </div>
                            <div v-else class="text-center">
                              <img :src="previewImage" alt="Selected Image" class="img-fluid mb-2"
                                style="max-height: 200px;">
                              <p>{{ selectedFile.name }}</p>
                              <button type="button" class="btn btn-outline-danger mt-2" @click="removeFile">
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
                          <textarea v-model="question.text" class="form-control"
                            id="questionText" rows="3" required></textarea>
                        </div>

                        <div v-if="question.type !== 'Numerical'" class="mb-3">
                          <label class="form-label me-2">Options</label>
                          <div v-for="(option, index) in question.options" :key="index" class="input-group mb-2">
                            <input v-model="question.options[index]" type="text"
                              class="form-control" :placeholder="`Option ${index + 1}`" required>
                            <button type="button" class="btn btn-danger" @click="removeOption(index)"><i
                                class="bi bi-trash2-fill"></i></button>
                          </div>
                          <button type="button" class="btn btn-outline-primary" @click="addOption"><i
                              class="bi bi-plus-circle-fill"></i></button>
                        </div>

                        <div v-if="question.type === 'MCQ'" class="mb-3">
                          <label for="correctAnswer" class="form-label">Correct Answer</label>
                          <select v-model="question.correctAnswer"
                            class="form-select" id="correctAnswer" required>
                            <option v-for="(option, index) in question.options" :key="index" :value="index">
                              Option {{ index + 1 }}
                            </option>
                          </select>
                        </div>

                        <div v-if="question.type === 'MSQ'" class="mb-3">
                          <label class="form-label">Correct Answers</label>
                          <div v-for="(option, index) in question.options" :key="index" class="form-check">
                            <input class="form-check-input" type="checkbox"
                              :id="`correctAnswer${index}`" v-model="question.correctAnswers" :value="index">
                            <label class="form-check-label" :for="`correctAnswer${index}`">Option {{ index + 1
                              }}</label>
                          </div>
                        </div>

                        <div v-if="question.type === 'Numerical'" class="mb-3">
                          <label for="numericalAnswer" class="form-label">Numerical Answer</label>
                          <input v-model="question.numericalAnswer" type="number"
                            step="0.01" class="form-control" id="numericalAnswer" required>
                        </div>

                        <div class="mb-3">
                          <label for="questionAnswerExplanation" class="form-label">Answer explanation</label>
                          <textarea v-model="question.answer_explanation" class="form-control"
                            id="questionAnswerExplanation" rows="3"></textarea>
                        </div>

                        <button type="submit" class="btn btn-success">Add Question</button>
                      </div>
                    </div>
                  </form>
                </div>
              </div>
          
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { push } from 'notivue'
import { useDateFormatter } from '../../utils/useDateFormatter';

const tabs = ['Subject', 'Chapter', 'Quiz', 'Question']
const activeTab = ref('Subject')

const subjects = ref([])

const subjectLock = ref(false)
const chapterLock = ref(false)
const questionTypeLock = ref(false)
const marksLock = ref(false)
const subject = reactive({
  name: '',
  description: ''
})

const chapter = reactive({
  name: '',
  subject_id: '',
  description: ''
})

const quiz = reactive({
  name: '',
  subject_id: '',
  chapter_id: '',
  difficulty_level: 'easy',
  date: '',
  duration: '',
  description: '',
  quizMode: 'practice'
})

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
  answer_explanation: '',
})

const quizChapters = computed(() => {
  const subject = subjects.value.find(s => s.id === quiz.subject_id)
  return subject ? subject.chapters : []
})

const questionChapters = computed(() => {
  const subject = subjects.value.find(s => s.id === question.subject_id)
  return subject ? subject.chapters : []
})

const updateQuizChapters = () => {
  quiz.chapter_id = ''
}

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

const isDragover = ref(false)
const selectedFile = ref(null)
const previewImage = ref(null)
const fileInput = ref(null)

const onFileSelected = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    previewImage.value = URL.createObjectURL(file)
  }
}

const onFileDrop = (event) => {
  isDragover.value = false
  const file = event.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) {
    selectedFile.value = file
    previewImage.value = URL.createObjectURL(file)
  }
}

const removeFile = () => {
  selectedFile.value = null
  previewImage.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const uploadFile = async () => {
  if (!selectedFile.value) return

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

const addSubject = async () => {
  try {
    await axios.post('/api/subjects', {
      name: subject.name,
      description: subject.description
    })
    push.success('Successfully added new subject')
    resetForm(subject)
    fetchData()
  } catch (error) {
    throw error;
  }
}

const addChapter = async () => {
  try {
    await axios.post('/api/chapters', {
      name: chapter.name,
      subject_id: chapter.subject_id,
      description: chapter.description
    })
    push.success('Successfully added new chapter')
    resetForm(chapter)
    fetchData()
  } catch (error) {
    throw error;
  }
}

const addQuiz = async () => {
  try {
    await axios.post('/api/quizzes', {
      name: quiz.name,
      chapter_id: quiz.chapter_id,
      difficulty_level: quiz.difficulty_level,
      quiz_mode: quiz.quizMode,
      date_of_quiz: quiz.date,
      time_duration: quiz.duration,
      description: quiz.description
    })
    push.success('Successfully added new quiz')
    // resetForm(quiz)
  } catch (error) {
    throw error;
  }
}

const validateQuestion = () => {
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


const addQuestion = async () => {
  if (!validateQuestion()) return
  if (selectedFile.value && !question.image) {
    push.error("Please upload the image first")
    return
  }
  try {
    await axios.post('/api/questions', {
      chapter_id: question.chapter_id,
      question_type: question.type,
      question_statement: question.text,
      options: question.options,
      marks: question.marks,
      correct_answer: question.correctAnswer,
      question_image: question.image,
      correct_answers: question.correctAnswers,
      numerical_answer: question.numericalAnswer,
      answer_explanation: question.answer_explanation,
    })
    push.success('Successfully added a new question')
    resetForm(question)
  } catch (error) {
    throw error;
  }
}

const resetForm = (form) => {
  Object.keys(form).forEach(key => {
    if ( //Don't reset if locked
      (key === 'subject_id' && subjectLock.value) ||
      (key === 'chapter_id' && chapterLock.value) ||
      (key === 'type' && questionTypeLock.value) ||
      (key === 'marks' && marksLock.value)
    ) {
      return;
    }
    if (Array.isArray(form[key])) {
      form[key] = []; // Reset arrays
    } else if (form[key] !== null && typeof form[key] === 'object') {
      resetForm(form[key]); // Recursively reset nested objects
    } else {
      form[key] = ''; // Reset other values
    }
  });

  if (form === question) {
    if (!questionTypeLock.value) {
      form.type = 'MCQ'; // Set default only if not locked
    }
    form.image = null
    removeFile()
    form.correctAnswer = null;
    form.correctAnswers = [];
    form.numericalAnswer = null;
  }
};

const fetchData = async () => {
  try {
    const response = await axios.get('/api/subjects')
    subjects.value = response.data.data
  } catch (error) {
    throw error;
  }
}

onMounted(() => {
  fetchData()
  if (useRoute().query.tab) {
    if ((useRoute().query.tab).toLowerCase() === 'question') {
      activeTab.value = 'Question'
      if (useRoute().query.subject_id) {
        question.subject_id = parseInt(useRoute().query.subject_id)
        subjectLock.value = true
      }
      if (useRoute().query.chapter_id) {
        question.chapter_id = parseInt(useRoute().query.chapter_id)
        chapterLock.value = true
      }
    }
    else if ((useRoute().query.tab).toLowerCase() === 'chapter') {
      activeTab.value = 'Chapter'
      if (useRoute().query.subject_id) {
        chapter.subject_id = parseInt(useRoute().query.subject_id)
      }
    }
    else if ((useRoute().query.tab).toLowerCase() === 'quiz') {
      activeTab.value = 'Quiz'
    }
    else if ((useRoute().query.tab).toLowerCase() === 'subject') {
      activeTab.value = 'Subject'
    }
  }

})

watch(activeTab, () => {
  fetchData()
})
</script>

<style scoped>
.nav-tabs .nav-link {
  color: #6c757d;
}
</style>