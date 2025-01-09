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
                  ×
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

          <Button type="submit" class="w-full">
            Create Account
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
</style>

<script lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
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
import { Alert, AlertDescription } from "@/components/ui/alert"
import { toast } from 'sonner'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

interface Hobby {
  id: number;
  name: string;
}

export default {
    components: {
        Button,
        Card,
        CardContent,
        CardDescription,
        CardFooter,
        CardHeader,
        CardTitle,
        Input,
        Label,
        Select,
        SelectContent,
        SelectGroup,
        SelectItem,
        SelectTrigger,
        SelectValue,
        Alert,
        AlertDescription
    },
    setup() {
        const authStore = useAuthStore()
        const router = useRouter()
        
        return {
            authStore,
            router
        }
    },
    data() {
        return {
            formData: {
                name: "",
                email: "",
                password: "",
            },
            selectedHobbies: [] as Hobby[],
            availableHobbies: [] as Hobby[],
            newHobby: "",
            errorMessage: "",
            successMessage: "",
            selectedHobbyId: "" as string,
        };
    },
    methods: {
        async fetchAvailableHobbies() {
            const response = await fetch("http://127.0.0.1:8000/api/hobbies/");
            if (response.ok) {
                this.availableHobbies = await response.json();
            }
        },
        async handleSignup() {
            try {
                const response = await fetch("http://127.0.0.1:8000/api/signup/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        name: this.formData.name,
                        email: this.formData.email,
                        password: this.formData.password,
                        hobbies: this.selectedHobbies,
                    }),
                });

                const data = await response.json();

                if (data.success) {
                    this.authStore.setUser({
                        id: data.user.id,
                        email: this.formData.email,
                        name: this.formData.name,
                        date_of_birth: "",
                        hobbies: this.selectedHobbies
                    });
                    
                    toast.success(data.message);
                    this.router.push("/profile");
                } else {
                    toast.error(data.message || "Signup failed.");
                }
            } catch (error) {
                toast.error("An error occurred during signup.");
            }
        },
        handleExistingHobbySelect(id: number) {
            const hobby = this.availableHobbies.find(h => h.id === id)
            if (hobby && !this.selectedHobbies.some(h => h.id === hobby.id)) {
                this.selectedHobbies.push(hobby)
            }
            this.selectedHobbyId = ""
        },
        async addNewHobby() {
            const hobbyName = this.newHobby.trim()
            if (hobbyName && !this.selectedHobbies.some(h => h.name === hobbyName)) {
                try {
                    const response = await fetch("http://127.0.0.1:8000/api/hobbies/", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ name: hobbyName }),
                    })
                    
                    if (response.ok) {
                        const newHobbyData = await response.json()
                        this.selectedHobbies.push(newHobbyData)
                        this.newHobby = ""
                        await this.fetchAvailableHobbies()
                    } else {
                        toast.error("Failed to add hobby")
                    }
                } catch (error) {
                    toast.error("Failed to add hobby")
                }
            }
        },
        removeHobby(hobby: Hobby) {
            this.selectedHobbies = this.selectedHobbies.filter(h => h.id !== hobby.id);
        }
    },
    mounted() {
        console.log(this.authStore.isAuthenticated);
        this.authStore.isAuthenticated ? this.router.push("/profile") :
        this.fetchAvailableHobbies();
    },
};
</script>