import { defineStore } from 'pinia'

interface User {
  email: string;
  name: string;
  date_of_birth: string;
  hobbies: string[];
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false
  }),
  
  actions: {
    setUser(userData: User) {
      this.user = userData;
      this.isAuthenticated = true;
    },
    
    logout() {
      this.user = null;
      this.isAuthenticated = false;
    }
  }
}) 