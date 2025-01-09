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

<script lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { toast } from 'sonner'
// import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
    components: {
      Button,
      Card,
      CardContent,
      CardDescription,
      CardHeader,
      CardTitle,
      Input,
      Label,
    },
    data() {
        return {
            form: {
                email: "", 
                password: "",
            }
        };
    },
    methods: {
        async handleLogin() {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.form),
                });

                if (response.ok) {
                    const userData = await response.json();
                    const authStore = useAuthStore();
                    authStore.setUser(userData);
                    const router = useRouter();
                    router.push('/profile');
                }
            } catch (error) {
                toast.error(`Login Failed: ${error}`);
            }
        },
    },
};
</script>