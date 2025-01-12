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

            <div class="space-y-2">
              <Label>Hobbies</Label>
              <div class="flex flex-wrap gap-2 mb-2">
                <div 
                  v-for="hobby in formData.hobbies" 
                  :key="hobby.id"
                  class="bg-primary/10 text-primary px-3 py-1 rounded-full flex items-center gap-2"
                >
                  {{ hobby.name }}
                  <button 
                    @click="removeHobby(hobby)" 
                    class="hover:text-destructive"
                    type="button"
                  >
                    ×
                  </button>
                </div>
              </div>
              
              <div class="mb-4">
                <Label>Select from existing hobbies:</Label>
                <Select
                  v-model="selectedHobbyId"
                  @update:modelValue="handleExistingHobbySelect"
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

      <Card class="mt-8">
        <CardHeader>
          <CardTitle>Logout</CardTitle>
          <CardDescription>
            Sign out of your account
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <Button 
            variant="destructive" 
            @click="logout" 
            class="w-full"
          >
            Logout
          </Button>
        </CardContent>
      </Card>
    </div>

    <div v-else class="text-center min-h-[calc(100svh-124px)] flex items-center justify-center p-4 bg-background">
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
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface Hobby {
  id: number
  name: string
}

interface ProfileFormData {
  id: number
  name: string
  email: string
  date_of_birth: string
  hobbies: Hobby[]
}

const router = useRouter()
const authStore = useAuthStore()
const availableHobbies = ref<Hobby[]>([])
const newHobby = ref("")
const selectedHobbyId = ref("")

const formData = reactive<ProfileFormData>({
  id: authStore.user?.id || 0,
  name: authStore.user?.name || '',
  email: authStore.user?.email || '',
  date_of_birth: authStore.user?.date_of_birth || '',
  hobbies: Array.isArray(authStore.user?.hobbies) ? [...authStore.user.hobbies] : [],
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
      const data = await response.json()
      availableHobbies.value = data
      console.log('Available hobbies:', data)
    }
  } catch (error) {
    toast.error("Failed to fetch hobbies")
  }
}

const fetchUserProfile = async (): Promise<void> => {
  try {
    const csrfToken = await authStore.setCsrfToken()
    const response = await fetch("http://localhost:8000/api/profile/", {
      credentials: 'include',
      headers: {
        'X-CSRFToken': csrfToken
      }
    })
    if (response.ok) {
      const userData = await response.json()
      console.log('User data:', userData)
      if (userData.success) {
        Object.assign(formData, userData.data)
        authStore.setUser(userData.data)
      }
    }
  } catch (error) {
    toast.error("Failed to fetch profile")
  }
}

const getChangedFields = () => {
  const changes: Partial<ProfileFormData> = {}
  
  if (formData.name !== authStore.user?.name) {
    changes.name = formData.name
  }
  
  if (formData.email !== authStore.user?.email) {
    changes.email = formData.email
  }
  
  if (formData.date_of_birth !== authStore.user?.date_of_birth) {
    changes.date_of_birth = formData.date_of_birth
  }
  
  // Always include hobbies if they're present in formData
  if (formData.hobbies.length > 0) {
    changes.hobbies = formData.hobbies
  }
  
  return changes
}

const submitUpdateProfile = async (): Promise<void> => {
  try {
    const changes = getChangedFields()

    if (Object.keys(changes).length === 0) {
      toast.info("No changes to update")
      return
    }
    
    const csrfToken = await authStore.setCsrfToken()
    const response = await fetch("http://localhost:8000/api/profile/update/", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(changes),
      credentials: 'include'
    })
    
    const result = await response.json()
    console.log('Update response:', result)
    
    if (result.success) {
      Object.assign(formData, result.data)
      authStore.setUser(result.data)
      toast.success(result.message)
    } else {
      toast.error(result.message)
    }
  } catch (error) {
    console.error('Update error:', error)
    toast.error("Failed to update profile")
  }
}

const submitUpdatePassword = async (): Promise<void> => {
  try {
    const csrfToken = await authStore.setCsrfToken()
    const response = await fetch("http://localhost:8000/api/profile/password/", {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        'X-CSRFToken': csrfToken
      },
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

const logout = async () => {
  try {
    await authStore.logout(router)
  } catch (error) {
    console.error(error)
  }
}

const handleExistingHobbySelect = (id: string) => {
  const hobby = availableHobbies.value.find(h => h.id === Number(id))
  if (hobby && !formData.hobbies.some(h => h.id === hobby.id)) {
    formData.hobbies.push(hobby)
  }
  selectedHobbyId.value = ""
}

const addNewHobby = async () => {
  const hobbyName = newHobby.value.trim()
  if (hobbyName && !formData.hobbies.some(h => h.name.toLowerCase() === hobbyName.toLowerCase())) {
    try {
      const csrfToken = await authStore.setCsrfToken()
      const response = await fetch("http://localhost:8000/api/hobbies/", {
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
        formData.hobbies.push(newHobbyData)
        newHobby.value = ""
        await fetchHobbies()
      } else {
        toast.error("Failed to add hobby")
      }
    } catch (error) {
      toast.error("Failed to add hobby")
    }
  }
}

const removeHobby = (hobby: Hobby) => {
  formData.hobbies = formData.hobbies.filter(h => h.id !== hobby.id)
}

onMounted(() => {
  fetchHobbies()
  if (authStore.isAuthenticated) {
    fetchUserProfile()
  }
})
</script>
