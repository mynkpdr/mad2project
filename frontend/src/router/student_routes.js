import StudentDashboard from "../views/student/dashboard/StudentDashboard.vue"
import StudentProfile from "../views/student/dashboard/StudentProfile.vue"
import QuizInterface from "../views/student/QuizInterface.vue"
import PracticeInterface from "../views/student/PracticeInterface.vue"
import Leaderboard from "../views/student/Leaderboard.vue"
import StudentMyQuizzes from "../views/student/dashboard/StudentMyQuizzes.vue"
import BrowseExam from "../views/student/BrowseExam.vue"
import BrowsePractice from "../views/student/BrowsePractice.vue"
import StudentQuizResults from "../views/student/dashboard/StudentQuizResults.vue"
import StudentSettings from "../views/student/dashboard/StudentSettings.vue"

const student_routes = [
  {
    path: "/dashboard",
    meta: { requiresAuth: true },
    children: [
      {
        path: "",
        name: "StudentDashboard",
        component: StudentDashboard,
      },
      {
        path: "profile",
        name: "StudentProfile",
        component: StudentProfile,
      },
      {
        path: "my_quizzes",
        children: [
          {
            path: "",
            name: "StudentMyQuizzes",
            component: StudentMyQuizzes,
          },
          {
            path: ":id",
            name: "StudentQuizResults",
            component: StudentQuizResults,
          }
        ]
      },
      {
        path: "settings",
        name: "StudentSettings",
        component: StudentSettings,
      }
    ]
  },
  {
    path: "/take_quiz/:id",
    name: "QuizInterface",
    component: QuizInterface,
    meta: { requiresAuth: true }
  },
  {
    path: "/take_practice/:id",
    name: "PracticeInterface",
    component: PracticeInterface,
    meta: { requiresAuth: true }
  },
  {
    path: "/browse",
    meta: { requiresAuth: true },
    children: [
      {
        path: "exam",
        name: "BrowseExam",
        component: BrowseExam,
      },
      {
        path: "practice",
        name: "BrowsePractice",
        component: BrowsePractice,
      },
    ]
  },
  {
    path: "/leaderboard",
    name: "Leaderboard",
    component: Leaderboard,
    meta: { requiresAuth: true }
  }
]

export default student_routes