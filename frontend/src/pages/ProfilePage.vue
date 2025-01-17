<template>
  <div class="container mx-auto p-4 md:p-8">
    <div v-if="authStore.isAuthenticated" class="grid grid-cols-12 gap-8">
      <div class="col-span-12 md:col-span-3">
        <div>
          <nav class="space-y-1">
            <button
              v-for="item in navigationItems"
              :key="item.id"
              @click="item.id === 'logout' ? logout() : router.push({ query: { tab: item.id } })"
              class="w-full flex items-center gap-3 px-4 py-3 hover:bg-accent hover:text-black transition-colors rounded-xl"
              :class="[
                currentSection === item.id ? 'bg-accent text-black' : 'text-muted-foreground'
              ]"
            >
              <component :is="item.icon" class="h-5 w-5" />
              {{ item.label }}
            </button>
          </nav>
        </div>
      </div>

      <div class="col-span-12 md:col-span-9">
        <div v-if="currentSection === 'edit'" class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Edit Profile</CardTitle>
              <CardDescription> Update your personal information </CardDescription>
            </CardHeader>
            <CardContent>
              <form @submit.prevent="submitUpdateProfile" class="space-y-6">
                <div class="flex items-center gap-6 mb-8">
                  <div class="relative">
                    <img
                      :src="getAvatarUrl(formData.name)"
                      :alt="formData.name"
                      class="rounded-full w-24 h-24 md:w-32 md:h-32 border-4 border-background shadow-xl"
                    />
                  </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div class="md:col-span-1 space-y-6">
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
                        v-model="formData.date_of_birth"
                        :max="getCurrentDate()"
                      />
                    </div>
                  </div>

                  <div class="space-y-6">
                    <Label>Hobbies</Label>
                    <div class="flex flex-wrap gap-2 mb-4">
                      <Badge
                        v-for="hobby in formData.hobbies"
                        :key="hobby.id"
                        variant="secondary"
                        class="flex items-center gap-1 px-3 py-1"
                      >
                        {{ hobby.name }}
                        <button
                          @click="removeHobby(hobby)"
                          class="hover:text-destructive ml-1"
                          type="button"
                        >
                          <X class="h-3 w-3" />
                        </button>
                      </Badge>
                      <Badge
                        variant="outline"
                        class="cursor-pointer hover:bg-secondary"
                        @click="showHobbyDialog = true"
                        id="editHobby"
                      >
                        <Plus class="h-3 w-3 mr-1" />
                        Add Hobby
                      </Badge>
                    </div>
                  </div>
                </div>

                <div class="flex justify-end">
                  <Button type="submit" class="w-full md:w-auto" id="saveChanges">
                    Save Changes
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>

        <div v-if="currentSection === 'security'" class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Security Settings</CardTitle>
              <CardDescription> Update your password </CardDescription>
            </CardHeader>
            <CardContent>
              <form @submit.prevent="submitUpdatePassword" class="space-y-6">
                <div class="grid gap-4">
                  <div class="space-y-2">
                    <Label for="oldPassword">Current Password</Label>
                    <Input
                      id="oldPassword"
                      type="password"
                      v-model="passwordData.oldPassword"
                      placeholder="Enter current password"
                    />
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                      <Label for="confirmPassword">Confirm Password</Label>
                      <Input
                        id="confirmPassword"
                        type="password"
                        v-model="passwordData.confirmPassword"
                        placeholder="Confirm new password"
                      />
                    </div>
                  </div>
                </div>

                <div class="flex justify-end">
                  <Button type="submit"> Update Password </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>

        <div v-if="currentSection === 'friends'" class="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Friends</CardTitle>

              <CardDescription class="flex items-center justify-between"
                ><span>Manage your connections</span>
                <span
                  class="flex items-center justify-center bg-accent py-1 px-3 rounded-full text-[0.6rem]"
                  >{{ friends.length }}</span
                ></CardDescription
              >
            </CardHeader>
            <CardContent>
              <div v-if="friends.length === 0" class="text-center py-6 text-muted-foreground">
                <Users class="h-12 w-12 mx-auto mb-2 opacity-50" />
                <p>No friends yet</p>
                <p class="text-sm">Start connecting with others!</p>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="friend in friends"
                  :key="friend.id"
                  class="flex items-center gap-3 p-2 rounded-lg hover:bg-secondary/50 transition-colors"
                >
                  <img
                    :src="getAvatarUrl(friend.name)"
                    :alt="friend.name"
                    class="rounded-full w-10 h-10"
                  />
                  <div class="flex-1 min-w-0">
                    <p class="font-medium truncate">{{ friend.name }}</p>
                    <p class="text-sm text-muted-foreground truncate">{{ friend.email }}</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Friend Requests</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="space-y-6">
                <div>
                  <h3
                    class="flex items-center justify-between font-medium text-sm text-muted-foreground mb-3"
                  >
                    <span>Received</span>
                    <span
                      class="flex items-center justify-center bg-accent py-1 px-3 rounded-full text-[0.6rem]"
                      >{{ receivedRequests.length }}</span
                    >
                  </h3>
                  <div
                    v-if="receivedRequests.length === 0"
                    class="text-center py-4 text-sm text-muted-foreground"
                  >
                    No pending requests
                  </div>
                  <div v-else class="space-y-3">
                    <div
                      v-for="request in receivedRequests"
                      :key="request.id"
                      class="flex items-center gap-3 p-2 rounded-lg bg-secondary/50"
                      id="receivedRequests"
                    >
                      <img
                        :src="getAvatarUrl(request.from_user || '')"
                        :alt="request.from_user"
                        class="rounded-full w-8 h-8"
                      />
                      <div class="flex-1 min-w-0">
                        <p class="font-medium truncate">{{ request.from_user }}</p>
                      </div>
                      <div class="flex gap-2">
                        <Button
                          size="sm"
                          variant="default"
                          @click="handleFriendRequest(request.id, 'accept')"
                          id="accept"
                        >
                          Accept
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          @click="handleFriendRequest(request.id, 'reject')"
                          id="reject"
                        >
                          Reject
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <h3
                    class="flex items-center justify-between font-medium text-sm text-muted-foreground mb-3"
                  >
                    <span>Sent</span>
                    <span
                      class="flex items-center justify-center bg-accent py-1 px-3 rounded-full text-[0.6rem]"
                      >{{ sentRequests.length }}</span
                    >
                  </h3>
                  <div
                    v-if="sentRequests.length === 0"
                    class="text-center py-4 text-sm text-muted-foreground"
                  >
                    No pending requests
                  </div>
                  <div v-else class="space-y-3">
                    <div
                      v-for="request in sentRequests"
                      :key="request.id"
                      class="flex items-center gap-3 p-2 rounded-lg bg-secondary/50"
                    >
                      <img
                        :src="getAvatarUrl(request.to_user || '')"
                        :alt="request.to_user"
                        class="rounded-full w-8 h-8"
                      />
                      <div class="flex-1 min-w-0">
                        <p class="font-medium truncate">{{ request.to_user }}</p>
                        <p class="text-sm text-muted-foreground">Pending</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>

    <div
      v-else
      class="text-center min-h-[calc(100svh-124px)] flex items-center justify-center p-4 bg-background"
    >
      <Card>
        <CardHeader>
          <CardTitle>Not Signed In</CardTitle>
          <CardDescription> Please sign in to view and edit your profile. </CardDescription>
        </CardHeader>
        <CardContent>
          <Button @click="goToSignin">Go to Sign In</Button>
        </CardContent>
      </Card>
    </div>

    <Dialog :open="showHobbyDialog" @update:open="showHobbyDialog = false">
      <DialogContent class="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add Hobby</DialogTitle>
          <DialogDescription> Choose from existing hobbies or add a new one </DialogDescription>
        </DialogHeader>

        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <Label>Select existing hobby</Label>
            <Select v-model="selectedHobbyId" @update:modelValue="handleExistingHobbySelect">
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

          <div class="space-y-2">
            <Label>Or add a new hobby</Label>
            <div class="flex gap-2">
              <Input v-model="newHobby" placeholder="Type a new hobby" class="flex-1" />
              <Button type="button" @click="addNewHobby" variant="secondary"> Add </Button>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" @click="showHobbyDialog = false"> Close </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
  import { reactive, ref, onMounted, watch } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useAuthStore } from '../stores/auth'
  import { toast } from 'vue-sonner'
  import { Button } from '@/components/ui/button'
  import { Input } from '@/components/ui/input'
  import { Label } from '@/components/ui/label'
  import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
  import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue
  } from '@/components/ui/select'
  import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle
  } from '@/components/ui/dialog'
  import { Badge } from '@/components/ui/badge'
  import { User, Users, LogOut, Plus, X, Shield } from 'lucide-vue-next'

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

  interface FriendRequest {
    id: number
    from_user?: string
    to_user?: string
    status: string
    created_at: string
  }

  interface Friend {
    id: number
    name: string
    email: string
  }

  const router = useRouter()
  const route = useRoute()
  const authStore = useAuthStore()
  const availableHobbies = ref<Hobby[]>([])
  const newHobby = ref('')
  const selectedHobbyId = ref('')
  const sentRequests = ref<FriendRequest[]>([])
  const receivedRequests = ref<FriendRequest[]>([])
  const friends = ref<Friend[]>([])
  const showHobbyDialog = ref(false)
  const currentSection = ref(route.query.tab?.toString() || 'edit')

  const navigationItems = [
    {
      id: 'edit',
      label: 'Edit Profile',
      icon: User
    },
    {
      id: 'security',
      label: 'Security',
      icon: Shield
    },
    {
      id: 'friends',
      label: 'Friends',
      icon: Users
    },
    {
      id: 'logout',
      label: 'Logout',
      icon: LogOut
    }
  ]

  const formData = reactive<ProfileFormData>({
    id: authStore.user?.id || 0,
    name: authStore.user?.name || '',
    email: authStore.user?.email || '',
    date_of_birth: authStore.user?.date_of_birth
      ? new Date(authStore.user.date_of_birth).toISOString().split('T')[0]
      : '',
    hobbies: Array.isArray(authStore.user?.hobbies) ? [...authStore.user.hobbies] : []
  })

  const passwordData = reactive({
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  })

  const fetchHobbies = async (): Promise<void> => {
    try {
      const csrfToken = await authStore.setCsrfToken()
      const response = await fetch('http://127.0.0.1:8000/api/hobbies/', {
        credentials: 'include',
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
      if (response.ok) {
        const data = await response.json()
        availableHobbies.value = data
        console.log('Available hobbies:', data)
      }
    } catch (error) {
      toast.error('Failed to fetch hobbies')
    }
    console.log('hi')
  }

  const fetchUserProfile = async (): Promise<void> => {
    try {
      const csrfToken = await authStore.setCsrfToken()
      const response = await fetch('http://127.0.0.1:8000/api/profile/', {
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
      toast.error('Failed to fetch profile')
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

    if (formData.hobbies.length > 0) {
      changes.hobbies = formData.hobbies
    }

    return changes
  }

  const submitUpdateProfile = async (): Promise<void> => {
    try {
      const changes = getChangedFields()

      if (Object.keys(changes).length === 0) {
        toast.info('No changes to update')
        return
      }

      const csrfToken = await authStore.setCsrfToken()
      const response = await fetch('http://127.0.0.1:8000/api/profile/update/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
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
      toast.error('Failed to update profile')
    }
  }

  const submitUpdatePassword = async (): Promise<void> => {
    try {
      if (passwordData.newPassword !== passwordData.confirmPassword) {
        toast.error('New passwords do not match')
        return
      }

      if (passwordData.newPassword.length < 8) {
        toast.error('Password must be at least 8 characters long')
        return
      }

      const csrfToken = await authStore.setCsrfToken()
      const response = await fetch('http://127.0.0.1:8000/api/profile/password/update/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(passwordData),
        credentials: 'include'
      })

      const result = await response.json()

      if (result.success) {
        toast.success(result.message)
        passwordData.oldPassword = ''
        passwordData.newPassword = ''
        passwordData.confirmPassword = ''
      } else {
        toast.error(result.message)
      }
    } catch (error) {
      console.error('Password update error:', error)
      toast.error('Failed to update password')
    }
  }

  const goToSignin = (): void => {
    router.push('/login')
  }

  const logout = async () => {
    try {
      await authStore.logout(router)
    } catch (error) {
      console.error(error)
    }
  }

  const handleExistingHobbySelect = (id: string) => {
    const hobby = availableHobbies.value.find((h) => h.id === Number(id))
    if (hobby && !formData.hobbies.some((h) => h.id === hobby.id)) {
      formData.hobbies.push(hobby)
    }
    selectedHobbyId.value = ''
  }

  const addNewHobby = async () => {
    const hobbyName = newHobby.value.trim()
    if (
      hobbyName &&
      !formData.hobbies.some((h) => h.name.toLowerCase() === hobbyName.toLowerCase())
    ) {
      try {
        const csrfToken = await authStore.setCsrfToken()
        const response = await fetch('http://127.0.0.1:8000/api/hobbies/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          credentials: 'include',
          body: JSON.stringify({ name: hobbyName })
        })

        if (response.ok) {
          const newHobbyData = await response.json()
          formData.hobbies.push(newHobbyData)
          newHobby.value = ''
          await fetchHobbies()
        } else {
          toast.error('Failed to add hobby')
        }
      } catch (error) {
        toast.error('Failed to add hobby')
      }
    }
  }

  const removeHobby = (hobby: Hobby) => {
    formData.hobbies = formData.hobbies.filter((h) => h.id !== hobby.id)
  }

  const getCurrentDate = () => {
    return new Date().toISOString().split('T')[0]
  }

  const fetchFriendRequests = async () => {
    try {
      const csrfToken = await authStore.setCsrfToken()

      const sentResponse = await fetch('http://127.0.0.1:8000/api/friend_requests/sent/', {
        credentials: 'include',
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
      if (sentResponse.ok) {
        const data = await sentResponse.json()
        sentRequests.value = data.sent_requests
      }

      const receivedResponse = await fetch('http://127.0.0.1:8000/api/friend_requests/received/', {
        credentials: 'include',
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
      if (receivedResponse.ok) {
        const data = await receivedResponse.json()
        receivedRequests.value = data.received_requests
      }
    } catch (error) {
      toast.error('Failed to fetch friend requests')
    }
  }

  const fetchFriends = async () => {
    try {
      const csrfToken = await authStore.setCsrfToken()
      const response = await fetch('http://127.0.0.1:8000/api/friends/', {
        credentials: 'include',
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
      if (response.ok) {
        const data = await response.json()
        friends.value = data.friends
      }
    } catch (error) {
      toast.error('Failed to fetch friends list')
    }
  }

  const handleFriendRequest = async (requestId: number, action: 'accept' | 'reject') => {
    try {
      const csrfToken = await authStore.setCsrfToken()
      const response = await fetch(
        `http://127.0.0.1:8000/api/friend_requests/${action}/${requestId}/`,
        {
          method: 'POST',
          credentials: 'include',
          headers: {
            'X-CSRFToken': csrfToken
          }
        }
      )

      if (response.ok) {
        toast.success(`Friend request ${action}ed`)
        await fetchFriendRequests()
        await fetchFriends()
      } else {
        toast.error(`Failed to ${action} friend request`)
      }
    } catch (error) {
      toast.error(`Failed to ${action} friend request`)
    }
  }

  const getAvatarUrl = (name: string) => {
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random`
  }

  watch(
    () => route.query.tab,
    (newTab) => {
      currentSection.value = newTab?.toString() || 'edit'
    }
  )

  onMounted(() => {
    fetchHobbies()
    if (authStore.isAuthenticated) {
      fetchUserProfile()
      fetchFriendRequests()
      fetchFriends()

      const initialTab = route.query.tab?.toString()
      if (initialTab && ['edit', 'security', 'friends'].includes(initialTab)) {
        currentSection.value = initialTab
      }
    }
  })
</script>
