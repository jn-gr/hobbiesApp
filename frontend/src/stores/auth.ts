import { defineStore } from 'pinia'

interface User {
  id: number
  email: string
  name: string
  date_of_birth: string
  hobbies: Array<{
    id: number
    name: string
  }>
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false
  }),
  
  actions: {
    setUser(userData: User) {
      console.log('Setting user:', userData)
      this.user = userData
      this.isAuthenticated = true
    },
    
    logout() {
      this.user = null
      this.isAuthenticated = false
    }
  }
}) 