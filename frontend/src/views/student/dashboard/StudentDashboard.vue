<template>
    <div class="container my-4 px-0">
        <div class="row d-flex justify-content-center align-items-start">
            <StudentSidebar />
            <div class="col">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="card-title mb-0">Dashboard <span class="fs-6 text-warning"
                                v-if="stats.pending_result">( Pending Results )</span></h5>
                        <div class="d-flex gap-2">
                            <select @change="getDashboardData" class="form-select ms-2 form-select-sm w-auto"
                                v-model="selected_quiz_mode" aria-label="Select quiz mode">
                                <option value="exam">Exam</option>
                                <option value="practice">Practice</option>
                            </select>
                            <select @change="getDashboardData" class="form-select ms-0 form-select-sm w-auto"
                                v-model="selected_days_ago" aria-label="Select time range">
                                <option value="1">Past 24 hours</option>
                                <option value="7">Past week</option>
                                <option value="30">Past month</option>
                                <option value="90">Past 3 months</option>
                                <option value="180">Past 6 months</option>
                                <option value="365">Past 1 year</option>
                            </select>
                        </div>
                    </div>
                    <!-- Stats Cards -->
                    <div class="card-body">
                        <div class="row mb-4">
                            <div class="col-md-4">
                                <div class="card stat-card rounded-0"
                                    style="border-left-color: #034d28; background: #046A38 !important; color: #fff !important;">
                                    <div class="card-body">
                                        <i class="bi bi-graph-up"
                                            style="position: absolute; top: 10px; right: 20px; font-size: 4rem; color: #034d286e; z-index: 1;">
                                        </i>
                                        <h6 style="position: relative; z-index: 2;">Average Score</h6>
                                        <h2 style="position: relative; z-index: 2;">{{ stats.avg_score }}%</h2>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card stat-card rounded-0"
                                    style="border-left-color: #06038D; background: #00499D !important; color: #fff !important;">
                                    <div class="card-body">
                                        <i class="bi bi-check-circle"
                                            style="position: absolute; top: 10px; right: 20px; font-size: 4rem; color: #06038D2e; z-index: 1">
                                        </i>
                                        <h6 style="position: relative; z-index: 2;">
                                            {{ selected_quiz_mode.charAt(0).toUpperCase() +
                                                selected_quiz_mode.slice(1) }}s Completed</h6>
                                        <h2 style="position: relative; z-index: 2;">{{ stats.completed_quizzes }}</h2>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="card stat-card rounded-0"
                                    style="border-left-color: #FFD700; background: #FFDD00 !important; color: #fff !important;">
                                    <div class="card-body">
                                        <i class="bi bi-trophy"
                                            style="position: absolute; top: 10px; right: 20px; font-size: 4rem; color: #F1D700; z-index: 1;">
                                        </i>
                                        <h6 style="position: relative; z-index: 2;">Points Earned</h6>
                                        <h2 style="position: relative; z-index: 2;">{{ stats.points_earned }}</h2>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
                <div class="row">
                    <!-- Points Chart -->
                    <div class="col-md-6">
                        <div class="card mt-4">
                            <div class="card-header d-flex justify-content-between align-items-center">
                                <h5 class="card-title mb-0">Points Earned in {{ selected_quiz_mode == 'exam' ? 'Exams' :
                                    'Practices' }}</h5>
                                <select v-model="selected_days_ago" @change="getPointsData"
                                    class="form-select form-select-sm" style="width: auto">
                                    <option value="1">Last 24 hours</option>
                                    <option value="7">Last Week</option>
                                    <option value="30">Last Month</option>
                                    <option value="90">Last 3 Months</option>
                                    <option value="180">Last 6 Months</option>
                                    <option value="365">Last Year</option>
                                </select>
                            </div>
                            <div class="card-body">
                                <canvas ref="pointsChart"></canvas>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="card mt-4">
                            <div class="card-header d-flex justify-content-between align-items-center">
                                <h5 class="card-title mb-0">Exam vs Practice Points</h5>
                                <select v-model="selected_days_ago" @change="getPointsData"
                                    class="form-select form-select-sm" style="width: auto">
                                    <option value="1">Last 24 hours</option>
                                    <option value="7">Last Week</option>
                                    <option value="30">Last Month</option>
                                    <option value="90">Last 3 Months</option>
                                    <option value="180">Last 6 Months</option>
                                    <option value="365">Last Year</option>
                                </select>
                            </div>
                            <div class="card-body">
                                <canvas ref="comparisonChart"></canvas>
                            </div>
                        </div>
                    </div>

                </div>
                <div class="row">
                    <div class="col-md-6">
                        <div class="card mt-4">
                            <div class="card-header d-flex justify-content-between align-items-start">
                                <h5 class="card-title mb-0 me-2">Subject-wise Average Scores in {{ selected_quiz_mode
                                    }}s</h5>
                                <select v-model="selected_days_ago" @change="getPointsData"
                                    class="form-select form-select-sm" style="width: auto">
                                    <option value="1">Last 24 hours</option>
                                    <option value="7">Last Week</option>
                                    <option value="30">Last Month</option>
                                    <option value="90">Last 3 Months</option>
                                    <option value="180">Last 6 Months</option>
                                    <option value="365">Last Year</option>
                                </select>
                                <button type="button" class="btn ms-2 btn-sm btn-outline-primary"
                                    @click="toggleDirection">
                                    <i v-if="subjectAvgScoresDirection == 'asc'" class="bi bi-sort-down"></i>
                                    <i v-else-if="subjectAvgScoresDirection == 'desc'" class="bi bi-sort-up"></i>
                                </button>
                            </div>
                            <div class="card-body">
                                <canvas ref="subjectAvgScoresChart"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card mt-4">
                            <div class="card-header d-flex justify-content-between align-items-center">
                                <h5 class="card-title mb-0">Time vs Score Analysis for the {{ selected_quiz_mode }}s
                                </h5>
                                <select v-model="selected_days_ago" @change="getPointsData"
                                    class="form-select form-select-sm" style="width: auto">
                                    <option value="1">Last 24 hours</option>
                                    <option value="7">Last Week</option>
                                    <option value="30">Last Month</option>
                                    <option value="90">Last 3 Months</option>
                                    <option value="180">Last 6 Months</option>
                                    <option value="365">Last Year</option>
                                </select>
                            </div>
                            <div class="card-body">
                                <canvas ref="timeScoreChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-if="upcomingQuizzes.length && !props.isAdmin" class="col-md-2 mb-4">

                <div class="card px-0">
                    <div class="card-header">
                        <h6 class="card-title mb-0">Upcoming {{ selected_quiz_mode }}s</h6>
                    </div>
                    <div class="card-body p-0">
                        <div class="list-group rounded-2 list-group-flush">
                            <div v-for="quiz in upcomingQuizzes" :key="quiz.id" class="list-group-item">
                                <div class="row mb-2">

                                    <h6 class="mb-2 text-secondary">{{ quiz.name }}</h6>
                                    <small class="text-secondary">
                                        {{ quiz.subject_name }} - {{ quiz.chapter_name }}
                                    </small>
                                    <div class="badge mb-2 bg-primary">
                                        {{ useDateFormatter().formatDate2(quiz.date_of_quiz) }}
                                    </div>
                                    <div class="col-md-6 mb-2 text-start">
                                        <small class="badge bg-success">
                                            {{ Math.floor(quiz.time_duration / 60) }} mins
                                        </small>
                                    </div>
                                    <div class="col-md-6 mb-2 text-end">
                                        <span class="badge" :class="useUtils().bgQuizModeClass(quiz.quiz_mode)">{{
                                            quiz.quiz_mode.charAt(0).toUpperCase() + quiz.quiz_mode.slice(1)
                                        }}</span>
                                    </div>
                                </div>
                            </div>
                            <div v-if="!upcomingQuizzes.length" class="list-group-item text-center py-4">
                                <i class="bi bi-calendar-x text-secondary fs-1"></i>
                                <p class="text-secondary mt-2">No upcoming {{ selected_quiz_mode }}s</p>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import StudentSidebar from '../../../components/StudentSidebar.vue';
