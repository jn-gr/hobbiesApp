<template>
  <div class="min-h-[calc(100svh-57px)] flex items-center justify-center p-4 bg-background">
    <Card class="w-full max-w-lg shadow-lg">
      <CardHeader class="space-y-1">
        <CardTitle class="text-2xl font-bold text-center">Create an Account</CardTitle>
        <CardDescription class="text-center">
          Enter your details below to create your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSignup" class="space-y-6">
          <div class="space-y-2">
            <Label for="name">Full Name</Label>
            <Input 
              id="name"
              v-model="formData.name" 
              placeholder="Enter your name"
              class="w-full"
              required 
            />
          </div>
          
          <div class="space-y-2">
            <Label for="email">Email</Label>
            <Input 
              id="email" 
              type="email" 
              v-model="formData.email" 
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
              v-model="formData.password" 
              placeholder="Create a password"
              class="w-full"
              required 
            />
          </div>

          <div class="space-y-2">
            <Label for="dob">Date of Birth</Label>
            <Input
              id="dob"
              type="date"
              v-model="formData.date_of_birth"
              :max="getCurrentDate()"
              required
            />
          </div>

          <div class="space-y-2">
            <Label>Hobbies</Label>
            <div class="flex flex-wrap gap-2 mb-2">
              <div 
                v-for="hobby in selectedHobbies" 
                :key="hobby.id"
                class="bg-primary/10 text-primary px-3 py-1 rounded-full flex items-center gap-2"
              >
                {{ hobby.name }}
                <button 
                  @click="removeHobby(hobby)" 
                  class="hover:text-destructive"
                >
                  x
                </button>
              </div>
            </div>
            
            <div class="mb-4">
              <Label>Select from existing hobbies:</Label>
              <Select
                v-model="selectedHobbyId"
                @update:modelValue="(value: string) => handleExistingHobbySelect(Number(value))"
              >
                <SelectTrigger>
                  <SelectValue placeholder="Choose a hobby" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectItem
                      v-for="hobby in availableHobbies"
                      :key="hobby.id"
                      :value="String(hobby.id)"
                    >
                      {{ hobby.name }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
            
            <div class="flex gap-2">
              <Input 
                v-model="newHobby" 
                placeholder="Or type a new hobby" 
                class="flex-1"
              />
              <Button 
                type="button" 
                @click="addNewHobby" 
                variant="outline"
              >
                Add
              </Button>
            </div>
          </div>

          <Button type="submit" class="w-full" :disabled="isLoading">
            <div v-if="isLoading">
              <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            </div>
            <div v-else>
              Create Account
            </div>
          </Button>

          <p class="text-center text-sm text-muted-foreground">
            Already have an account?
            <router-link 
              to="/login" 
              class="text-primary hover:underline"
            >
              Login here
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

.spinner-border {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 0.1em solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: spinner-border 0.75s linear infinite;
}

@keyframes spinner-border {
  100% {
    transform: rotate(360deg);
  }
}
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { toast } from 'vue-sonner'

interface Hobby {
  id: number
  name: string
}

interface FormData {
  name: string
  email: string
  password: string
  date_of_birth: string
}

const router = useRouter()
const authStore = useAuthStore()

const formData = ref<FormData>({
  name: "",
  email: "",
  password: "",
  date_of_birth: "",
})
const selectedHobbies = ref<Hobby[]>([])
const availableHobbies = ref<Hobby[]>([])
const newHobby = ref("")
const selectedHobbyId = ref("")
const isLoading = ref(false)

const fetchAvailableHobbies = async () => {
  try {
    const response = await fetch("https://group39-web-apps-ec21653.apps.a.comp-teach.qmul.ac.uk/api/hobbies/", {
      credentials: 'include'
    })
    if (response.ok) {
      availableHobbies.value = await response.json()
    }
  } catch (error) {
    toast.error("Failed to fetch hobbies")
  }
}

const handleSignup = async () => {
  isLoading.value = true
  try {
    const csrfToken = await authStore.setCsrfToken()
    
    const response = await fetch("https://group39-web-apps-ec21653.apps.a.comp-teach.qmul.ac.uk/api/signup/", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        'X-CSRFToken': csrfToken
      },
      credentials: 'include',
      body: JSON.stringify({
        name: formData.value.name,
        email: formData.value.email,
        password: formData.value.password,
        date_of_birth: formData.value.date_of_birth,
        hobbies: selectedHobbies.value,
      }),
    })

    const data = await response.json()

    if (data.success) {
      toast.success(data.message)
      await router.push("/profile")
    } else {
      toast.error(data.message || "Signup failed.")
    }
  } catch (error) {
    toast.error("An error occurred during signup.")
  } finally {
    isLoading.value = false
  }
}

const handleExistingHobbySelect = (id: number) => {
  const hobby = availableHobbies.value.find(h => h.id === id)
  if (hobby && !selectedHobbies.value.some(h => h.id === hobby.id)) {
    selectedHobbies.value.push(hobby)
  }
  selectedHobbyId.value = ""
}

const addNewHobby = async () => {
  const hobbyName = newHobby.value.trim()
  if (hobbyName && !selectedHobbies.value.some(h => h.name === hobbyName)) {
    try {
      const csrfToken = await authStore.setCsrfToken()
      
      const response = await fetch("https://group39-web-apps-ec21653.apps.a.comp-teach.qmul.ac.uk/api/hobbies/", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          'X-CSRFToken': csrfToken
        },
        credentials: 'include',
        body: JSON.stringify({ name: hobbyName }),
      })
      
      if (response.ok) {
        const newHobbyData = await response.json()
        selectedHobbies.value.push(newHobbyData)
        newHobby.value = ""
        await fetchAvailableHobbies()
      } else {
        toast.error("Failed to add hobby")
      }
    } catch (error) {
      toast.error("Failed to add hobby")
    }
  }
}

const removeHobby = (hobby: Hobby) => {
  selectedHobbies.value = selectedHobbies.value.filter(h => h.id !== hobby.id)
}

const getCurrentDate = () => {
  return new Date().toISOString().split('T')[0]
}

onMounted(async () => {
  if (authStore.isAuthenticated) {
    router.push("/profile")
  } else {
    await fetchAvailableHobbies()
  }
})
</script>
