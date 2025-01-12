<template>
  <div class="min-h-[calc(100svh-57px)] flex items-center justify-center p-4 bg-background">
    <Card class="w-full max-w-lg shadow-lg">
      <CardHeader class="space-y-1">
        <CardTitle class="text-2xl font-bold text-center">Welcome Back</CardTitle>
        <CardDescription class="text-center">
          Enter your credentials to access your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-2">
            <Label for="email">Email</Label>
            <Input 
              id="email" 
              type="email" 
              v-model="formData.email" 
              placeholder="Enter your email"
              class="w-full"
              required 
              @input="resetError"
            />
          </div>

          <div class="space-y-2">
            <Label for="password">Password</Label>
            <Input 
              id="password" 
              type="password" 
              v-model="formData.password" 
              placeholder="Enter your password"
              class="w-full"
              required 
              @input="resetError"
            />
          </div>

          <Alert variant="destructive" v-if="error">
            <AlertCircle class="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>
              {{ error }}
            </AlertDescription>
          </Alert>

          <Button type="submit" class="w-full">
            Sign In
          </Button>

          <p class="text-center text-sm text-muted-foreground">
            Don't have an account?
            <router-link 
              to="/signup" 
              class="text-primary hover:underline"
            >
              Create an account
            </router-link>
          </p>
        </form>
      </CardContent>
    </Card>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'
import { AlertCircle } from 'lucide-vue-next'
import { toast } from 'sonner'

interface FormData {
  email: string
  password: string
}

const router = useRouter()
const authStore = useAuthStore()
const error = ref('')
const formData = ref<FormData>({
  email: '',
  password: ''
})

const handleLogin = async () => {
  try {
    await authStore.login(formData.value.email, formData.value.password, router)
    if (!authStore.isAuthenticated) {
      error.value = 'Login failed. Please check your credentials.'
    }
  } catch (err) {
    error.value = 'An error occurred during login: ' + err
    toast.error(error.value)
  }
}

const resetError = () => {
  error.value = ''
}
</script>