import { useDateFormatter } from '../../../utils/useDateFormatter';
import Chart from 'chart.js/auto';
import useUtils from '../../../utils/useUtils';

const selected_days_ago = ref(7);
const selected_quiz_mode = ref('exam');
const upcomingQuizzes = ref([]);

const props = defineProps({
    isAdmin: {
        type: Boolean,
        default: false,
    },
    studentId: {
        type: Number,
        default: null,
    }
})


const subjectAvgScoresDirection = ref('desc');
const pointsChart = ref(null);
const comparisonChart = ref(null);
const subjectAvgScoresChart = ref(null);
const timeScoreChart = ref(null);

const chartInstance = ref(null);
const comparisonChartInstance = ref(null);
const subjectAvgScoresChartInstance = ref(null);
const timeScoreChartInstance = ref(null);

const stats = ref({
    total_quizzes: 0,
    avg_score: 0,
    completed_quizzes: 0,
    points_earned: 0
});

const getUpcomingQuizzes = async () => {
    try {
        if (props.isAdmin) {
            return;
        }
        const response = await axios.get('/api/quizzes/upcoming', {
            params: { quiz_mode: selected_quiz_mode.value }
        });
        upcomingQuizzes.value = response.data.data;
    } catch (error) {
        console.error('Error fetching upcoming quizzes:', error);
    }
};

