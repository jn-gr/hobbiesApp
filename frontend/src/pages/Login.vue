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
              v-model="form.email" 
              placeholder="Enter your email"
              class="w-full"
              required 
            />
          </div>

          <div class="space-y-2">
            <Label for="password">Password</Label>
            <Input 
              id="password" 
              type="password" 
              v-model="form.password" 
              placeholder="Enter your password"
              class="w-full"
              required 
            />
          </div>

          <Button type="submit" class="w-full">
            Login
          </Button>

          <p class="text-center text-sm text-muted-foreground">
            Don't have an account?
            <router-link 
              to="/signup" 
              class="text-primary hover:underline"
            >
              Sign up here
            </router-link>
          </p>
        </form>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { toast } from 'sonner'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
    email: "",
    password: "",
})

const handleLogin = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(form),
        });

        const data = await response.json()
        console.log('Login response:', data)

        if (data.success && data.user) {
            authStore.setUser(data.user)
            toast.success(data.message)
            router.push('/profile')
        } else {
            toast.error(data.message || 'Login failed')
        }
    } catch (error) {
        console.error('Login error:', error)
        toast.error(`Login Failed: ${error}`)
    }
}
</script>