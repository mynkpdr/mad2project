<template>
  <div class="section m-4">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h3 class="card-title mb-0">
              Dashboard
            </h3>
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
          <div class="card-body">
            <div class="row mb-4">
              <div class="col-md-3">
                <div class="card shadow stat-card rounded-0"
                  style="border-left-color: #ec5205; background: #FF671F !important; color: #fff !important;">
                  <div class="card-body">
                    <i class="bi bi-mortarboard-fill"
                      style="position: absolute; top: 10px; right: 20px; font-size: 4rem; color: #ec5205; z-index: 1"></i>
                    <h6 style="position: relative; z-index: 2;">TOTAL STUDENTS</h6>
                    <h2 style="position: relative; z-index: 2;">{{ stats.total_students }}</h2>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="card shadow stat-card rounded-0"
                  style="border-left-color: #034d28; background: #046A38 !important; color: #fff !important;">
                  <div class="card-body">
                    <i class="bi bi-clipboard-check"
                      style="position: absolute; bottom: 0px; right: 20px; font-size: 4rem; color: #034d286e; z-index: 1;"></i>
                    <h6 style="position: relative; z-index: 2;">TOTAL {{ selected_quiz_mode.toUpperCase() }}S</h6>
                    <h2 style="position: relative; z-index: 2;">{{ stats.total_quizzes }}</h2>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="card shadow stat-card rounded-0"
                  style="border-left-color: #06038D; background: #00499D !important; color: #fff !important; z-index: 1;">
                  <div class="card-body">
                    <i class="bi bi-mortarboard-fill"
                      style="position: absolute; bottom: 0px; right: 20px; font-size: 4rem; color: #06038D2e;"></i>
                    <h6 style="position: relative; z-index: 2;">ACTIVE STUDENTS</h6>
                    <h2 style="position: relative; z-index: 2;">{{ stats.active_students }}</h2>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="card shadow stat-card rounded-0"
                  style="border-left-color: #FFD700; background: #FFDD00 !important; color: #fff !important; z-index: 1;">
                  <div class="card-body">
                    <i class="bi bi-clipboard-check"
                      style="position: absolute; bottom: 0px; right: 20px; font-size: 4rem; color: #F1D700;"></i>
                    <h6 style="position: relative; z-index: 2;">{{ selected_quiz_mode.toUpperCase() }}S COMPLETED</h6>
                    <h2 style="position: relative; z-index: 2;">{{ stats.quizzes_completed }}</h2>
                  </div>
                </div>
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
            <h5 class="card-title mb-0">{{ selected_quiz_mode == 'exam' ? 'Exams' :
              'Practices' }} taken in the last {{ selected_days_ago }} days</h5>
          </div>
          <div class="card-body">
            <canvas ref="takeQuizzesGrowthChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Comparison Chart -->
      <div class="col-md-6">
        <div class="card mt-4">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="card-title mb-0">Students growth in the last {{ selected_days_ago }} days</h5>
          </div>
          <div class="card-body">
            <canvas ref="studentsGrowthChart"></canvas>
          </div>
        </div>
      </div>
    </div>
    <div class="row mt-4">
      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">Top {{ selected_quiz_mode.charAt(0).toUpperCase() +
              selected_quiz_mode.slice(1) }}s by attempts in the last {{ selected_days_ago }} days</h5>
          </div>
          <div class="card-body">
            <canvas ref="topQuizzesByAttemptsChart"></canvas>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title mb-0">{{ selected_quiz_mode.charAt(0).toUpperCase() + selected_quiz_mode.slice(1) }}s
              with Difficulty Level Distribution</h5>
          </div>
          <div class="card-body">
            <canvas ref="difficultyLevelsChart"></canvas>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-start">
            <h5 class="card-title mb-0">Subject wise Average Score in {{ selected_quiz_mode.charAt(0).toUpperCase() +
              selected_quiz_mode.slice(1) }}s in the last {{ selected_days_ago }} days</h5>
            <button type="button" class="btn ms-2 btn-sm btn-outline-primary" @click="toggleDirection">
              <i v-if="subjectAvgScoresDirection == 'asc'" class="bi bi-sort-down"></i>
              <i v-else-if="subjectAvgScoresDirection == 'desc'" class="bi bi-sort-up"></i>
            </button>
          </div>
          <div class="card-body">
            <canvas ref="subjectAvgScoresChart"></canvas>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import Chart from 'chart.js/auto'

const selected_days_ago = ref(7);
const selected_quiz_mode = ref('exam');

const subjectAvgScoresDirection = ref('desc');
const studentsGrowthChartInstance = ref(null);
const takeQuizzesGrowthChartInstance = ref(null);
const difficultyLevelsChartInstance = ref(null);
const subjectAvgScoresChartInstance = ref(null);
const topQuizzesByAttemptsChartInstance = ref(null);

const studentsGrowthChart = ref(null);
const takeQuizzesGrowthChart = ref(null);
const difficultyLevelsChart = ref(null);
const subjectAvgScoresChart = ref(null);
const topQuizzesByAttemptsChart = ref(null);
const stats = ref({});

