<template>
    <div class="card shadow">
        <div class="card-body px-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h5 class="card-title m-0">Q. {{ questions[currentQuestionIndex].display_id }}</h5>
                <div class="d-flex justify-content-between mb-3">
                    <span class="badge me-2"
                        :class="useUtils().bgQuestionTypeClass(questions[currentQuestionIndex].type)">
                        {{ questions[currentQuestionIndex].type }}
                    </span>
                    <span class="badge"
                        :class="questions[currentQuestionIndex].score > 0 ? 'bg-success' : 'bg-danger'">
                        + {{ questions[currentQuestionIndex].score }} / {{ questions[currentQuestionIndex].total_marks }}
                        Marks
                    </span>
                </div>
            </div>

            <p class="card-text">{{ questions[currentQuestionIndex].statement }}</p>
            <img v-if="questions[currentQuestionIndex].question_image"
                :src="questionImageSrc.value + questions[currentQuestionIndex].question_image" class="img-fluid mb-4"
                alt="Question Image" style="max-width: 100%; max-height: 400px; object-fit: contain;" />

            <!-- Question Options -->
            <div class="options flex-grow-1">
                <!-- MCQ -->
                <template v-if="questions[currentQuestionIndex].type === 'MCQ'">
                    <div v-for="option in questions[currentQuestionIndex].options" :key="option.id"
                        class="form-check mb-3">
                        <input class="form-check-input" type="radio"
                            :name="'question' + questions[currentQuestionIndex].id" :id="option.id" :value="option.id"
                            :class="{
                                'bg-success': isCorrectAnswer(questions[currentQuestionIndex], option),
                                'bg-danger': isSelected(questions[currentQuestionIndex], option) && !isCorrectAnswer(questions[currentQuestionIndex], option)
                            }" :checked="questions[currentQuestionIndex].selected_answer.includes(option.id)" disabled>
                        <label class="form-check-label" :for="option.id">
                            {{ option.text }}
                        </label>
                    </div>
                </template>

                <!-- MSQ -->
                <template v-if="questions[currentQuestionIndex].type === 'MSQ'">
                    <div v-for="option in questions[currentQuestionIndex].options" :key="option.id"
                        class="form-check mb-3">
                        <input class="form-check-input" type="checkbox" :id="option.id" :value="option.id" :class="{
                            'bg-success': isCorrectAnswer(questions[currentQuestionIndex], option),
                            'bg-danger': isSelected(questions[currentQuestionIndex], option) && !isCorrectAnswer(questions[currentQuestionIndex], option)
                        }" :checked="questions[currentQuestionIndex].selected_answer.includes(option.id)" disabled>
                        <label class="form-check-label" :for="option.id">
                            {{ option.text }}
                        </label>
                    </div>
                </template>

                <!-- Numerical -->
                <template v-if="questions[currentQuestionIndex].type === 'Numerical'">
                    <div class="row">
                        <div class="col-md-6">
                            <input class="form-control bg-opacity-50" type="number" :class="{
                                'is-valid bg-success': questions[currentQuestionIndex].selected_answer[0] == questions[currentQuestionIndex].correct_answer[0],
                                'is-invalid bg-danger': !(questions[currentQuestionIndex].selected_answer[0] == questions[currentQuestionIndex].correct_answer[0])
                            }" :value="questions[currentQuestionIndex].selected_answer[0]" disabled>
                        </div>
                        <div class="col-md-6">
                            <input type="number" class="form-control is-valid bg-success bg-opacity-50"
                                :value="questions[currentQuestionIndex].correct_answer" disabled>
                        </div>
                    </div>
                </template>

                <button disabled class="btn bg-opacity-25 mt-4" style="font-size: 14px;"
                    :class="useUtils().btnQuestionStatusClass(quizData.state[questions[currentQuestionIndex]['id']])">
                    {{ getCurrentQuestionStatus(quizData.state[questions[currentQuestionIndex]['id']]) }}
                </button>

                <div class="mt-4" v-if="questions[currentQuestionIndex].answer_explanation">
                    <h6 class="text-secondary">Answer Explanation:</h6>
                    <p class="form-control p-3 rounded">
                        {{ questions[currentQuestionIndex].answer_explanation }}
                    </p>
                </div>
            </div>

            <div class="d-flex gap-2 mt-4">
                <button class="btn btn-primary" @click="prevQuestion" :disabled="currentQuestionIndex === 0">Previous</button>
                <button class="btn btn-primary" @click="nextQuestion"
                    :disabled="currentQuestionIndex === questions.length - 1">Next</button>
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
    currentQuestionIndex: {
        type: Number,
        required: true
    },
    quizData: {
        type: Object,
        required: true
    }
});

const emit = defineEmits(['update:currentQuestionIndex']);

const nextQuestion = () => {
    if (props.currentQuestionIndex < props.questions.length - 1) {
        emit('update:currentQuestionIndex', props.currentQuestionIndex + 1);
    }
};

const prevQuestion = () => {
    if (props.currentQuestionIndex > 0) {
        emit('update:currentQuestionIndex', props.currentQuestionIndex - 1);
    }
};

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
</script>
