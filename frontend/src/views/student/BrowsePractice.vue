<template>
    <div class="container py-4">
        <div class="row">
            <!-- Filter Sidebar -->
            <div class="col-md-3 ps-0">
                <div class="card">
                    <div class="card-header">
                        <h5 class="card-title mb-0">Filters</h5>
                    </div>
                    <div class="card-body">
                        <!-- Search Bar -->
                        <div class="mb-4">
                            <div class="input-group">
                                <span class="input-group-text border-end-0">
                                    <i class="bi bi-search"></i>
                                </span>
                                <input type="text"
                                    class="form-control form-control-sm" placeholder="Search practices..."
                                    v-model="filters.search">
                            </div>
                        </div>

                        <div class="mb-4">
                            <label class="mb-2">Subject</label>
                            <select class="form-select form-select-sm"
                                v-model="filters.subject">
                                <option value="">All Subjects</option>
                                <option v-for="cat in subjects" :key="cat" :value="cat">{{ cat }}</option>
                            </select>
                        </div>

                        <div class="mb-4">
                            <label class="mb-2">Difficulty</label>
                            <div class="btn-group d-flex" role="group">
                                <button class="btn btn-outline-primary btn-sm mb-2"
                                    :class="{ 'btn-primary text-white': filters.difficulty === difficulty }"
                                    @click="toggleDifficulty(difficulty)" v-for="difficulty in difficulties"
                                    :key="difficulty">
                                    {{ difficulty.charAt(0).toUpperCase() + difficulty.slice(1) }}
                                </button>
                            </div>
                        </div>

                        <div class="mb-4">
                            <label class="mb-2">Status</label>
                            <div class="row p-2">
                                <button class="btn btn-outline-primary btn-sm mb-2"
                                    :class="{ 'btn-primary text-white': filters.status === status }"
                                    @click="toggleStatus(status)" v-for="status in statuses" :key="status">
                                    <i class="bi" :class="getStatusIcon(status)"></i>
                                    {{ status.charAt(0).toUpperCase() + status.slice(1) }}
                                </button>
                            </div>
                        </div>

                        <div class="mb-4">
                            <label class="mb-2">Duration</label>
                            <select class="form-select form-select-sm"
                                v-model="filters.timeRange">
                                <option value="">Any Duration</option>
                                <option value="0-15">0-15 minutes</option>
                                <option value="15-30">15-30 minutes</option>
                                <option value="30-60">30-60 minutes</option>
                                <option value="60+">60+ minutes</option>
                            </select>
                        </div>

                        <div class="mb-4">
                            <label class="mb-2">Sort By</label>
                            <div class="d-flex align-items-center">
                                <!-- Sort By Dropdown -->
                                <select class="form-select form-select-sm me-2"
                                    v-model="filters.sortBy">
                                    <option value="date">Date</option>
                                    <option value="newest">Newest First</option>
                                    <option value="oldest">Oldest First</option>
                                    <option value="name">Quiz Name</option>
                                    <option value="duration">Duration</option>
                                </select>

                                <!-- Sort Direction Buttons -->
                                <button type="button" class="btn btn-sm btn-outline-primary me-2"
                                    @click="filters.sortDirection = 'asc'">
                                    <i class="bi bi-sort-up"></i>
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-primary"
                                    @click="filters.sortDirection = 'desc'">
                                    <i class="bi bi-sort-down"></i>
                                </button>
                            </div>
                        </div>


                        <button class="btn btn-danger btn-sm w-100" @click="resetFilters" v-if="hasActiveFilters">
                            <i class="bi bi-x-circle me-1"></i> Clear All Filters
                        </button>
                    </div>
                </div>
            </div>

            <!-- Main Content -->
            <div class="col-md-9 pe-0">

                <!-- Active Filters -->
                <div v-if="hasActiveFilters" class="card mb-4">
                    <div class="card-header p-0 border-0">
                        <h6 class="p-2 card-title mb-0 text-secondary">Active Filters:
                            <button v-for="(value, key) in activeFilters" :key="key"
                                class="btn btn-sm btn-outline-primary me-2" @click="removeFilter(key)">
                                {{ key.charAt(0).toUpperCase() + key.slice(1) }}: {{
                                    value.charAt(0).toUpperCase() +
                                    value.slice(1) }} <i class="bi bi-x"></i>
                            </button>
                            <button class="btn btn-sm btn-danger" @click="resetFilters">
                                <i class="bi bi-x-circle me-1"></i> Clear
                            </button>
                        </h6>
                    </div>
                </div>

                <!-- Results Grid -->
                <div class="row">
                    <div v-if="loading" class="text-center">
                        <div class="spinner-border" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </div>

                    <template v-else-if="filteredPractices.length">
                        <div v-for="quiz in filteredPractices" :key="quiz.id" class="col-md-6 mb-4">
                            <div class="card">

                                <div class="card-header">
                                    <h5 class="card-title mb-0">{{ quiz.name }}</h5>
                                </div>
                                <div class="card-body">
                                    <p class="card-text text-secondary">{{ quiz.description }}</p>

                                    <div class="mb-3">
                                        <div class="d-flex align-items-center mb-2">
                                            <i class="bi bi-book text-primary me-2"></i>
                                            <span>Subject: {{ quiz.subject_name }}</span>
                                        </div>
                                        <div class="d-flex align-items-center mb-2">
                                            <i class="bi bi-file-earmark-text text-primary me-2"></i>
                                            <span>Chapter: {{ quiz.chapter_name }}</span>
                                        </div>
                                    </div>

                                    <div class="d-flex gap-2">
                                        <span class="badge"
                                            :class="useUtils().bgDifficultyTypeClass(quiz.difficulty_level)">
                                            Difficulty: {{ quiz.difficulty_level.charAt(0).toUpperCase() +
                                                quiz.difficulty_level.slice(1) }}
                                        </span>
                                        <span class="badge" :class="useUtils().bgQuizStatusClass(quiz.status)">
                                            Status: {{ quiz.status.charAt(0).toUpperCase() + quiz.status.slice(1) }}
                                        </span>
                                    </div>
                                </div>
                                <div class="card-footer border-top p-0 rounded-bottom-4">
                                    <div class="row g-0 text-center py-2">
                                        <div class="col-md-3">
                                            <div class="d-flex flex-column align-items-center">
                                                <i class="bi bi-clipboard-check text-success fs-4 mb-1"></i>
                                                <span class="text-secondary small">{{ quiz.total_questions }}
                                                    Questions</span>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="d-flex flex-column align-items-center">
                                                <i class="bi bi-calendar text-info fs-4 mb-1"></i>
                                                <span class="text-secondary small">{{
                                                    useDateFormatter().formatDate2(quiz.date_of_quiz) }}</span>
                                            </div>
                                        </div>
                                        <div class="col-md-3">
                                            <div class="d-flex flex-column align-items-center">
                                                <i class="bi bi-clock text-warning fs-4 mb-1"></i>
                                                <span class="text-secondary small">{{ Math.floor(quiz.time_duration
                                                    / 60) }} mins</span>
                                            </div>
                                        </div>
                                    </div>

                                    <button v-if="quiz.status == 'upcoming'" class="btn btn-primary w-100 rounded-top-0"
                                        disabled>
                                        Starting on {{ useDateFormatter().formatDate2(quiz.date_of_quiz) }}
                                    </button>
                                    <button v-else-if="quiz.status == 'live'"
                                        class="btn btn-primary w-100 rounded-top-0" @click="takePractice(quiz.id)">
                                        Take Practice
                                    </button>
                                </div>

                            </div>
                        </div>
                    </template>

                    <div v-else class="col-md-12 text-center">
                        <p class="text-muted fs-5">No practices found matching your criteria.</p>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useDateFormatter } from '../../utils/useDateFormatter'
