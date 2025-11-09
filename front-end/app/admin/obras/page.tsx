'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Plus, Search, Edit, Trash2, Eye } from 'lucide-react'
import { obrasAPI } from '@/lib/api'
import { Obra } from '@/types'
import Link from 'next/link'

const statusMap: Record<string, { label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline' }> = {
  'planejamento': { label: 'Planejamento', variant: 'secondary' },
  'em_andamento': { label: 'Em Andamento', variant: 'default' },
  'paralisada': { label: 'Paralisada', variant: 'destructive' },
  'concluida': { label: 'Concluída', variant: 'outline' },
  'cancelada': { label: 'Cancelada', variant: 'destructive' },
}

export default function ObrasPage() {
  const [obras, setObras] = useState<Obra[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchObras()
  }, [])

  async function fetchObras() {
    try {
      const data = await obrasAPI.list()
      setObras(data)
    } catch (error) {
      console.error('Erro ao buscar obras:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredObras = obras.filter(obra =>
    obra.nome?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    obra.codigo?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    obra.endereco?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Obras</h1>
              <p className="text-sm text-muted-foreground">Gerenciamento de obras cadastradas</p>
            </div>
            <div className="flex gap-2">
              <Link href="/admin/dashboard">
                <Button variant="outline">Voltar ao Dashboard</Button>
              </Link>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Nova Obra
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
                <CardTitle>Lista de Obras</CardTitle>
                <CardDescription>
                  {filteredObras.length} obra(s) encontrada(s)
                </CardDescription>
              </div>
              <div className="w-72">
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Buscar obras..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-8"
                  />
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
                <p className="mt-2 text-sm text-muted-foreground">Carregando obras...</p>
              </div>
            ) : filteredObras.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-muted-foreground">Nenhuma obra encontrada.</p>
                <Button className="mt-4" variant="outline">
                  <Plus className="h-4 w-4 mr-2" />
                  Cadastrar Primeira Obra
                </Button>
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Código</TableHead>
                    <TableHead>Nome</TableHead>
                    <TableHead>Endereço</TableHead>
                    <TableHead>Data Início</TableHead>
                    <TableHead>Data Fim</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Orçamento</TableHead>
                    <TableHead className="text-right">Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredObras.map((obra) => (
                    <TableRow key={obra.id}>
                      <TableCell className="font-medium">{obra.codigo}</TableCell>
                      <TableCell>{obra.nome}</TableCell>
                      <TableCell className="max-w-xs truncate">{obra.endereco}</TableCell>
                      <TableCell>{new Date(obra.data_inicio).toLocaleDateString('pt-BR')}</TableCell>
                      <TableCell>{new Date(obra.data_fim_prevista).toLocaleDateString('pt-BR')}</TableCell>
                      <TableCell>
                        <Badge variant={statusMap[obra.status]?.variant || 'default'}>
                          {statusMap[obra.status]?.label || obra.status}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {new Intl.NumberFormat('pt-BR', {
                          style: 'currency',
                          currency: 'BRL'
                        }).format(Number(obra.orcamento_total))}
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
