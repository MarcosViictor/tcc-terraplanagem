'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Plus, Search, Edit, Trash2, Eye } from 'lucide-react'
import { funcionariosAPI } from '@/lib/api'
import { Funcionario } from '@/types'
import Link from 'next/link'

export default function FuncionariosPage() {
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchFuncionarios()
  }, [])

  async function fetchFuncionarios() {
    try {
      const data = await funcionariosAPI.list()
      setFuncionarios(data)
    } catch (error) {
      console.error('Erro ao buscar funcionários:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredFuncionarios = funcionarios.filter(func =>
    func.nome?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    func.matricula?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    func.funcao?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    func.cpf?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Funcionários</h1>
              <p className="text-sm text-muted-foreground">Gerenciamento de funcionários</p>
            </div>
            <div className="flex gap-2">
              <Link href="/admin/dashboard">
                <Button variant="outline">Voltar ao Dashboard</Button>
              </Link>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Novo Funcionário
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
                <CardTitle>Lista de Funcionários</CardTitle>
                <CardDescription>
                  {filteredFuncionarios.length} funcionário(s) encontrado(s)
                </CardDescription>
              </div>
              <div className="w-72">
                <div className="relative">
                  <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Buscar funcionários..."
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
                <p className="mt-2 text-sm text-muted-foreground">Carregando funcionários...</p>
              </div>
            ) : filteredFuncionarios.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-muted-foreground">Nenhum funcionário encontrado.</p>
                <Button className="mt-4" variant="outline">
                  <Plus className="h-4 w-4 mr-2" />
                  Cadastrar Primeiro Funcionário
                </Button>
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Matrícula</TableHead>
                    <TableHead>Nome</TableHead>
                    <TableHead>Função</TableHead>
                    <TableHead>CPF</TableHead>
                    <TableHead>Telefone</TableHead>
                    <TableHead>Data Admissão</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredFuncionarios.map((funcionario) => (
                    <TableRow key={funcionario.id}>
                      <TableCell className="font-medium">{funcionario.matricula}</TableCell>
                      <TableCell>{funcionario.nome}</TableCell>
                      <TableCell>{funcionario.funcao}</TableCell>
                      <TableCell>{funcionario.cpf || '-'}</TableCell>
                      <TableCell>{funcionario.telefone || '-'}</TableCell>
                      <TableCell>
                        {funcionario.data_admissao 
                          ? new Date(funcionario.data_admissao).toLocaleDateString('pt-BR')
                          : '-'
                        }
                      </TableCell>
                      <TableCell>
                        <Badge variant={funcionario.ativo ? 'default' : 'secondary'}>
                          {funcionario.ativo ? 'Ativo' : 'Inativo'}
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