// API Functions
const getDashboardData = async () => {
  try {
    const response = await axios.get('/api/admins/dashboard', {
      params: {
        days_ago: selected_days_ago.value,
        quiz_mode: selected_quiz_mode.value,
        growth_type: 'students'
      }
    });
    stats.value = response.data;
    await getPointsData(),
      await getDifficultyLevelsData(),
      await getSubjectAvgScoresData()
    await getTopQuizzesByAttemptsData()
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
};

const getPointsData = async () => {
  try {
    const studentsGrowthDataResponse = await axios.get('/api/admins/dashboard/growth-history', {
      params: {
        days_ago: selected_days_ago.value,
        quiz_mode: selected_quiz_mode.value,
        growth_type: 'students'
      }
    });

    const takeQuizzesGrowthDataResponse = await axios.get('/api/admins/dashboard/growth-history', {
      params: {
        days_ago: selected_days_ago.value,
        quiz_mode: selected_quiz_mode.value,
        growth_type: 'take_quizzes'
      }
    });
    updateTakeQuizzesGrowthChart(takeQuizzesGrowthDataResponse.data.labels, takeQuizzesGrowthDataResponse.data.points);
    updateStudentsGrowthChart(studentsGrowthDataResponse.data.labels, studentsGrowthDataResponse.data.points);
  } catch (error) {
    throw error
  }
};

const getDifficultyLevelsData = async () => {
  try {
    const response = await axios.get('/api/admins/dashboard/charts', {
      params: {
        chart_type: 'difficulty_levels',
        quiz_mode: selected_quiz_mode.value
      }
    });
    updateDifficultyLevelsChart(response.data);
  } catch (error) {
    console.error('Error fetching difficulty levels data:', error);
  }
};

const toggleDirection = () => {
  subjectAvgScoresDirection.value = subjectAvgScoresDirection.value === 'asc' ? 'desc' : 'asc';
  getSubjectAvgScoresData();
};

const getSubjectAvgScoresData = async () => {
  try {
    const response = await axios.get('/api/admins/dashboard/charts', {
      params: {
        chart_type: 'subject_avg_scores',
        quiz_mode: selected_quiz_mode.value,
        days_ago: selected_days_ago.value,
        direction: subjectAvgScoresDirection.value
      }
    });
    updateSubjectAvgScoresChart(response.data.labels, response.data.data);
  } catch (error) {
    console.error('Error fetching subject average scores data:', error);
  }
};

const getTopQuizzesByAttemptsData = async () => {
  try {
    const response = await axios.get('/api/admins/dashboard/charts', {
      params: {
        chart_type: 'top_quizzes_by_attempts',
        quiz_mode: selected_quiz_mode.value
      }
    });
    updateTopQuizzesByAttemptsChart(response.data.labels, response.data.data);
  } catch (error) {
    console.error('Error fetching top quizzes by attempts data:', error);
  }
};

const updateStudentsGrowthChart = (labels, data) => {
  if (studentsGrowthChartInstance.value) {
    studentsGrowthChartInstance.value.destroy();
  }

  studentsGrowthChartInstance.value = new Chart(studentsGrowthChart.value, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Students',
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
          ticks: {
            stepSize: 1
          },
          title: {
            display: true,
            text: 'Students'
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

const updateTakeQuizzesGrowthChart = (labels, data) => {
  if (takeQuizzesGrowthChartInstance.value) {
    takeQuizzesGrowthChartInstance.value.destroy();
  }

  takeQuizzesGrowthChartInstance.value = new Chart(takeQuizzesGrowthChart.value, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: (selected_quiz_mode.value === 'exam' ? ' Exams ' : 'Practices ') + 'taken',
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
          ticks: {
            stepSize: 1
          },
          title: {
            display: true,
            text: (selected_quiz_mode.value === 'exam' ? ' Exams ' : 'Practices ') + 'taken'
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

const updateDifficultyLevelsChart = (data) => {
  if (difficultyLevelsChartInstance.value) {
    difficultyLevelsChartInstance.value.destroy();
  }

  const colors = {
    Easy: 'rgba(40, 167, 69, 0.7)',
    Medium: 'rgba(255, 193, 7, 0.7)',
    Hard: 'rgba(220, 53, 69, 0.7)',
    Unset: 'rgba(108, 117, 125, 0.7)'
  };

  const borderColors = {
    Easy: 'rgb(40, 167, 69)',
    Medium: 'rgb(255, 193, 7)',
    Hard: 'rgb(220, 53, 69)',
    Unset: 'rgb(108, 117, 125)'
  };

  difficultyLevelsChartInstance.value = new Chart(difficultyLevelsChart.value, {
    type: 'doughnut',
    data: {
      labels: data.labels,
      datasets: [{
        data: data.data,
        animation: {
          duration: 0
        },
        backgroundColor: data.labels.map(label => colors[label]),
        borderColor: data.labels.map(label => borderColors[label]),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      aspectRatio: 2,
      plugins: {
        legend: {
          labels: {
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = Math.round((context.raw / total) * 100);
              return `${context.label}: ${context.raw} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
};

const updateSubjectAvgScoresChart = (labels, data) => {
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
            text: 'Average Score'
          }
        },
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

const updateTopQuizzesByAttemptsChart = (labels, data) => {
  if (topQuizzesByAttemptsChartInstance.value) {
    topQuizzesByAttemptsChartInstance.value.destroy();
  }
  const backgroundColors = ['#36A2EB', '#FF6384', '#FFCE56'];
  const datasets = labels.slice(0, 3).map((quizName, idx) => ({
    label: quizName + ' attempts',
    data: [data[idx]],
    backgroundColor: backgroundColors[idx % backgroundColors.length],
    animation: {
      duration: 0
    },
  }));

  topQuizzesByAttemptsChartInstance.value = new Chart(topQuizzesByAttemptsChart.value, {
    type: 'bar',
    data: {
      labels: [''], // Single x-axis label
      datasets: datasets
    },

    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Attempts' } },
      },
      plugins: {
        legend: {
          display: true
        }
      }
    }
  });
};


// Lifecycle Hooks
onMounted(async () => {
  await getDashboardData();
});
</script>

<style scoped>
.main-content {
  padding: 20px;
}

.card {
  border: none;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

.stat-card {
  border-left: 4px solid;
}

.leaderboard-item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.leaderboard-item:last-child {
  border-bottom: none;
}

canvas {
  min-height: 200px;
}
</style>
