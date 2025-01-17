import { defineStore } from 'pinia'
import { Router } from 'vue-router'
import { toast } from 'vue-sonner';

interface Hobby {
    id: number;
    name: string;
}

interface User {
    id?: number;
    email?: string;
    name?: string;
    date_of_birth?: string;
    hobbies?: Hobby[];
    is_active?: boolean;
}

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => {
        const storedState = localStorage.getItem('authState')
        return storedState ? JSON.parse(storedState) : {
            user: null,
            isAuthenticated: false
        }
    },
    actions: {
        async setCsrfToken(): Promise<string> {
            try {
                console.log('Setting CSRF token...')
                const response = await fetch('http://localhost:8000/api/set-csrf-token/', {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Accept': 'application/json',
                    }
                })

                if (!response.ok) {
                    throw new Error(`Failed to set CSRF token. Status: ${response.status}`)
                }

                const csrfToken = response.headers.get('X-CSRFToken')
                if (csrfToken) {
                    console.log('Got CSRF token from header:', csrfToken.substring(0, 5) + '...')
                    return csrfToken
                }
                await new Promise(resolve => setTimeout(resolve, 500))

                const token = getCSRFToken()
                console.log('Got CSRF token from cookie:', token.substring(0, 5) + '...')
                return token
            } catch (error) {
                console.error('Failed to set CSRF token:', error)
                throw new Error('Failed to set CSRF token. Please ensure cookies are enabled.')
            }
        },

        async login(email: string, password: string, router: Router | null = null) {
            try {
                console.log('Attempting login for email:', email)
                const csrfToken = await this.setCsrfToken()
                
                const response = await fetch('http://localhost:8000/api/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ email, password }),
                    credentials: 'include'
                })
                const data = await response.json()

                if (data.success) {
                    this.user = data.user
                    this.isAuthenticated = true
                    this.saveState()
                    if (router) {
                        toast.success('Login successful')
                        await router.push('/profile')
                    }
                } else {
                    console.log('Login failed:', data.error || 'Unknown error')
                    toast.error(data.error || 'Unknown error')
                    this.user = null
                    this.isAuthenticated = false
                    this.saveState()
                }
            } catch (error) {
                console.error('Login error:', error)
                toast.error('Login failed. Please try again.')
                this.user = null
                this.isAuthenticated = false
                this.saveState()
                throw error
            }
        },

        setUser(userData: User) {
            this.user = userData
            this.isAuthenticated = true
            this.saveState()
        },

        async logout(router: Router | null = null) {
            console.log('Attempting logout')
            try {
                const csrfToken = await this.setCsrfToken()
                const response = await fetch('http://localhost:8000/api/logout/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    credentials: 'include'
                })
                if (response.ok) {
                    console.log('Logout successful')
                    this.user = null
                    this.isAuthenticated = false
                    this.saveState()
                    if (router) {
                        console.log('Redirecting to login page')
                        await router.push({name: "login"})
                    }
                }
            } catch (error) {
                console.error('Logout failed:', error)
                throw error
            }
        },

        async fetchUser() {
            try {
                const response = await fetch('http://localhost:8000/api/profile/', {
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                })
                if (response.ok) {
                    const userData = await response.json()
                    this.user = userData.data
                    this.isAuthenticated = true
                }
                else{
                    this.user = null
                    this.isAuthenticated = false
                }
            } catch (error) {
                console.error('Failed to fetch user', error)
                this.user = null
                this.isAuthenticated = false
            }
            this.saveState()
        },

        saveState() {
            localStorage.setItem('authState', JSON.stringify({
                user: this.user,
                isAuthenticated: this.isAuthenticated
            }))
        }
    }
})

export function getCSRFToken(): string {
    console.log('Checking cookies:', document.cookie)
    
    const name = 'csrftoken'
    let cookieValue = null
    
    if (!document.cookie) {
        console.error('No cookies available - cookies might be disabled')
        throw new Error('Cookies are required but seem to be disabled in your browser.')
    }
    
    if (document.cookie === '') {
        console.error('Empty cookies string')
        throw new Error('No cookies found. Please ensure third-party cookies are enabled.')
    }
    
    const cookies = document.cookie.split(';')
    console.log('Available cookies:', cookies)
    
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
        }
    }
    
    if (cookieValue === null) {
        console.error('CSRF token cookie not found. Available cookies:', document.cookie)
        throw new Error('CSRF token not found. Please check your cookie settings.')
    }
    
    return cookieValue
}
