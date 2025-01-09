import { defineStore } from 'pinia'

interface User {
  id: number
  name: string
  email: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    isAuthenticated: false,
  }),
  
  actions: {
    setUser(user: User | null) {
      this.user = user
      this.isAuthenticated = !!user
    },
    
    async checkAuth() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/profile/', {
          credentials: 'include'
        })
        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            this.setUser(data.data)
          } else {
            this.setUser(null)
          }
        } else {
          this.setUser(null)
        }
      } catch {
        this.setUser(null)
      }
    },

    async logout() {
      try {
        await fetch('http://127.0.0.1:8000/api/logout/', {
          method: 'POST',
          credentials: 'include'
        })
      } finally {
        this.setUser(null)
      }
    }
  }
}) 