const getPointsData = async () => {
    try {
        // Get exam data
        const examResponse = await axios.get('/api/students/dashboard/points_history', {
            params: {
                days_ago: selected_days_ago.value,
                quiz_mode: 'exam',
                student_id: props.isAdmin ? props.studentId : null
            }
        });

        // Get practice data
        const practiceResponse = await axios.get('/api/students/dashboard/points_history', {
            params: {
                days_ago: selected_days_ago.value,
                quiz_mode: 'practice',
                student_id: props.isAdmin ? props.studentId : null
            }
        });

        // Get subject-wise average scores
        const subjectAvgResponse = await axios.get('/api/students/dashboard/charts', {
            params: {
                days_ago: selected_days_ago.value,
                quiz_mode: selected_quiz_mode.value,
                direction: subjectAvgScoresDirection.value,
                student_id: props.isAdmin ? props.studentId : null
            }
        });
        const response = await axios.get('/api/students/dashboard/time-score', {
            params: {
                days_ago: selected_days_ago.value,
                quiz_mode: selected_quiz_mode.value,
                student_id: props.isAdmin ? props.studentId : null
            }
        });
        updateTimeScoreChart(response.data);
        // Update main points chart
        if (selected_quiz_mode.value === 'exam') {
            updateChart(examResponse.data.labels, examResponse.data.points);
        } else {
            updateChart(practiceResponse.data.labels, practiceResponse.data.points);
        }

        // Update comparison chart
        updateComparisonChart(
            examResponse.data.labels,
            examResponse.data.points,
            practiceResponse.data.points
        );

        updateSubjectAvgChart(
            subjectAvgResponse.data.labels,
            subjectAvgResponse.data.data
        );
    } catch (error) {
        console.error('Error fetching points data:', error);
    }
};
const toggleDirection = () => {
    subjectAvgScoresDirection.value = subjectAvgScoresDirection.value === 'asc' ? 'desc' : 'asc';
    getSubjectAvgScoresData();
};

const getSubjectAvgScoresData = async () => {
    try {
        const response = await axios.get('/api/students/dashboard/charts', {
            params: {
                days_ago: selected_days_ago.value,
                quiz_mode: selected_quiz_mode.value,
                direction: subjectAvgScoresDirection.value,
                student_id: props.isAdmin ? props.studentId : null
            }
        });
        updateSubjectAvgChart(response.data.labels, response.data.data);
    } catch (error) {
        console.error('Error fetching subject avg scores data:', error);
    }
};


