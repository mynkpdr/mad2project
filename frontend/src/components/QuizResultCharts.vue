<template>
        <div class="row g-4">
            <div class="col-md-4">
                <div class="card result-card">
                    <div class="card-header">
                        <h5 class="card-title mb-0 text-center">Score Overview</h5>
                    </div>
                    <div class="card-body d-flex align-items-center justify-content-center">
                        <canvas ref="scoreChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card result-card">
                    <div class="card-header">
                        <h5 class="card-title mb-0 text-center">Time Analysis</h5>
                    </div>
                    <div class="card-body d-flex align-items-center justify-content-center">
                        <canvas ref="timeChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card result-card">
                    <div class="card-header">
                        <h5 class="card-title mb-0 text-center">Performance Comparison</h5>
                    </div>
                    <div class="card-body d-flex align-items-center justify-content-center">
                        <canvas ref="comparisonChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';
import { useDateFormatter } from '../utils/useDateFormatter';

const props = defineProps({
    quizData: {
        type: Object,
        required: true
    }
});

const scoreChart = ref(null);
const timeChart = ref(null);
const comparisonChart = ref(null);

const scoreChartInstance = ref(null);
const timeChartInstance = ref(null);
const comparisonChartInstance = ref(null);

const initCharts = () => {
    const { total_scored_marks, total_marks, total_scored_percentage, total_percentage, time_taken, total_time, others_average } = props.quizData;

    // Score Chart
    scoreChartInstance.value = new Chart(scoreChart.value, {
        type: 'doughnut',
        data: {
            labels: ['Marks Scored', 'Marks Missed'],
            datasets: [{
                data: [total_scored_marks, total_marks - total_scored_marks],
                backgroundColor: ['#198754', '#e9ecef']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: `You got ${total_scored_marks} / ${total_marks} which is ~${total_scored_percentage}%`,
                    font: {
                        size: 16,
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                },
            }
        }
    });

    // Time Chart
    timeChartInstance.value = new Chart(timeChart.value, {
        type: 'doughnut',
        data: {
            labels: ['Time Taken', 'Time Remaining'],
            datasets: [{
                data: [time_taken, total_time - time_taken],
                backgroundColor: ['#198754', '#e9ecef']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: `${(useDateFormatter().formatTimeTaken(time_taken))} / ${(useDateFormatter().formatTimeTaken(total_time))}`,
                    font: {
                        size: 16,
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            return `${label}: ${(useDateFormatter().formatTimeTaken(value))}`;
                        }
                    }
                }
            }
        }
    });

    // Comparison Chart
    comparisonChartInstance.value = new Chart(comparisonChart.value, {
        type: 'bar',
        data: {
            labels: ['Your Score', 'Others Average'],
            datasets: [{
                data: [total_scored_percentage, others_average],
                backgroundColor: ['#FF671F', '#ffc107']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return context.raw + '%';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: total_percentage,
                    ticks: {
                        callback: function (value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });

};

watch(() => props.quizData, () => {
    if (scoreChartInstance.value) scoreChartInstance.value.destroy();
    if (timeChartInstance.value) timeChartInstance.value.destroy();
    if (comparisonChartInstance.value) comparisonChartInstance.value.destroy();
    initCharts();
}, { deep: true });

onMounted(() => {
    initCharts();
});
</script>

<style scoped>
.card {
    min-height: 350px;
}

.card-body {
    height: 300px;
}
</style>