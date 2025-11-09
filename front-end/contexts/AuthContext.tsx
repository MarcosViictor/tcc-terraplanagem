"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { useRouter } from 'next/navigation'
import { authAPI } from '@/lib/api'
import { User, AuthTokens } from '@/types'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Verificar se há usuário salvo no localStorage
    const loadUser = () => {
      try {
        const savedUser = localStorage.getItem('user')
        const token = localStorage.getItem('access_token')

        if (savedUser && token) {
          setUser(JSON.parse(savedUser))
        }
      } catch (error) {
        console.error('Erro ao carregar usuário:', error)
      } finally {
        setLoading(false)
      }
    }

    loadUser()
  }, [])

  const login = async (username: string, password: string) => {
    try {
      setLoading(true)
      const data: AuthTokens = await authAPI.login(username, password)

      // Salvar tokens e usuário
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))

      setUser(data.user)

      // Redirecionar baseado no papel do usuário
      const role = data.user.papel || ''
      switch (role) {
        case 'admin':
          router.push('/admin/dashboard')
          break
        case 'encarregado':
          router.push('/encarregado/equipe')
          break
        case 'operador':
          router.push('/motorista/equipamento')
          break
        default:
          router.push('/apontador/tarefas')
      }
    } catch (error: any) {
      console.error('Erro no login:', error)
      throw new Error(error.response?.data?.detail || 'Erro ao fazer login')
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    // Limpar dados do localStorage
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')

    setUser(null)
    router.push('/login')
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  return context
}