const updateChart = (labels, data) => {
    if (chartInstance.value) {
        chartInstance.value.destroy();
    }

    chartInstance.value = new Chart(pointsChart.value, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: (selected_quiz_mode.value === 'exam' ? 'Exams ' : 'Practice ') + 'Points',
                data: data,
                animation: {
                    duration: 0
                },
                borderColor: '#046A38',
                backgroundColor: 'rgba(4, 106, 56, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Points'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: `${selected_days_ago.value == 1 ? 'Hours' : selected_days_ago.value <= 30 ? 'Days' : 'Months'}`
                    }
                }
            }
        }
    });
};

const updateSubjectAvgChart = (labels, data) => {
    if (subjectAvgScoresChartInstance.value) {
        subjectAvgScoresChartInstance.value.destroy();
    }

    const colors = ['rgba(40, 167, 69, 0.7)',
        'rgba(255, 193, 7, 0.7)',
        'rgba(220, 53, 69, 0.7)'
    ];

    const borderColors = [
        'rgb(40, 167, 69)',
        'rgb(255, 193, 7)',
        'rgb(220, 53, 69)',
    ];

    subjectAvgScoresChartInstance.value = new Chart(subjectAvgScoresChart.value, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Score',
                data: data,
                animation: {
                    duration: 0
                },
                backgroundColor: colors,
                borderColor: borderColors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function (value) {
                            return value + '%';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Average Score (%)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `Average Score: ${context.raw} %`;
                        }
                    }
                }
            }
        }
    });
};

const updateComparisonChart = (labels, examPoints, practicePoints) => {
    if (comparisonChartInstance.value) {
        comparisonChartInstance.value.destroy();
    }

    comparisonChartInstance.value = new Chart(comparisonChart.value, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Exam Points',
                    data: examPoints,
                    animation: {
                        duration: 0
                    },
                    borderColor: '#046A38',
                    backgroundColor: 'rgba(4, 106, 56, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Practice Points',
                    data: practicePoints,
                    animation: {
                        duration: 0
                    },
                    borderColor: '#FF671F',
                    backgroundColor: 'rgba(255, 103, 31, 0.1)',
                    fill: true,
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Points'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: `${selected_days_ago.value == 1 ? 'Hours' : selected_days_ago.value <= 30 ? 'Days' : 'Months'}`
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });

};

const updateTimeScoreChart = (data) => {
    if (timeScoreChartInstance.value) {
        timeScoreChartInstance.value.destroy();
    }

    timeScoreChartInstance.value = new Chart(timeScoreChart.value, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Quiz Scores',
                data: data.map(item => ({
                    x: item.time,
                    y: item.score,
                })),
                animation: {
                    duration: 0
                },
                backgroundColor: 'rgba(4, 106, 56, 0.5)',
                borderColor: '#046A38',
                pointRadius: 6,
                pointHoverRadius: 8,
                pointHoverBackgroundColor: '#FF671F',
                pointHoverBorderColor: '#FF671F',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time Taken (minutes)'
                    },
                    beginAtZero: true
                },
                y: {
                    title: {
                        display: true,
                        text: 'Score (%)'
                    },
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function (value) {
                            return value + '%';
                        }
                    },
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const point = data[context.dataIndex];
                            return [
                                `Quiz: ${point.quiz_name}`,
                                `Time: ${useDateFormatter().formatTimeTaken(point.time_taken)}`,
                                `Score: ${point.score}%`
                            ];
                        }
                    }
                }
            }
        }
    });
};

const getDashboardData = async () => {
    try {
        const response = await axios.get('/api/students/dashboard', {
            params: {
                days_ago: selected_days_ago.value,
                quiz_mode: selected_quiz_mode.value,
                student_id: props.isAdmin ? props.studentId : null
            }
        });
        stats.value = response.data;
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
    await getUpcomingQuizzes();
    await getPointsData();
};

onMounted(() => {
    getDashboardData();
});

</script>

<style scoped>
.stat-card {
    border-left: 4px solid;
}

canvas {
    min-height: 250px;
}
</style>