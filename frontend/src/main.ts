import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import './assets/index.css'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

const authStore = useAuthStore()

const initApp = async () => {
    try {
        await authStore.setCsrfToken()
    } catch (error) {
        console.warn('Initial CSRF token setup failed:', error)
    }
    await authStore.fetchUser()
}

initApp().finally(() => {
    app.mount('#app')
})
