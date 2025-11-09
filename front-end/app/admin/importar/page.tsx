'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Upload, FileText, CheckCircle2, AlertCircle } from 'lucide-react'
import { importacoesAPI } from '@/lib/api'
import Link from 'next/link'
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

export default function ImportarPage() {
  const [tipoDados, setTipoDados] = useState('obras')
  const [arquivo, setArquivo] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [resultado, setResultado] = useState<any>(null)

  async function handleUpload() {
    if (!arquivo) return

    setUploading(true)
    setResultado(null)

    try {
      const result = await importacoesAPI.upload(arquivo, tipoDados)
      setResultado(result)
      setArquivo(null)
      // Reset file input
      const fileInput = document.getElementById('file-upload') as HTMLInputElement
      if (fileInput) fileInput.value = ''
    } catch (error: any) {
      setResultado({
        status: 'erro',
        mensagem: error.message || 'Erro ao fazer upload do arquivo'
      })
    } finally {
      setUploading(false)
    }
  }

  const tiposDisponiveis = [
    { value: 'obras', label: 'Obras' },
    { value: 'fornecedores', label: 'Fornecedores' },
    { value: 'contratos', label: 'Contratos' },
    { value: 'equipamentos', label: 'Equipamentos' },
    { value: 'funcionarios', label: 'Funcionários' },
    { value: 'atividades', label: 'Atividades' },
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold">Importar Dados</h1>
              <p className="text-sm text-muted-foreground">Upload de arquivos CSV</p>
            </div>
            <Link href="/admin/dashboard">
              <Button variant="outline">Voltar ao Dashboard</Button>
            </Link>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-6">
        <div className="grid gap-6 max-w-2xl mx-auto">
          {/* Card de Upload */}
          <Card>
            <CardHeader>
              <CardTitle>Selecione o arquivo para importar</CardTitle>
              <CardDescription>
                Faça upload de um arquivo CSV com os dados para importação
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Tipo de Dados */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Tipo de Dados</label>
                <Select value={tipoDados} onValueChange={setTipoDados}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {tiposDisponiveis.map((tipo) => (
                      <SelectItem key={tipo.value} value={tipo.value}>
                        {tipo.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Upload de Arquivo */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Arquivo CSV</label>
                <div className="border-2 border-dashed rounded-lg p-8 text-center">
                  <input
                    id="file-upload"
                    type="file"
                    accept=".csv"
                    onChange={(e) => setArquivo(e.target.files?.[0] || null)}
                    className="hidden"
                  />
                  <label
                    htmlFor="file-upload"
                    className="cursor-pointer flex flex-col items-center gap-2"
                  >
                    <Upload className="h-10 w-10 text-muted-foreground" />
                    <div>
                      <p className="font-medium">Clique para selecionar ou arraste o arquivo</p>
                      <p className="text-sm text-muted-foreground">Apenas arquivos .csv</p>
                    </div>
                  </label>
                </div>
                {arquivo && (
                  <div className="flex items-center gap-2 mt-2 p-2 bg-muted rounded">
                    <FileText className="h-4 w-4" />
                    <span className="text-sm">{arquivo.name}</span>
                  </div>
                )}
              </div>

              {/* Botão de Upload */}
              <Button
                onClick={handleUpload}
                disabled={!arquivo || uploading}
                className="w-full"
              >
                {uploading ? (
                  <>
                    <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-solid border-current border-r-transparent" />
                    Enviando...
                  </>
                ) : (
                  <>
                    <Upload className="h-4 w-4 mr-2" />
                    Importar Dados
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Resultado */}
          {resultado && (
            <Alert variant={resultado.status === 'sucesso' ? 'default' : 'destructive'}>
              {resultado.status === 'sucesso' ? (
                <CheckCircle2 className="h-4 w-4" />
              ) : (
                <AlertCircle className="h-4 w-4" />
              )}
              <AlertTitle>
                {resultado.status === 'sucesso' ? 'Importação Concluída!' : 'Erro na Importação'}
              </AlertTitle>
              <AlertDescription>
                <p>{resultado.mensagem}</p>
                {resultado.sucessos !== undefined && (
                  <p className="mt-2">Registros importados com sucesso: {resultado.sucessos}</p>
                )}
                {resultado.erros_count > 0 && (
                  <p className="mt-1 text-destructive">Erros encontrados: {resultado.erros_count}</p>
                )}
                {resultado.erros && resultado.erros.length > 0 && (
                  <div className="mt-2 space-y-1">
                    <p className="font-medium">Detalhes dos erros:</p>
                    {resultado.erros.slice(0, 5).map((erro: any, index: number) => (
                      <p key={index} className="text-sm">
                        Linha {erro.linha}: {erro.erro}
                      </p>
                    ))}
                    {resultado.erros.length > 5 && (
                      <p className="text-sm italic">... e mais {resultado.erros.length - 5} erros</p>
                    )}
                  </div>
                )}
              </AlertDescription>
            </Alert>
          )}

          {/* Instruções */}
          <Card>
            <CardHeader>
              <CardTitle>Instruções</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              <p>1. Selecione o tipo de dados que deseja importar</p>
              <p>2. Escolha o arquivo CSV correspondente</p>
              <p>3. Clique em "Importar Dados"</p>
              <p className="text-muted-foreground mt-4">
                <strong>Importante:</strong> O arquivo CSV deve seguir o formato esperado para cada tipo de dado.
                Você pode baixar templates de exemplo em cada página de listagem.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
