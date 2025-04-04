<template>
    <div class="card shadow">
        <div class="card-body px-4">
            <h5 class="card-title mb-4">Question Overview</h5>
            <div class="question-grid mb-4 flex-grow-1 overflow-auto">
                <button v-for="question in questions" :key="question.id" class="btn"
                    :class="useUtils().btnQuestionStatusClass(quizData.state[questions[question.display_id - 1]['id']])"
                    @click="handleCurrentQuestionIndex(question.display_id - 1)">
                    {{ question.display_id }}
                </button>
            </div>
            <h6 class="mb-3 fw-bold">Question Summary</h6>
            <div class="row row-cols-1 g-3">
                <div class="col">
                    <div class="d-flex align-items-center">
                        <div class="bg-light border rounded-square rounded-2 me-2"
                            style="width: 20px; height: 20px;"></div>
                        <small class="text-secondary">Not Visited ({{ getQuestionStatusCount('Not Visited')
                            }})</small>
                    </div>
                </div>

                <div class="col">
                    <div class="d-flex align-items-center">
                        <div class="bg-success rounded-square rounded-2 me-2" style="width: 20px; height: 20px;"></div>
                        <small class="text-success">Answered ({{ getQuestionStatusCount('Answered') }})</small>
                    </div>
                </div>

                <div class="col">
                    <div class="d-flex align-items-center">
                        <div class="bg-danger rounded-square rounded-2 me-2" style="width: 20px; height: 20px;"></div>
                        <small class="text-danger">Not Answered ({{ getQuestionStatusCount('Not Answered')
                            }})</small>
                    </div>
                </div>

                <div class="col">
                    <div class="d-flex align-items-center">
                        <div class="bg-warning rounded-square rounded-2 me-2" style="width: 20px; height: 20px;"></div>
                        <small class="text-warning">Marked ({{ getQuestionStatusCount('Marked') }})</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import useUtils from '../utils/useUtils';

const props = defineProps({
    questions: {
        type: Array,
        required: true
    },
    quizData: {
        type: Object,
        required: true
    }
});

const emit = defineEmits(['update:currentQuestionIndex']);

const handleCurrentQuestionIndex = (index) => {
    emit('update:currentQuestionIndex', index);
};

const getCurrentQuestionStatus = (question) => {
    if (!question.answered && question.selected_values === null) {
        return 'Not Visited';
    }
    if (question.answered && question.selected_values && !question.markedForReview) {
        return 'Answered';
    }
    if (!question.answered && !question.markedForReview) {
        return 'Not Answered';
    }
    if (question.markedForReview && !question.answered) {
        return 'Marked';
    }
    if (question.markedForReview && question.answered) {
        return 'Marked';
    }
    return 'Not Visited';
};

const getQuestionStatusCount = (status) => {
    return props.questions.filter(question =>
        getCurrentQuestionStatus(props.quizData.state[question.id]) === status
    ).length;
};
</script>

<style scoped>
.question-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
    gap: 0.5rem;
}
</style>
