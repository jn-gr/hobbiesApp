<template>
  <div class="container mx-auto p-8 max-w-2xl">
    <div v-if="authStore.isAuthenticated">
      <Card>
        <CardHeader>
          <CardTitle>Profile Settings</CardTitle>
          <CardDescription>
            Manage your account settings and preferences here.
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <form @submit.prevent="submitUpdateProfile" class="space-y-6">
            <div class="space-y-2">
              <Label for="name">Name</Label>
              <Input
                id="name"
                v-model="formData.name"
                :placeholder="authStore.user?.name || 'Enter your name'"
              />
            </div>

            <div class="space-y-2">
              <Label for="email">Email</Label>
              <Input
                id="email"
                type="email"
                v-model="formData.email"
                :placeholder="authStore.user?.email || 'Enter your email'"
              />
            </div>

            <div class="space-y-2">
              <Label for="dob">Date of Birth</Label>
              <Input
                id="dob"
                type="date"
                :value="authStore.user?.date_of_birth || ''"
                v-model="formData.date_of_birth"
              />
            </div>

            <Button type="submit">Update Profile</Button>
          </form>
        </CardContent>
      </Card>

      <Card class="mt-8">
        <CardHeader>
          <CardTitle>Change Password</CardTitle>
          <CardDescription>
            Update your password here. Please enter your current password to confirm changes.
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <form @submit.prevent="submitUpdatePassword" class="space-y-6">
            <div class="space-y-2">
              <Label for="oldPassword">Current Password</Label>
              <Input
                id="oldPassword"
                type="password"
                v-model="passwordData.oldPassword"
                placeholder="Enter current password"
              />
            </div>

            <div class="space-y-2">
              <Label for="newPassword">New Password</Label>
              <Input
                id="newPassword"
                type="password"
                v-model="passwordData.newPassword"
                placeholder="Enter new password"
              />
            </div>

            <div class="space-y-2">
              <Label for="confirmPassword">Confirm New Password</Label>
              <Input
                id="confirmPassword"
                type="password"
                v-model="passwordData.confirmPassword"
                placeholder="Confirm new password"
              />
            </div>

            <Button type="submit" variant="destructive">
              Change Password
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>

    <div v-else class="text-center">
      <Card>
        <CardHeader>
          <CardTitle>Not Signed In</CardTitle>
          <CardDescription>
            Please sign in to view and edit your profile.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="goToSignin">Go to Sign In</Button>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "../stores/auth"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface Hobby {
  id: number
  name: string
}

interface User {
  id: number
  name: string
  email: string
  date_of_birth: string
  hobbies: number[]
}

const router = useRouter()
const authStore = useAuthStore()
const hobbies = ref<Hobby[]>([])

const formData = reactive<User>({
  id: 0,
  name: "",
  email: "",
  date_of_birth: "",
  hobbies: [],
})

const passwordData = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
})

const fetchHobbies = async (): Promise<void> => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/hobbies/")
    if (response.ok) {
      hobbies.value = await response.json()
    }
  } catch (error) {
    toast.error("Failed to fetch hobbies")
  }
}

const fetchUserProfile = async (): Promise<void> => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/profile/", {
      credentials: 'include'
    })
    if (response.ok) {
      const userData = await response.json()
      if (userData.success) {
        Object.assign(formData, userData.data)
        authStore.setUser(userData.data)
      }
    }
  } catch (error) {
    toast.error("Failed to fetch profile")
  }
}

const submitUpdateProfile = async (): Promise<void> => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/profile/update/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
      credentials: 'include'
    })
    const result = await response.json()
    if (result.success) {
      Object.assign(formData, result.data)
      authStore.setUser(result.data)
      toast.success(result.message)
    } else {
      toast.error(result.message)
    }
  } catch (error) {
    toast.error("Failed to update profile")
  }
}

const submitUpdatePassword = async (): Promise<void> => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/profile/password/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(passwordData),
      credentials: 'include'
    })
    const result = await response.json()
    if (result.success) {
      toast.success(result.message)
      passwordData.oldPassword = ""
      passwordData.newPassword = ""
      passwordData.confirmPassword = ""
    } else {
      toast.error(result.message)
    }
  } catch (error) {
    toast.error("Failed to update password")
  }
}

const goToSignin = (): void => {
  router.push("/login")
}

onMounted(() => {
  fetchHobbies()
  if (authStore.isAuthenticated) {
    fetchUserProfile()
  }
})
</script>
