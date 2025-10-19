# Estrutura do Projeto - Sistema de Terraplanagem

## 📁 Organização Final

O projeto está organizado em **2 apps Django principais**:

### 1. **accounts/** - Autenticação e Usuários
Responsável por:
- ✅ Autenticação JWT
- ✅ Modelo de Usuário customizado (User)
- ✅ Login e registro
- ✅ Controle de papéis (admin, encarregado, operador, mecânico, gestor)
- ✅ Relacionamento com Perfil

**Arquivos principais:**
```
accounts/
├── models.py          # Model User (AbstractUser customizado)
├── views.py           # Login, registro, token
├── serializers.py     # Serializers de autenticação
├── urls.py            # Rotas /api/accounts/
├── permissions.py     # Permissões customizadas
└── admin.py          # Config admin para User
```

**Endpoints:**
- `POST /api/accounts/login/` - Login com JWT
- `POST /api/accounts/register/` - Registro de usuário
- `POST /api/accounts/token/refresh/` - Renovar token

---

### 2. **terraplanagem/** - Sistema Principal
Responsável por **TODA a lógica de negócio**:

#### 📊 Models (25 ao total)

**Perfis e Usuários**
- `Perfil` - Perfis com permissões JSON

**Obras e Contratos**
- `Obra` - Cadastro de obras
- `Fornecedor` - Fornecedores de equipamentos
- `Contrato` - Contratos entre obras e fornecedores

**Equipamentos**
- `Equipamento` - Cadastro de equipamentos
- `ParteDiaria` - Registro diário de trabalho de equipamento
- `AtividadeEquipamento` - Atividades executadas

**Mão de Obra**
- `Funcionario` - Cadastro de funcionários
- `Equipe` - Equipes de trabalho
- `EquipeFuncionario` - Relacionamento equipe-funcionário
- `ApropriacaoMaoObra` - Apropriação de horas trabalhadas

**Atividades**
- `Atividade` - Cadastro de atividades (serviços)
- `Localizacao` - Localizações da obra (estaqueamento)
- `AtividadeLocalizacao` - Atividades em locais específicos

**Manutenção**
- `MotivoManutencao` - Motivos de parada
- `Manutencao` - Registro de manutenções
- `ParadaEquipamento` - Paradas de equipamento

**RDO e Medição**
- `RDO` - Relatório Diário de Obra
- `RDOAtividade` - Atividades do RDO
- `CriterioMedicao` - Critérios de medição
- `BoletimMedicao` - Boletim mensal de medição
- `ItemMedicao` - Itens do boletim

**Auditoria**
- `LogAlteracao` - Log de todas as alterações
- `EvidenciaFotografica` - Fotos de evidência
- `Importacao` - Histórico de importações CSV

**Arquivos principais:**
```
terraplanagem/
├── models.py          # Todos os 25 models
├── views.py           # ViewSets da API REST
├── serializers.py     # Serializers DRF
├── csv_service.py     # Serviço de importação CSV
├── urls.py            # Rotas /api/terraplanagem/
└── admin.py          # Config admin (25 models)
```

**Endpoints principais:**
```
/api/terraplanagem/
├── perfis/                    # CRUD de perfis
├── obras/                     # CRUD de obras
├── fornecedores/              # CRUD de fornecedores
├── contratos/                 # CRUD de contratos
├── equipamentos/              # CRUD de equipamentos
├── funcionarios/              # CRUD de funcionários
├── atividades/                # CRUD de atividades
├── motivos-manutencao/        # CRUD de motivos
└── importacoes/               # Sistema de importação
    ├── tipos-disponiveis/     # GET - Tipos de CSV
    ├── template/{tipo}/       # GET - Download template
    └── upload/                # POST - Upload CSV
```

---

## 🎯 Fluxo de Dados

### 1. **Admin importa dados base (CSV)**
```
Obras → Fornecedores → Contratos → Equipamentos
                                  ↓
                            Funcionários
                                  ↓
                             Atividades
```

### 2. **Operadores registram trabalho**
```
Operador → ParteDiaria → AtividadeEquipamento
Operador → ApropriacaoMaoObra
```

### 3. **Encarregado valida**
```
ParteDiaria [aberto] → [em_validacao] → [validado/rejeitado]
ApropriacaoMaoObra [aberto] → [em_validacao] → [validado/rejeitado]
```

### 4. **Sistema consolida**
```
Dados Validados → RDO → BoletimMedicao → Dashboard
```

---

## 🗂️ Estrutura de Diretórios

