import Home from "@/views/Home.vue";
import NotFound from "@/views/error/NotFound.vue";
import TermsAndConditions from "../views/auth/TermsAndConditions.vue";

const main_routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },
    {
        path: '/:pathMatch(.*)*', // This will match any path
        name: 'NotFound',
        component: NotFound
    },
    {
        path: '/terms',
        name: 'TermsAndConditions',
        component: TermsAndConditions
    }
]

export default main_routes;