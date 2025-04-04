import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export const useNightModeStore = defineStore('nightMode', () => {
    const isNightMode = ref(localStorage.getItem('nightMode') === 'enabled');
    const router = useRouter()
    // Toggle night mode
    const toggleNightMode = () => {
        isNightMode.value = !isNightMode.value;
        localStorage.setItem('nightMode', isNightMode.value ? 'enabled' : 'disabled');
        // const currentRoute = router.currentRoute.value;
        // router.replace('/reload-temp').then(() => {
        //     router.replace(currentRoute.fullPath);
        // });
        window.location.reload();
        
    };
    

    return {
        isNightMode,
        toggleNightMode,
    };
});