import useUtils from '../../utils/useUtils';
const router = useRouter()
const practices = ref([])

const loading = ref(false)
const subjects = ref([])
const difficulties = ref(['easy', 'medium', 'hard'])
const statuses = ref(['upcoming', 'live'])

const filters = reactive({
    search: '',
    subject: '',
    difficulty: '',
    timeRange: '',
    sortBy: 'date',
    sortDirection: 'desc',
    status: ''

})

const hasActiveFilters = computed(() => {
    return Object.values(filters).some(value => value !== '' && value !== 'date' && value !== 'desc' && value !== 'asc')
})

const activeFilters = computed(() => {
    return Object.entries(filters).reduce((acc, [key, value]) => {
        if (value && key !== 'search' && value !== 'date' && value !== 'desc' && value !== 'asc') {
            acc[key] = value
        }
        return acc
    }, {})
})

const filteredPractices = computed(() => {
    let result = [...practices.value]

    // Apply search filter
    if (filters.search) {
        const searchTerm = filters.search.toLowerCase()
        result = result.filter(quiz =>
            quiz.name.toLowerCase().includes(searchTerm) ||
            quiz.description.toLowerCase().includes(searchTerm)
        )
    }

    // Apply subject filter
    if (filters.subject) {
        result = result.filter(quiz => quiz.subject_name === filters.subject)
    }

    // Apply difficulty filter
    if (filters.difficulty) {
        result = result.filter(quiz => quiz.difficulty_level === filters.difficulty)
    }

    // Apply time range filter
    if (filters.timeRange) {
        const [min, max] = filters.timeRange.split('-').map(Number)
        result = result.filter(quiz => {
            const durationInMinutes = quiz.time_duration / 60 // Convert seconds to minutes
            if (filters.timeRange === '60+') {
                return durationInMinutes >= 60
            }
            return durationInMinutes >= min && durationInMinutes < max
        })
    }

    // Apply status filter
    if (filters.status) {
        result = result.filter(quiz => quiz.status.toLowerCase() === filters.status)
    }

    // Apply sorting
    switch (filters.sortBy) {
        case 'newest':
            result.sort((a, b) => b.date_created - a.date_created)
            break
        case 'oldest':
            result.sort((a, b) => a.date_created - b.date_created)
            break
        case 'name':
            result.sort((a, b) => a.name.localeCompare(b.name))
            break
        case 'duration':
            result.sort((a, b) => a.time_duration - b.time_duration)
            break
        case 'date':
            result.sort((a, b) => a.date_of_quiz - b.date_of_quiz)
            break
    }

    // Apply sort direction
    if (filters.sortDirection === 'desc') {
        result.reverse()
    }

    return result
})

const fetchPractices = async () => {
    try {
        loading.value = true
        const response = await axios.get('/api/quizzes/practices')
        practices.value = response.data.data
        subjects.value = [...new Set(practices.value.map(quiz => quiz.subject_name))]
        loading.value = false
    } catch (error) {
        loading.value = false
        console.error('Error fetching practices:', error)
    }
}

const takePractice = (quizId) => {
    router.push({ name: 'PracticeInterface', params: { id: quizId } })
}

const removeFilter = (filterKey) => {
    filters[filterKey] = ''
}

const resetFilters = () => {
    Object.keys(filters).forEach(key => {
        filters[key] = key === 'sortBy' ? 'date' : ''
    })
}


const getStatusIcon = (status) => {
    const icons = {
        'upcoming': 'bi-calendar-event',
        'live': 'bi-play-circle',
    }
    return icons[status] || 'bi-circle'
}

const toggleStatus = (status) => {
    filters.status = filters.status === status ? '' : status
}

const toggleDifficulty = (difficulty) => {
    filters.difficulty = filters.difficulty === difficulty ? '' : difficulty
}

onMounted(() => {
    fetchPractices()
})
</script>
