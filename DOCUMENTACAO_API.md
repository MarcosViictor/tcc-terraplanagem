# Sistema de Terraplanagem - API de Importação CSV

## Visão Geral

Este sistema permite que administradores importem dados via CSV e que operadores de campo preencham formulários que passam por validação do encarregado antes de serem consolidados com os dados importados.

## Estrutura do Projeto

### Models Implementados

O sistema possui os seguintes módulos:

1. **Perfis e Usuários**: Gestão de perfis e controle de acesso
2. **Obras e Contratos**: Gerenciamento de obras, fornecedores e contratos
3. **Equipamentos**: Controle de equipamentos, partes diárias e atividades
4. **Mão de Obra**: Gestão de funcionários, equipes e apropriações
5. **Atividades**: Cadastro de atividades e localizações
6. **Manutenção**: Controle de manutenções e paradas
7. **RDO e Medição**: Relatórios diários e boletins de medição
8. **Auditoria**: Logs de alterações e evidências fotográficas

## API de Importação CSV

### Endpoints Disponíveis

#### 1. Listar Tipos Disponíveis para Importação

```
GET /api/terraplanagem/importacoes/tipos-disponiveis/
```

**Resposta:**
```json
[
  {"value": "obras", "label": "Obras"},
  {"value": "fornecedores", "label": "Fornecedores"},
  {"value": "contratos", "label": "Contratos"},
  {"value": "equipamentos", "label": "Equipamentos"},
  {"value": "funcionarios", "label": "Funcionários"},
  {"value": "atividades", "label": "Atividades"}
]
```

#### 2. Baixar Template CSV

```
GET /api/terraplanagem/importacoes/template/{tipo_dados}/
```

**Exemplos:**
- `/api/terraplanagem/importacoes/template/obras/`
- `/api/terraplanagem/importacoes/template/equipamentos/`

**Resposta:** Arquivo CSV com cabeçalho e exemplo

#### 3. Upload de Arquivo CSV

```
POST /api/terraplanagem/importacoes/upload/
Content-Type: multipart/form-data
```

**Parâmetros:**
- `arquivo`: arquivo CSV
- `tipo_dados`: tipo de dados (obras, equipamentos, etc)

**Exemplo com cURL:**
```bash
curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer SEU_TOKEN_JWT" \
  -F "arquivo=@obras.csv" \
  -F "tipo_dados=obras"
```

**Resposta de Sucesso:**
```json
{
  "id": 1,
  "status": "sucesso",
  "mensagem": "Importação concluída com sucesso! 10 registros importados.",
  "total": 10,
  "sucessos": 10,
  "erros_count": 0,
  "erros": []
}
```

**Resposta com Erros Parciais:**
```json
{
  "id": 2,
  "status": "parcial",
  "mensagem": "Importação parcial: 8 sucessos, 2 erros.",
  "total": 10,
  "sucessos": 8,
  "erros_count": 2,
  "erros": [
    {
      "linha": 5,
      "erro": "Formato de data inválido: 01-13-2025",
      "dados": {...}
    }
  ]
}
```

#### 4. Listar Importações

```
GET /api/terraplanagem/importacoes/
```

**Filtros disponíveis:**
- `tipo_dados`: filtrar por tipo (ex: `?tipo_dados=obras`)

