<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { UserPlus, Compass } from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'
import { toast } from 'vue-sonner'
import { useAuthStore } from '../stores/auth'

interface User {
  id: number
  name: string
  common_hobbies: number
  age: number | null
  isFriend: boolean
  requestSent: boolean
}

const route = useRoute()
const router = useRouter()
const users = ref<User[]>([])
const totalPages = ref(0)
const currentPage = ref(1)
const ageMin = ref('')
const ageMax = ref('')
const isLoading = ref(false)
const authStore = useAuthStore()

onMounted(() => {
  const { page, age_min, age_max } = route.query
  currentPage.value = Number(page) || 1
  ageMin.value = String(age_min || '')
  ageMax.value = String(age_max || '')
  fetchUsers()
})

const fetchUsers = async () => {
  try {
    isLoading.value = true
    const params = new URLSearchParams({
      page: String(currentPage.value)
    })
    
    if (ageMin.value) params.append('age_min', ageMin.value)
    if (ageMax.value) params.append('age_max', ageMax.value)
    
    const csrfToken = await authStore.setCsrfToken()
    const response = await fetch(`https://group39-web-apps-ec22572.apps.a.comp-teach.qmul.ac.uk/api/similar_users/?${params}`, {
      credentials: 'include',
      headers: {
        'X-CSRFToken': csrfToken
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      users.value = data.users
      totalPages.value = Math.ceil(data.total_count / 9)

      router.push({
        query: {
          ...(currentPage.value > 1 && { page: currentPage.value }),
          ...(ageMin.value && { age_min: ageMin.value }),
          ...(ageMax.value && { age_max: ageMax.value })
        }
      })
    } else {
      console.error('Failed response:', await response.text())
    }
  } catch (error) {
    console.error('Failed to fetch users:', error)
  } finally {
    isLoading.value = false
  }
}

const applyFilters = () => {
  currentPage.value = 1 
  fetchUsers()
}

const goToPage = (page: number) => {
  currentPage.value = page
  fetchUsers()
}

const getAvatarUrl = (name: string) => {
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random`
}

const sendFriendRequest = async (userId: number) => {
  try {
    const csrfToken = await authStore.setCsrfToken()
    const response = await fetch(`https://group39-web-apps-ec22572.apps.a.comp-teach.qmul.ac.uk/api/friend_requests/send/${userId}/`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken': csrfToken
      }
    })
    
    if (response.ok) {
      toast.success('Friend request sent!')
      await fetchUsers()
    } else {
      const data = await response.json()
      toast.error(data.error || 'Failed to send friend request')
    }
  } catch (error) {
    toast.error('Failed to send friend request')
  }
}

onMounted(async () => {
  await fetchUsers()
})
</script>

<template>
  <div class="container mx-auto p-8">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 space-y-6 md:space-y-0">
      <div class="flex items-center gap-2">
        <Compass class="h-6 w-6" />
        <h1 class="text-2xl font-bold">Discover</h1>
      </div>
      
      <div class="flex items-end gap-4 flex-wrap">
        <div class="space-y-2">
          <Label>Age Range</Label>
          <div class="flex items-center gap-2">
            <Input
              v-model="ageMin"
              type="number"
              placeholder="Min"
              class="w-24"
            />
            <span>-</span>
            <Input
              v-model="ageMax"
              type="number"
              placeholder="Max"
              class="w-24"
            />
          </div>
        </div>
        <Button @click="applyFilters">Apply Filters</Button>
      </div>
    </div>

    <div v-if="isLoading && users.length === 0" class="text-center py-12">
      <p>Loading users...</p>
    </div>

    <div v-else-if="!isLoading && users.length === 0" class="text-center py-12">
      <h3 class="text-lg font-semibold">No users found</h3>
      <p class="text-muted-foreground">
        Try adjusting your filters or add some hobbies to your profile to find users with similar interests.
      </p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card v-for="user in users" :key="user.id" class="relative" id="filteredUsers">
        <Button
          v-if="!user.isFriend && !user.requestSent"
          class="absolute top-4 right-4"
          variant="outline"
          size="sm"
          @click="sendFriendRequest(user.id)"
          id="sendRequest"
        >
          <UserPlus />
        </Button>
        <Button 
          v-else-if="user.requestSent"
          class="absolute top-4 right-4"
          variant="secondary"
          size="sm"
          disabled
        >
          Request Sent
        </Button>
        <Button
          v-else
          class="absolute top-4 right-4"
          variant="secondary"
          size="sm"
          disabled
        >
          Friends
        </Button>

        <CardContent class="pt-6">
          <div class="flex items-start gap-4">
            <img
              :src="getAvatarUrl(user.name)"
              :alt="user.name"
              class="rounded-full w-16 h-16"
            />
            <div>
              <h3 class="font-semibold text-lg">{{ user.name }}</h3>
              <p class="text-sm text-muted-foreground">
                {{ user.age ? `${user.age} years old` : 'Age not specified' }}
              </p>
              <p class="text-sm text-muted-foreground">
                {{ user.common_hobbies }} shared {{ user.common_hobbies === 1 ? 'hobby' : 'hobbies' }}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <div class="mt-8 flex justify-end items-center gap-2">
      <Button
        variant="outline"
        size="sm"
        :disabled="currentPage === 1 || isLoading"
        @click="goToPage(currentPage - 1)"
      >
        Previous
      </Button>
      
      <div class="flex items-center gap-1">
        <Button
          v-for="page in totalPages"
          :key="page"
          variant="outline"
          size="sm"
          :class="{
            'bg-primary text-primary-foreground': page === currentPage
          }"
          @click="goToPage(page)"
        >
          {{ page }}
        </Button>
      </div>
      
      <Button
        variant="outline"
        size="sm"
        :disabled="currentPage === totalPages || isLoading"
        @click="goToPage(currentPage + 1)"
      >
        Next
      </Button>
    </div>
  </div>
</template>
