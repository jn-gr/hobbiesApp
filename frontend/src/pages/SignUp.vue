<template>
  <div class="h-full flex items-center justify-center p-4 bg-background">
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
            
            <div class="flex gap-2">
              <Input 
                v-model="newHobby" 
                placeholder="Type a hobby and press Enter" 
                class="flex-1"
                @keyup.enter="addNewHobby"
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

          <TransitionGroup name="fade">
            <Alert 
              v-if="errorMessage" 
              variant="destructive" 
              class="mt-4"
              key="error"
            >
              <AlertDescription>{{ errorMessage }}</AlertDescription>
            </Alert>

            <Alert 
              v-if="successMessage" 
              variant="default" 
              class="mt-4"
              key="success"
            >
              <AlertDescription>{{ successMessage }}</AlertDescription>
            </Alert>
          </TransitionGroup>

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
                console.log("Signup Response:", data);

                if (data.success) {
                    this.successMessage = data.message;
                    this.errorMessage = "";
                    setTimeout(() => this.$router.push("/login"), 2000);
                } else {
                    this.errorMessage = data.message || "Signup failed.";
                    this.successMessage = "";
                }
            } catch (error) {
                console.error("Error during signup:", error);
                this.errorMessage = "An error has occurred.";
            }
        },
        addNewHobby() {
            const hobbyName = this.newHobby.trim();
            if (hobbyName && !this.selectedHobbies.some(h => h.name === hobbyName)) {
                this.selectedHobbies.push({ id: Date.now(), name: hobbyName });
                this.newHobby = "";
            }
        },
        removeHobby(hobby: Hobby) {
            this.selectedHobbies = this.selectedHobbies.filter(h => h.id !== hobby.id);
        }
    },
    mounted() {
        this.fetchAvailableHobbies();
    },
};
</script>