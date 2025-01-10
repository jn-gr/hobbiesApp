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
    user: JSON.parse(sessionStorage.getItem('user') || 'null') as User | null, // new
    isAuthenticated: !!sessionStorage.getItem('user') // new
  }),
  
  // Storage set specifically to Session Storage. Can also be stored in Local Storage.
  actions: {
    setUser(userData: User) {
      console.log('Setting user:', userData)
      this.user = userData
      this.isAuthenticated = true
      sessionStorage.setItem('user', JSON.stringify(userData)) // new

    },
    
    logout() {
      this.user = null
      this.isAuthenticated = false
      sessionStorage.removeItem('user') // new
    }
  }
}) 