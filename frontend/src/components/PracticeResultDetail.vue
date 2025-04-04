<template>
    <div class="card mx-auto mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0 fw-bold text-center">Detailed Review</h5>
            <!-- Search Filter -->
            <div class="d-flex align-items-center mb-0">
                <input type="text" class="form-control" v-model="searchQuery" placeholder="Search questions..." />
            </div>
        </div>

        <div class="card-body">
            <div v-for="question in filteredQuestions" :key="question.id" class="mb-5 pb-4 border-bottom">
                <div class="d-flex fw-bold justify-content-between align-items-center mb-3">
                    <div>
                        <span class="text-secondary me-2">Question {{ question.display_id }}</span>
                        <span class="badge" :class="useUtils().bgQuestionTypeClass(question.type)">
                            {{ question.type }}
                        </span>
                    </div>
                    <span class="badge" :class="question.score > 0 ? 'bg-success' : 'bg-danger'">
                        {{ question.score > 0 ? '+' + question.score : question.score }} / {{ question.total_marks }}
                    </span>
                </div>

                <h3 class="mb-4">{{ question.statement }}</h3>

                <!-- Question Image if exists -->
                <div class="text-center mb-4" v-if="question.question_image">
                    <img :src="questionImageSrc.value + question.question_image" class="img-fluid" alt="Question Image"
                        style="max-height: 300px; object-fit: contain;" />
                </div>

                <!-- MCQ/MSQ Options -->
                <template v-if="['MCQ', 'MSQ'].includes(question.type)">
                    <div v-for="option in question.options" :key="option.id" class="mb-3">
                        <div class="p-3" :class="{
                            'bg-success bg-opacity-50': isCorrectAnswer(question, option),
                            'bg-danger bg-opacity-50': !isCorrectAnswer(question, option),
                        }">
                            {{ option.text }}
                            <span v-if="isSelected(question, option) && isCorrectAnswer(question, option)"
                                class="badge bg-success float-end">
                                <i class="bi bi-check-circle-fill me-2"></i>Selected
                            </span>
                            <span v-else-if="isSelected(question, option) && !isCorrectAnswer(question, option)"
                                class="badge bg-danger float-end">
                                <i class="bi bi-x-circle-fill me-2"></i>Selected
                            </span>
                        </div>
                    </div>
                </template>

                <!-- Numerical Answer -->
                <template v-else-if="question.type === 'Numerical'">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label">Your Answer</label>
                            <input type="number" class="form-control rounded-0" :value="question.selected_answer"
                                disabled :class="{
                                    'is-valid bg-success bg-opacity-50': question.selected_answer[0] == question.correct_answer[0],
                                    'is-invalid bg-danger bg-opacity-50': !(question.selected_answer[0] == question.correct_answer[0]),
                                }" />
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">Correct Answer</label>
                            <input type="number" class="form-control rounded-0 is-valid bg-success bg-opacity-50"
                                :value="question.correct_answer" disabled />
                        </div>
                    </div>
                </template>

                <!-- Explanation -->
                <div class="mt-4" v-if="question.answer_explanation">
                    <h6 class="text-secondary">Answer Explanation:</h6>
                    <p class="form-control p-3 rounded">
                        {{ question.answer_explanation }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import useUtils from '../utils/useUtils';


const props = defineProps({
    questions: {
        type: Array,
        required: true
    }
});

const searchQuery = ref('');
const filteredQuestions = computed(() => {
    return props.questions.filter(question => question.statement.toLowerCase().includes(searchQuery.value.toLowerCase()));
});

// Helper functions for checking answers
const isCorrectAnswer = (question, option) => {
    if (question.type === 'MCQ' || question.type === 'MSQ') {
        return question.correct_answer.includes(option.id);
    }
    return false;
};

const isSelected = (question, option) => {
    if (question.type === 'MCQ' || question.type === 'MSQ') {
        return question.selected_answer.includes(option.id);
    }
    return false;
};

</script>