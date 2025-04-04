import axios from 'axios'
import { defineStore } from 'pinia'

export const useQuizStore = defineStore('quiz', {
    state: () => ({
        questions: [],
        quiz_id: null,
        take_quiz_id: null,
        currentQuestionId: 0,
        timeRemaining: null,
        quizState: {},
        candidateName: '',
        chapterName: '',
        quizName: '',
        totalMarks: ''
    }),
    getters: {
        totalQuestions: (state) => state.questions.length,
        formattedTime: (state) => {
            const hours = Math.floor(state.timeRemaining / 3600)
            const minutes = Math.floor((state.timeRemaining % 3600) / 60)
            const seconds = state.timeRemaining % 60
            return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
        },
        getCurrentQuestion: (state) => () => {
            return state.questions.find((q) => q.id === state.currentQuestionId) || {}
        },
        getCurrentQuestionStatus: (state) => () => {
            return state.quizState[state.currentQuestionId] || {
                answered: false,
                markedForReview: false,
            }
        },
        questionCounts: (state) => {
            const counts = {
                notVisited: state.questions.length,
                answered: 0,
                notAnswered: 0,
                markedForReview: 0,
            }

            Object.values(state.quizState).forEach((status) => {
                counts.notVisited--
                if (status.answered && !status.markedForReview) {
                    counts.answered++
                } else if (status.markedForReview) {
                    counts.markedForReview++
                } else {
                    counts.notAnswered++
                }
            })

            return counts
        },
    },
    actions: {
        setQuestions(questions) {
            this.questions = questions
            if (questions.length > 0) {
                this.currentQuestionId = questions[0].id
            }
        },
        setQuizID(id) {
            this.quiz_id = id
        },
        setTakeQuizID(id) {
            this.take_quiz_id = id
        },
        setStudent(name) {
            this.candidateName = name
        },
        setChapter(name) {
            this.chapterName = name
        },
        setQuiz(name) {
            this.quizName = name
        },
        setTimeRemaining(time_duration) {
            this.timeRemaining = time_duration
        },
        handleSelectAnswer(answer) {
            this.quizState[this.currentQuestionId] = {
                ...this.getCurrentQuestionStatus(),
                answered: false,
                selected_values: answer,
            }
        },
        handleMSQChange(optionId, checked) {
            const currentAnswers = Array.isArray(this.getCurrentQuestionStatus().selected_values)
                ? this.getCurrentQuestionStatus().selected_values
                : []

            if (checked) {
                this.handleSelectAnswer([...currentAnswers, optionId])
            } else {
                this.handleSelectAnswer(currentAnswers.filter(a => a !== optionId))
            }
        },
        handleMarkForReview() {
            const currentStatus = this.getCurrentQuestionStatus()
            this.quizState[this.currentQuestionId] = {
                ...currentStatus,
                markedForReview: true,
                answered: currentStatus.answered || !!currentStatus.selected_values
            }

            this.moveToNextQuestion()
        },
        handleClearResponse() {
            this.quizState[this.currentQuestionId] = {
                ...this.getCurrentQuestionStatus(),
                answered: false,
                selected_values: undefined,
            }
        },
        handleSaveAndNext() {
            const currentStatus = this.getCurrentQuestionStatus()
            this.quizState[this.currentQuestionId] = {
                ...currentStatus,
                answered: currentStatus.answered || !!currentStatus.selected_values
            }
            if (currentStatus.markedForReview && currentStatus.selected_values) {
                this.quizState[this.currentQuestionId] = {
                    ...currentStatus,
                    answered: true,
                    markedForReview: false
                }
            }
            try {
                axios.post(`/api/take_quiz/${this.take_quiz_id}/save`, {
                    "quiz_state": this.quizState
                });
            } catch (error) {
                throw error;
            }
            this.moveToNextQuestion()
        },
        handleNext() {
            const currentStatus = this.getCurrentQuestionStatus()
            this.quizState[this.currentQuestionId] = {
                ...currentStatus,
                answered: currentStatus.answered || !!currentStatus.selected_values
            }
            if (currentStatus.markedForReview && currentStatus.selected_values) {
                this.quizState[this.currentQuestionId] = {
                    ...currentStatus,
                    answered: true,
                    markedForReview: false
                }
            }
            this.moveToNextQuestion()
        },

        handleSelectQuestion(questionId) {
            this.currentQuestionId = questionId
        },
        moveToNextQuestion() {
            const currentIndex = this.questions.findIndex(q => q.id === this.currentQuestionId)
            if (currentIndex < this.questions.length - 1) {
                this.currentQuestionId = this.questions[currentIndex + 1].id
            }
        },
        moveToPreviousQuestion() {
            const currentIndex = this.questions.findIndex(q => q.id === this.currentQuestionId)
            if (currentIndex > 0) {
                this.currentQuestionId = this.questions[currentIndex - 1].id
            }
        },
        decrementTimer() {
            if (this.timeRemaining > 0) {
                this.timeRemaining--
            }
        },
        resetQuiz() {
            this.questions = []
            this.quiz_id = null
            this.take_quiz_id = null
            this.currentQuestionId = 0
            this.timeRemaining = null
            this.quizState = {}
            this.candidateName = 'John Doe'
            this.chapterName = "Chapter"
        }
    },
})

