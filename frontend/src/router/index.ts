// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router';

// 1. Define route components.
// These can be imported from other files
import MainPage from '../pages/MainPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import SignUp from '../pages/SignUp.vue';
import Login from '../pages/Login.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

const router = createRouter({
    history: createWebHistory(base),
    routes: [
    { path: '/', name: 'Main Page', component: MainPage },
    { path: '/profile/', name: 'Profile Page', component: ProfilePage },
    { path: '/signup/', name: 'Signup', component: SignUp},
    { path: '/login/', name: 'Login', component: Login},
]
})

export default router
