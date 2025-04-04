import Add from "@/views/admin/Add.vue";
import AdminStudents from "@/views/admin/AdminStudents.vue";
import AdminDashboard from "@/views/admin/AdminDashboard.vue";
import AdminProfile from "../views/admin/AdminProfile.vue";
import AdminSubjects from "../views/admin/AdminSubjects.vue";
import AdminQuestions from "../views/admin/AdminQuestions.vue";
import AdminChapters from "../views/admin/AdminChapters.vue";
import AdminQuizzes from "../views/admin/AdminQuizzes.vue";
import AdminSubject from "../views/admin/AdminSubject.vue";
import AdminChapter from "../views/admin/AdminChapter.vue";
import AdminQuestion from "../views/admin/AdminQuestion.vue";
import AdminQuiz from "../views/admin/AdminQuiz.vue";
import AdminStudentProfile from "../views/admin/AdminStudent/AdminStudentProfile.vue";
import AdminLeaderboard from "../views/admin/AdminLeaderboard.vue";
import AdminStudentQuizzes from "../views/admin/AdminStudent/AdminStudentQuizzes.vue";
import AdminStudentQuizResults from "../views/admin/AdminStudent/AdminStudentQuizResults.vue";
import AdminStudentSummary from "../views/admin/AdminStudent/AdminStudentSummary.vue";
import AdminContacts from "../views/admin/AdminContacts.vue";
import AdminContact from "../views/admin/AdminContact.vue";
import AdminSettings from "../views/admin/AdminSettings.vue";

const admin_routes = [
    {
        path: "/admin/dashboard",
        name: "AdminDashboard",
        component: AdminDashboard,
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path: "/admin/dashboard/add",
        name: "AdminAdd",
        component: Add,
        meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
        path: "/admin/dashboard/quizzes",
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
            {   
                path: "",
                name: "AdminQuizzes",
                component: AdminQuizzes,
            },
            {
                path: ":id",
                name: "AdminQuiz",
                component: AdminQuiz,
            },
        ]
    },
    {
        path: "/admin/dashboard/students",
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
            {
                path: "",
                name: "AdminStudents",
                component: AdminStudents,
            },
            {
                path: ":id",
                children: [
                    {
                        path: "",
                        name: "AdminStudentProfile",
                        component: AdminStudentProfile
                    },
                    {
                        path: "quizzes",
                        name: "AdminStudentQuizzes",
                        component: AdminStudentQuizzes
                    },
                    {
                        path: "results/:take_quiz_id",
                        name: "AdminStudentQuizResults",
                        component: AdminStudentQuizResults
                    },
                    {
                        path: "summary",
                        name: "AdminStudentSummary",
                        component: AdminStudentSummary
                    }
                ]
            },
        ]
    },
    {
        path: "/admin/dashboard/subjects",
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
            {
                path: "",
                name: "AdminSubjects",
                component: AdminSubjects,
            },
            {
                path: ":id",
                name: "AdminSubject",
                component: AdminSubject,
            },
        ]
    },
    {
        path: "/admin/dashboard/questions",
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
            {
                path: "",
                name: "AdminQuestions",
                component: AdminQuestions,
            },
            {
                path: ":id",
                name: "AdminQuestion",
                component: AdminQuestion,
            },
        ]
    },
    {
        path: "/admin/dashboard/chapters",
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
            {
                path: "",
                name: "AdminChapters",
                component: AdminChapters,
            },
            {
                path: ":id",
                name: "AdminChapter",
                component: AdminChapter,
            },
        ]
    },
    {
        path: "/admin/dashboard/profile",
        name: "AdminProfile",
        component: AdminProfile,
        meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
        path: "/admin/dashboard/leaderboard",
        name: "AdminLeaderboard",
        component: AdminLeaderboard,
        meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
        path: '/admin/dashboard/contacts',
        name: 'AdminContacts',
        component: AdminContacts,
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: '/admin/dashboard/contacts/:id',
        name: 'AdminContact',
        component: AdminContact,
        meta: { requiresAuth: true, requiresAdmin: true }
      },
    {
        path: "/admin/dashboard/settings",
        name: "AdminSettings",
        component: AdminSettings,
        meta: { requiresAuth: true, requiresAdmin: true }
    },
]

export default admin_routes