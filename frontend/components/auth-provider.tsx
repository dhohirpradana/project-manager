"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"

interface AuthContextType {
  token: string | null
  user: { id: string; email: string } | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = React.createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [token, setToken] = React.useState<string | null>(null)
  const [user, setUser] = React.useState<{ id: string; email: string } | null>(null)

  React.useEffect(() => {
    const stored = localStorage.getItem('token')
    if (stored) {
      setToken(stored)
      try {
        const payload = JSON.parse(atob(stored.split('.')[1]))
        setUser({ id: payload.sub, email: payload.email })
      } catch {
        /* ignore malformed token */
      }
    }
  }, [])

  const login = async (email: string, password: string) => {
    const res = await api.post<{ token: string }>('/auth/login', { email, password })
    localStorage.setItem('token', res.token)
    setToken(res.token)
    try {
      const payload = JSON.parse(atob(res.token.split('.')[1]))
      setUser({ id: payload.sub, email: payload.email })
    } catch {
      setUser({ id: '', email })
    }
    router.push('/dashboard')
  }

  const register = async (email: string, password: string) => {
    const res = await api.post<{ token: string }>('/auth/register', { email, password })
    localStorage.setItem('token', res.token)
    setToken(res.token)
    setUser({ id: '', email })
    router.push('/dashboard')
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
    router.push('/login')
  }

  return (
    <AuthContext.Provider
      value={{ token, user, login, register, logout, isAuthenticated: !!token }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = React.useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}