**Resposta:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "tipo_dados": "obras",
      "nome_arquivo": "obras_janeiro.csv",
      "status": "sucesso",
      "data_importacao": "2025-10-19T10:30:00Z",
      "usuario_nome": "admin"
    }
  ]
}
```

## Formatos CSV por Tipo

### 1. Obras

**Colunas obrigatórias:**
- nome
- codigo (único)
- data_inicio (YYYY-MM-DD ou DD/MM/YYYY)
- data_fim_prevista
- endereco
- orcamento_total (decimal, ex: 1000000.00)

**Colunas opcionais:**
- descricao
- status (planejamento, em_andamento, paralisada, concluida, cancelada)

**Exemplo:**
```csv
nome,codigo,descricao,data_inicio,data_fim_prevista,endereco,orcamento_total,status
Obra BR-101,OBR-001,Duplicação da rodovia,2025-01-01,2025-12-31,BR-101 KM 120,5000000.00,em_andamento
```

### 2. Fornecedores

**Colunas obrigatórias:**
- razao_social
- cnpj (único, formato: XX.XXX.XXX/XXXX-XX)
- contato
- telefone
- email

**Exemplo:**
```csv
razao_social,cnpj,contato,telefone,email
Locadora XYZ LTDA,12.345.678/0001-90,João Silva,(11) 98765-4321,contato@xyz.com
```

### 3. Contratos

**Colunas obrigatórias:**
- obra_codigo (deve existir)
- fornecedor_cnpj (deve existir)
- numero_contrato (único)
- valor_total
- data_inicio
- data_fim

**Colunas opcionais:**
- observacoes

**Exemplo:**
```csv
obra_codigo,fornecedor_cnpj,numero_contrato,valor_total,data_inicio,data_fim,observacoes
OBR-001,12.345.678/0001-90,CTR-001,500000.00,2025-01-01,2025-12-31,Contrato de locação de equipamentos
```

### 4. Equipamentos

**Colunas obrigatórias:**
- contrato_numero (deve existir)
- codigo (único)
- descricao
- tipo
- marca
- modelo

**Colunas opcionais:**
- horimetro_inicial (padrão: 0)
- status (operacional, manutencao, parado, inativo)

**Exemplo:**
```csv
contrato_numero,codigo,descricao,tipo,marca,modelo,horimetro_inicial,status
CTR-001,EQ-001,Escavadeira Hidráulica 20t,Escavadeira,Caterpillar,320D,1250,operacional
CTR-001,EQ-002,Motoniveladora,Motoniveladora,Caterpillar,140K,3500,operacional
```

### 5. Funcionários

**Colunas obrigatórias:**
- nome
- matricula (único)
- funcao
- setor
- salario_base

**Colunas opcionais:**
- ativo (true/false, sim/não, 1/0)

**Exemplo:**
```csv
nome,matricula,funcao,setor,salario_base,ativo
João da Silva,MAT-001,Operador de Escavadeira,Operação,5500.00,true
Maria Santos,MAT-002,Encarregada,Supervisão,8000.00,true
```

### 6. Atividades

**Colunas obrigatórias:**
- codigo (único)
- descricao
- unidade_medida (ex: m³, m², km, un)
- preco_unitario

**Colunas opcionais:**
- categoria (terraplenagem, drenagem, pavimentacao, obras_arte, sinalizacao, outros)
- ativa (true/false)

**Exemplo:**
```csv
codigo,descricao,unidade_medida,preco_unitario,categoria,ativa
AT-001,Escavação e carga de material 1ª categoria,m³,25.50,terraplenagem,true
AT-002,Transporte de material até 5km,m³,15.00,terraplenagem,true
```

## Outras APIs Disponíveis

### Obras

```
GET    /api/terraplanagem/obras/          # Listar obras
GET    /api/terraplanagem/obras/{id}/     # Detalhe da obra
POST   /api/terraplanagem/obras/          # Criar obra
PUT    /api/terraplanagem/obras/{id}/     # Atualizar obra
DELETE /api/terraplanagem/obras/{id}/     # Deletar obra
```

**Filtros:** `?status=em_andamento`

### Equipamentos

```
GET    /api/terraplanagem/equipamentos/          # Listar equipamentos
GET    /api/terraplanagem/equipamentos/{id}/     # Detalhe
POST   /api/terraplanagem/equipamentos/          # Criar
PUT    /api/terraplanagem/equipamentos/{id}/     # Atualizar
DELETE /api/terraplanagem/equipamentos/{id}/     # Deletar
```

**Filtros:** `?status=operacional`

### Funcionários

```
GET    /api/terraplanagem/funcionarios/          # Listar funcionários
GET    /api/terraplanagem/funcionarios/{id}/     # Detalhe
POST   /api/terraplanagem/funcionarios/          # Criar
PUT    /api/terraplanagem/funcionarios/{id}/     # Atualizar
DELETE /api/terraplanagem/funcionarios/{id}/     # Deletar
```

**Filtros:** `?ativo=true`

### Atividades

```
GET    /api/terraplanagem/atividades/          # Listar atividades
GET    /api/terraplanagem/atividades/{id}/     # Detalhe
POST   /api/terraplanagem/atividades/          # Criar
PUT    /api/terraplanagem/atividades/{id}/     # Atualizar
DELETE /api/terraplanagem/atividades/{id}/     # Deletar
```

## Autenticação

Todas as requisições requerem autenticação JWT. 

### Obter Token

```
POST /api/accounts/login/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Resposta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar Token

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Fluxo de Trabalho

1. **Admin importa dados base via CSV:**
   - Obras, fornecedores, contratos
   - Equipamentos e funcionários
   - Atividades

2. **Operadores preenchem formulários:**
   - Partes diárias de equipamentos
   - Apropriações de mão de obra
   - Com evidências fotográficas

3. **Encarregado valida:**
   - Revisa os dados enviados
   - Aprova ou rejeita
   - Solicita correções se necessário

4. **Sistema consolida:**
   - Dados aprovados são consolidados
   - Gera RDOs e boletins de medição
   - Alimenta dashboard

## Painel Admin

Acesse `/admin/` para gerenciar todos os dados através da interface administrativa do Django.

**Usuários:**
- Criar usuários com diferentes papéis
- Atribuir perfis e permissões

**Visualizar Importações:**
- Ver histórico de todas as importações
- Verificar status e erros
- Reprocessar se necessário

## Tratamento de Erros

O sistema valida:
- Formatos de data (YYYY-MM-DD ou DD/MM/YYYY)
- Valores decimais (aceita vírgula ou ponto)
- Códigos únicos (obras, equipamentos, etc)
- Relacionamentos (contrato deve existir, etc)
- Tipos enumerados (status, categoria, etc)

Erros são retornados com:
- Número da linha do CSV
- Mensagem de erro clara
- Dados que causaram o erro

## Exemplos Práticos

### 1. Importar Obras

```bash
# Baixar template
curl -O http://localhost:8000/api/terraplanagem/importacoes/template/obras/ \
  -H "Authorization: Bearer $TOKEN"

# Editar o CSV e fazer upload
curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@obras.csv" \
  -F "tipo_dados=obras"
```

### 2. Importar Equipamentos

```bash
# Baixar template
curl -O http://localhost:8000/api/terraplanagem/importacoes/template/equipamentos/ \
  -H "Authorization: Bearer $TOKEN"

# Fazer upload
curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@equipamentos.csv" \
  -F "tipo_dados=equipamentos"
```

### 3. Consultar Status

```bash
# Listar todas as importações
curl http://localhost:8000/api/terraplanagem/importacoes/ \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por tipo
curl http://localhost:8000/api/terraplanagem/importacoes/?tipo_dados=obras \
  -H "Authorization: Bearer $TOKEN"
```

## Próximos Passos

1. **Implementar formulários de campo:**
   - API para partes diárias
   - API para apropriações de mão de obra
   - Upload de evidências fotográficas

2. **Sistema de validação:**
   - Endpoints para encarregados validarem
   - Workflow de aprovação
   - Notificações

3. **Dashboard:**
   - Consolidação de dados
   - Visualizações e relatórios
   - Exportação de relatórios

4. **Mobile:**
   - App para operadores
   - Formulários offline
   - Sincronização
