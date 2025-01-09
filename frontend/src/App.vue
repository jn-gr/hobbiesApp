<template>
  <div class="min-h-screen flex flex-col">
    <header class="border-b">
      <div class="container flex h-14 items-center px-4">
        <router-link to="/" class="flex items-center">
          <img 
            src="/logo.png" 
            alt="Logo" 
            class="h-12 w-auto"
          />
        </router-link>

        <nav class="flex-1 flex justify-center items-center space-x-6 text-sm font-medium">
          <router-link
            to="/"
            class="transition-colors hover:text-primary"
          >
            Home
          </router-link>
          <router-link
            :to="{name: 'Profile Page'}"
            class="transition-colors hover:text-primary"
          >
            Profile
          </router-link>
        </nav>

        <div class="flex items-center space-x-4">
          <router-link
            to="/login"
            class="text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md"
          >
            Login
          </router-link>
        </div>
      </div>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import { useAuthStore } from './stores/auth'

export default defineComponent({
  components: { RouterView },
  setup() {
    const authStore = useAuthStore()

    const handleLogout = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/logout/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include'
        });
        
        if (response.ok) {
          authStore.logout();
          // Redirect to login page
          window.location.href = '/login';
        }
      } catch (error) {
        console.error('Logout failed:', error);
      }
    }

    return {
      authStore,
      handleLogout
    }
  }
});
</script>

<style scoped>
</style>
