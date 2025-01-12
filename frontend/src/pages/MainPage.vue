<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

const authStore = useAuthStore()
const router = useRouter()

const logout = async () => {
  try {
    await authStore.logout(router)
  } catch (error) {
    console.error(error)
  }
}

onMounted(async () => {
  await authStore.fetchUser()
})
</script>

<template>
  <div class="container mx-auto p-8">
    <Card class="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle class="text-3xl">Welcome to the Dashboard</CardTitle>
      </CardHeader>
      <CardContent>
        <div v-if="authStore.isAuthenticated" class="space-y-4">
          <h2 class="text-2xl font-semibold">
            Hi there {{ authStore.user?.email }}!
          </h2>
          <p class="text-muted-foreground">
            You are currently logged in to your account.
          </p>
          <Button @click="logout" variant="destructive">
            Logout
          </Button>
        </div>
        <div v-else class="space-y-4">
          <p class="text-muted-foreground">
            You are not logged in.
          </p>
          <Button asChild>
            <router-link to="/login">Login</router-link>
          </Button>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
