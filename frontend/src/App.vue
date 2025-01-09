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
            v-if="authStore.isAuthenticated"
            :to="{name: 'Profile Page'}" 
            class="transition-colors hover:text-primary"
          >
            Profile
          </router-link>
        </nav>

        <div class="flex items-center space-x-4">
          <template v-if="!authStore.isAuthenticated">
            <router-link
              to="/login"
              class="text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md"
            >
              Login
            </router-link>
            <router-link
              to="/signup"
              class="text-sm font-medium transition-colors hover:text-primary"
            >
              Sign Up
            </router-link>
          </template>
          <template v-else>
            <span class="text-sm text-muted-foreground">
              {{ authStore.user?.name }}
            </span>
            <Button 
              variant="outline" 
              @click="handleLogout"
            >
              Logout
            </Button>
          </template>
        </div>
      </div>
    </header>

    <main class="flex-1">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/auth'
import { toast } from 'sonner'

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  await authStore.logout()
  toast.success('Logged out successfully')
  router.push('/login')
}

onMounted(() => {
  authStore.checkAuth()
})
</script>

<style scoped>
</style>
