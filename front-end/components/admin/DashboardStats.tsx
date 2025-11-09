'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, Users, Truck, AlertTriangle } from "lucide-react"
import { equipamentosAPI, funcionariosAPI, obrasAPI } from '@/lib/api'

interface Stats {
  equipamentosAtivos: number
  funcionariosPresentes: number
  obrasAtivas: number
  alertasPendentes: number
}

export function DashboardStats() {
  const [stats, setStats] = useState<Stats>({
    equipamentosAtivos: 0,
    funcionariosPresentes: 0,
    obrasAtivas: 0,
    alertasPendentes: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchStats() {
      try {
        // Buscar equipamentos ativos
        const equipamentos = await equipamentosAPI.list()
        const equipamentosAtivos = equipamentos.filter((e: any) => 
          e.ativo && e.status === 'operacional'
        ).length

        // Buscar funcionários
        const funcionarios = await funcionariosAPI.list()
        const funcionariosPresentes = funcionarios.filter((f: any) => f.ativo).length

        // Buscar obras ativas
        const obras = await obrasAPI.list()
        const obrasAtivas = obras.filter((o: any) => 
          o.ativo && o.status === 'em_andamento'
        ).length

        setStats({
          equipamentosAtivos,
          funcionariosPresentes,
          obrasAtivas,
          alertasPendentes: 0 // TODO: implementar lógica de alertas
        })
      } catch (error) {
        console.error('Erro ao buscar estatísticas:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} className="animate-pulse">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <div className="h-4 bg-muted rounded w-24"></div>
              <div className="h-4 w-4 bg-muted rounded"></div>
            </CardHeader>
            <CardContent>
              <div className="h-8 bg-muted rounded w-16 mb-2"></div>
              <div className="h-3 bg-muted rounded w-32"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Equipamentos Ativos</CardTitle>
          <Truck className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.equipamentosAtivos}</div>
          <p className="text-xs text-muted-foreground mt-1">
            Operacionais no momento
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Funcionários</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.funcionariosPresentes}</div>
          <p className="text-xs text-muted-foreground mt-1">
            Cadastrados no sistema
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Obras Ativas</CardTitle>
          <TrendingUp className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.obrasAtivas}</div>
          <p className="text-xs text-muted-foreground mt-1">
            Em andamento
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium">Alertas Pendentes</CardTitle>
          <AlertTriangle className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-warning">{stats.alertasPendentes}</div>
          <p className="text-xs text-muted-foreground mt-1">
            Sem alertas no momento
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