```
tcc-terraplanagem/
│
├── core/                          # Projeto Django principal
│   ├── accounts/                  # App de autenticação ✅
│   │   ├── migrations/
│   │   ├── models.py             # User customizado
│   │   ├── views.py              # Login/Register
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── terraplanagem/             # App principal ✅
│   │   ├── migrations/
│   │   ├── models.py             # 25 models
│   │   ├── views.py              # ViewSets API
│   │   ├── serializers.py        # Serializers
│   │   ├── csv_service.py        # Importação CSV
│   │   ├── urls.py
│   │   └── admin.py
│   │
│   ├── core/                      # Configurações Django
│   │   ├── settings.py           # Configurações
│   │   ├── urls.py               # URLs principais
│   │   └── wsgi.py
│   │
│   ├── db.sqlite3                # Banco de dados
│   └── manage.py                 # Comando Django
│
├── venv/                          # Virtual environment
│
├── exemplos_csv/                  # Arquivos CSV de exemplo
│   ├── obras_exemplo.csv
│   ├── fornecedores_exemplo.csv
│   ├── contratos_exemplo.csv
│   ├── equipamentos_exemplo.csv
│   ├── funcionarios_exemplo.csv
│   └── atividades_exemplo.csv
│
├── requirements.txt               # Dependências Python
├── README.md                      # Documentação principal
├── DOCUMENTACAO_API.md            # Docs da API
├── GUIA_RAPIDO.md                # Guia de início
├── ESTRUTURA_PROJETO.md          # Este arquivo
├── testar_importacao.sh          # Script de teste
└── .gitignore
```

---

## 🔐 Modelo de Segurança

### Autenticação
- **JWT (JSON Web Tokens)** via djangorestframework-simplejwt
- Tokens de acesso: 1 hora de validade
- Tokens de refresh: 1 dia de validade

### Autorização
- **Perfis personalizados** com permissões em JSON
- **Papéis predefinidos**:
  - `admin` - Acesso total
  - `encarregado` - Valida dados de campo
  - `operador` - Preenche formulários
  - `mecanico` - Registra manutenções
  - `gestor` - Visualiza relatórios

### Auditoria
- **LogAlteracao**: Registra todas as mudanças (CREATE, UPDATE, DELETE)
- **Importacao**: Histórico completo de importações
- **EvidenciaFotografica**: Fotos com geolocalização

---

## 📊 Relacionamentos Entre Models

```
User (accounts)
  ↓
Perfil (terraplanagem)

Obra
  ├─→ Contrato
  │     ├─→ Equipamento
  │     │     ├─→ ParteDiaria
  │     │     ├─→ Manutencao
  │     │     └─→ ParadaEquipamento
  │     └─→ CriterioMedicao
  ├─→ Equipe
  ├─→ Localizacao
  └─→ RDO

Fornecedor
  └─→ Contrato

Funcionario
  ├─→ EquipeFuncionario
  └─→ ApropriacaoMaoObra

Atividade
  ├─→ AtividadeEquipamento
  ├─→ ApropriacaoMaoObra
  ├─→ AtividadeLocalizacao
  └─→ RDOAtividade

MotivoManutencao
  ├─→ Manutencao
  └─→ ParadaEquipamento

Contrato
  └─→ BoletimMedicao
        └─→ ItemMedicao
```

---

## 🚀 Como Funciona na Prática

### Cenário 1: Admin importa equipamentos

1. Admin acessa `/api/terraplanagem/importacoes/template/equipamentos/`
2. Baixa o template CSV
3. Preenche com dados dos equipamentos
4. Faz upload em `/api/terraplanagem/importacoes/upload/`
5. Sistema valida e importa
6. Admin verifica em `/admin/terraplanagem/equipamento/`

### Cenário 2: Operador preenche parte diária

1. Operador faz login (`POST /api/accounts/login/`)
2. Lista equipamentos (`GET /api/terraplanagem/equipamentos/`)
3. Cria parte diária (`POST /api/terraplanagem/partes-diarias/`)
4. Adiciona atividades (`POST /api/terraplanagem/atividades-equipamento/`)
5. Anexa fotos (`POST /api/terraplanagem/evidencias/`)
6. Submete para validação

### Cenário 3: Encarregado valida

1. Encarregado vê partes diárias pendentes
2. Revisa dados e evidências
3. Aprova ou rejeita com observações
4. Sistema atualiza status
5. Dados aprovados vão para medição

---

## 📦 Dependências Principais

```python
Django==5.2.6                      # Framework web
djangorestframework==3.16.1        # API REST
djangorestframework-simplejwt==5.3.1  # JWT
pandas==2.2.3                      # Processamento CSV
Pillow==10.4.0                     # Imagens
```

---

## ✅ Checklist de Apps

- ❌ **myapp** - Removida (não era usada)
- ✅ **accounts** - Autenticação e usuários
- ✅ **terraplanagem** - Sistema completo de gestão

---

## 🎯 Próximos Passos Sugeridos

### Fase 1 - Backend (Completar)
- [ ] APIs para ParteDiaria
- [ ] APIs para ApropriacaoMaoObra
- [ ] Sistema de validação (workflow)
- [ ] Upload de evidências fotográficas
- [ ] Geração de RDO em PDF
- [ ] Geração de Boletim de Medição

### Fase 2 - Frontend
- [ ] Dashboard administrativo
- [ ] Formulários para operadores
- [ ] Painel do encarregado
- [ ] Relatórios e gráficos

### Fase 3 - Mobile
- [ ] App React Native / Flutter
- [ ] Modo offline
- [ ] Câmera integrada
- [ ] Geolocalização automática

### Fase 4 - Melhorias
- [ ] Notificações push
- [ ] Exportação Excel
- [ ] Integração com sistemas externos
- [ ] Backup automático

---

## 📞 Resumo

**2 apps Django:**
1. **accounts** - Autenticação (User + JWT)
2. **terraplanagem** - Todo o sistema de gestão (25 models)

**Tudo centralizado e organizado!** ✅
