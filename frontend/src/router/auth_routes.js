import Login from "@/views/auth/Login.vue";
import Signup from "@/views/auth/Signup.vue";
import ResetPassword from "@/views/auth/ResetPassword.vue";
import ForgotPassword from "@/views/auth/ForgotPassword.vue";
import ConfirmEmail from "@/views/auth/ConfirmEmail.vue";

const auth_routes = [
    {
        path: "/login",
        name: "Login",
        component: Login,
        meta: { requiresAuth: false },
    },
    {
        path: "/signup",
        name: "Signup",
        component: Signup,
    },
    {
        path: "/forgot-password",
        name: "ForgotPassword",
        component: ForgotPassword
    },
    {
        path: "/reset-password/:token",
        name: "ResetPassword",
        component: ResetPassword
    },
    {
        path: "/confirm-email/:token",
        name: "ConfirmEmail",
        component: ConfirmEmail
    },
]

export default auth_routes;