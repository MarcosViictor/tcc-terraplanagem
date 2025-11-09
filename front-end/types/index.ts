// Tipos de usuário
export interface User {
  id: number
  username: string
  email: string
  papel: 'admin' | 'encarregado' | 'operador' | 'mecanico' | 'gestor'
  perfil?: number
  matricula?: string
  is_active: boolean
}

// Tokens de autenticação
export interface AuthTokens {
  access: string
  refresh: string
  user: User
}

// Obra
export interface Obra {
  id: number
  codigo: string
  nome: string
  descricao?: string
  endereco: string
  data_inicio: string
  data_fim_prevista: string
  data_fim_real?: string
  orcamento_total: string
  status: 'planejamento' | 'em_andamento' | 'paralisada' | 'concluida' | 'cancelada'
  ativo: boolean
  created_at: string
  updated_at: string
}

// Fornecedor
export interface Fornecedor {
  id: number
  cnpj: string
  razao_social: string
  nome_fantasia?: string
  telefone?: string
  email?: string
  endereco?: string
  ativo: boolean
}

// Contrato
export interface Contrato {
  id: number
  numero: string
  obra: number
  fornecedor: number
  data_inicio: string
  data_fim: string
  valor_total?: string
  ativo: boolean
}

// Equipamento
export interface Equipamento {
  id: number
  codigo: string
  tipo: string
  modelo?: string
  placa?: string
  ano_fabricacao?: number
  status: 'operacional' | 'manutencao' | 'parado'
  contrato: number
  ativo: boolean
  created_at: string
}

// Funcionário
export interface Funcionario {
  id: number
  matricula: string
  nome: string
  funcao: string
  cpf?: string
  telefone?: string
  data_admissao?: string
  ativo: boolean
}

// Atividade
export interface Atividade {
  id: number
  codigo: string
  descricao: string
  unidade: string
  tipo: 'equipamento' | 'mao_obra'
  ativo: boolean
}

// Importação
export interface Importacao {
  id: number
  arquivo: string
  tipo_dados: string
  status: 'sucesso' | 'erro' | 'parcial'
  usuario: number
  data_importacao: string
  total_linhas?: number
  linhas_sucesso?: number
  linhas_erro?: number
  mensagem_erro?: string
}

// Parte Diária
export interface ParteDiaria {
  id: number
  equipamento: number
  data: string
  horimetro_inicial?: string
  horimetro_final?: string
  observacoes?: string
  status: 'pendente' | 'aprovado' | 'rejeitado'
}

// Apropriação Mão de Obra
export interface ApropriacaoMaoObra {
  id: number
  equipe: number
  atividade: number
  data: string
  quantidade: string
  observacoes?: string
}

// Dashboard Stats
export interface DashboardStats {
  equipamentos_ativos: number
  mao_obra_total: number
  disponibilidade_mecanica: number
  alertas_pendentes: number
}
