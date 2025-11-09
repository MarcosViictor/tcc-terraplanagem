'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Plus, Search, Edit, Trash2, Eye } from 'lucide-react'
import { equipamentosAPI } from '@/lib/api'
import { Equipamento } from '@/types'
import Link from 'next/link'

const statusMap: Record<string, { label: string; variant: 'default' | 'secondary' | 'destructive' }> = {
  'operacional': { label: 'Operacional', variant: 'default' },
  'manutencao': { label: 'Manutenção', variant: 'secondary' },
  'parado': { label: 'Parado', variant: 'destructive' },
}

export default function EquipamentosPage() {
  const [equipamentos, setEquipamentos] = useState<Equipamento[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('todos')

  useEffect(() => {
    fetchEquipamentos()
  }, [])

  async function fetchEquipamentos() {
    try {
      const data = await equipamentosAPI.list()
      setEquipamentos(data)
    } catch (error) {
      console.error('Erro ao buscar equipamentos:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredEquipamentos = equipamentos.filter(equip => {
    const matchesSearch = 
      equip.codigo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      equip.tipo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      equip.modelo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      equip.placa?.toLowerCase().includes(searchTerm.toLowerCase())
    
    const matchesStatus = statusFilter === 'todos' || equip.status === statusFilter
    
    return matchesSearch && matchesStatus
  })

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Equipamentos</h1>
              <p className="text-sm text-muted-foreground">Gerenciamento de equipamentos</p>
            </div>
            <div className="flex gap-2">
              <Link href="/admin/dashboard">
                <Button variant="outline">Voltar ao Dashboard</Button>
              </Link>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Novo Equipamento
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Lista de Equipamentos</CardTitle>
                <CardDescription>
                  {filteredEquipamentos.length} equipamento(s) encontrado(s)
                </CardDescription>
              </div>
              <div className="flex gap-2">
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Filtrar por status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="todos">Todos os status</SelectItem>
                    <SelectItem value="operacional">Operacional</SelectItem>
                    <SelectItem value="manutencao">Manutenção</SelectItem>
                    <SelectItem value="parado">Parado</SelectItem>
                  </SelectContent>
                </Select>
                <div className="w-72">
                  <div className="relative">
                    <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Buscar equipamentos..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-8"
                    />
                  </div>
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
                <p className="mt-2 text-sm text-muted-foreground">Carregando equipamentos...</p>
              </div>
            ) : filteredEquipamentos.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-muted-foreground">Nenhum equipamento encontrado.</p>
                <Button className="mt-4" variant="outline">
                  <Plus className="h-4 w-4 mr-2" />
                  Cadastrar Primeiro Equipamento
                </Button>
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Código</TableHead>
                    <TableHead>Tipo</TableHead>
                    <TableHead>Modelo</TableHead>
                    <TableHead>Placa</TableHead>
                    <TableHead>Ano</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredEquipamentos.map((equipamento) => (
                    <TableRow key={equipamento.id}>
                      <TableCell className="font-medium">{equipamento.codigo}</TableCell>
                      <TableCell>{equipamento.tipo}</TableCell>
                      <TableCell>{equipamento.modelo || '-'}</TableCell>
                      <TableCell>{equipamento.placa || '-'}</TableCell>
                      <TableCell>{equipamento.ano_fabricacao || '-'}</TableCell>
                      <TableCell>
                        <Badge variant={statusMap[equipamento.status]?.variant || 'default'}>
                          {statusMap[equipamento.status]?.label || equipamento.status}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex justify-end gap-2">
                          <Button size="sm" variant="ghost">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button size="sm" variant="ghost">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button size="sm" variant="ghost">
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
