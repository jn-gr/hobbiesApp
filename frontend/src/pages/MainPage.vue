<template>
  <div class="container mx-auto p-8">
    <Card class="mb-6">
      <CardHeader>
        <CardTitle>Find DiscoverUsers with Similar Interests</CardTitle>
        <CardDescription>
          Discover users who share your hobbies. DiscoverUsers are sorted by the number of hobbies you have in common.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-4">
          <!-- Age Filter -->
          <div class="space-y-2">
            <Label>Filter by Age Range</Label>
            <div class="flex gap-4">
              <div class="flex-1 space-y-2">
                <Label for="min-age" class="text-sm text-muted-foreground">Minimum Age</Label>
                <Input
                  id="min-age"
                  type="number"
                  placeholder="e.g., 18"
                  v-model="filters.ageMin"
                  min="0"
                  max="120"
                />
              </div>
              <div class="flex-1 space-y-2">
                <Label for="max-age" class="text-sm text-muted-foreground">Maximum Age</Label>
                <Input
                  id="max-age"
                  type="number"
                  placeholder="e.g., 30"
                  v-model="filters.ageMax"
                  min="0"
                  max="120"
                />
              </div>
            </div>
          </div>
          
          <Button @click="fetchDiscoverUsers" class="w-full">
            Apply Age Filter
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
    </div>
    
    <!-- Empty State -->
    <div v-else-if="users.length === 0" class="text-center py-8">
      <div class="text-muted-foreground">
        No users found matching your criteria.
      </div>
    </div>
    
    <!-- DiscoverUsers Grid -->
    <div v-else class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <Card v-for="user in users" :key="user.id" class="relative">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            {{ user.name }}
            <Badge variant="secondary">
              {{ user.common_hobbies }} {{ user.common_hobbies === 1 ? 'hobby' : 'hobbies' }} in common
            </Badge>
          </CardTitle>
          <CardDescription>
            {{ user.age }} years old
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <Button 
              v-if="!user.isFriend && !user.requestSent" 
              @click="sendFriendRequest(user.id)"
              variant="outline"
              class="w-full"
            >
              Send Friend Request
            </Button>
            <p v-else-if="user.requestSent" class="text-sm text-muted-foreground text-center">
              Friend request sent
            </p>
            <p v-else class="text-sm text-muted-foreground text-center">
              Already friends
            </p>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Load More -->
    <div v-if="hasNextPage" class="mt-6 text-center">
      <Button @click="loadMore" variant="outline">
        Load More DiscoverUsers
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { toast } from 'sonner'

interface DiscoverUser {
  id: number
  name: string
  age: number
  common_hobbies: number
  isFriend: boolean
  requestSent: boolean
}

const users = ref<DiscoverUser[]>([])
const currentPage = ref(1)
const hasNextPage = ref(false)
const loading = ref(false)

const filters = reactive({
  ageMin: '',
  ageMax: '',
})

const fetchDiscoverUsers = async (resetPage = true) => {
  if (resetPage) {
    currentPage.value = 1
  }
  
  loading.value = true
  try {
    const queryParams = new URLSearchParams({
      page: currentPage.value.toString(),
      ...(filters.ageMin && { age_min: filters.ageMin }),
      ...(filters.ageMax && { age_max: filters.ageMax }),
    })

    const response = await fetch(`http://127.0.0.1:8000/api/similar_users/?${queryParams}`, {
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      if (resetPage) {
        users.value = data.users
      } else {
        users.value = [...users.value, ...data.users]
      }
      hasNextPage.value = data.has_next
    }
  } catch (error) {
    toast.error('Failed to fetch users')
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  currentPage.value++
  fetchDiscoverUsers(false)
}

const sendFriendRequest = async (userId: number) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/friend_requests/send/${userId}/`, {
      method: 'POST',
      credentials: 'include'
    })

    if (response.ok) {
      const data = await response.json()
      toast.success(data.message)
      // Update the user in the list to show request sent
      const userIndex = users.value.findIndex(u => u.id === userId)
      if (userIndex !== -1) {
        users.value[userIndex].requestSent = true
      }
    } else {
      const data = await response.json()
      toast.error(data.error)
    }
  } catch (error) {
    toast.error('Failed to send friend request')
  }
}

// Fetch users on component mount
fetchDiscoverUsers()
</script>

<style scoped>
</style>
