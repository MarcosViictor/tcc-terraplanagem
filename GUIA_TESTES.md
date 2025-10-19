# 🧪 Guia Completo de Testes - Sistema de Terraplanagem

## 📋 Pré-requisitos

Certifique-se de que:
- ✅ Você está na pasta do projeto
- ✅ A venv está ativada
- ✅ O servidor Django está rodando

---

## 🚀 Método 1: Teste Rápido (5 minutos)

### Passo 1: Preparar o ambiente

```bash
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
cd core
```

### Passo 2: Criar superusuário (se ainda não criou)

```bash
python manage.py createsuperuser
```

Preencha:
- **Username:** admin
- **Email:** admin@teste.com
- **Password:** admin123 (use algo simples para teste)

### Passo 3: Aplicar migrations (se ainda não aplicou)

```bash
python manage.py migrate
```

### Passo 4: Iniciar o servidor

```bash
python manage.py runserver
```

Deixe o servidor rodando e **abra um novo terminal** para os próximos passos.

---

## 🌐 Método 2: Testar via Admin (Mais Fácil)

### 1. Acessar o Admin

Abra o navegador e acesse:
```
http://localhost:8000/admin
```

**Login:**
- Username: admin
- Password: (a senha que você criou)

### 2. Verificar Models Criados

No painel admin, você deve ver:

**ACCOUNTS**
- Users

**TERRAPLANAGEM**
- Atividades
- Apropriações de Mão de Obra
- Atividades de Equipamentos
- Atividades em Localizações
- Boletins de Medição
- Contratos
- Critérios de Medição
- Equipes
- Equipamentos
- Evidências Fotográficas
- Fornecedores
- Funcionários
- Importações
- Itens de Medição
- Localizações
- Logs de Alterações
- Manutenções
- Membros de Equipe
- Motivos de Manutenção
- Obras
- Paradas de Equipamento
- Partes Diárias
- Perfis
- RDO Atividades
- RDOs

### 3. Criar Dados Manualmente (Teste Básico)

#### 3.1. Criar uma Obra
1. Clique em "Obras" → "Adicionar Obra"
2. Preencha:
   - **Nome:** Teste Obra 1
   - **Código:** OBR-TEST-001
   - **Data início:** 2025-01-01
   - **Data fim prevista:** 2025-12-31
   - **Endereço:** Rua Teste, 123
   - **Orçamento total:** 1000000.00
   - **Status:** Em andamento
3. Clique em "Salvar"

#### 3.2. Criar um Fornecedor
1. Clique em "Fornecedores" → "Adicionar Fornecedor"
2. Preencha:
   - **Razão social:** Empresa Teste LTDA
   - **CNPJ:** 12.345.678/0001-90
   - **Contato:** João Silva
   - **Telefone:** (11) 98765-4321
   - **Email:** teste@empresa.com
3. Clique em "Salvar"

#### 3.3. Criar uma Atividade
1. Clique em "Atividades" → "Adicionar Atividade"
2. Preencha:
   - **Código:** AT-TEST-001
   - **Descrição:** Escavação de teste
   - **Unidade medida:** m³
   - **Preço unitário:** 25.50
   - **Categoria:** Terraplenagem
   - **Ativa:** ✓
3. Clique em "Salvar"

Se conseguir criar esses 3 registros, **o sistema está funcionando!** ✅

---

## 📁 Método 3: Testar Importação CSV (Recomendado)

### Opção A: Via Script Interativo

Em um **novo terminal**:

```bash
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
./testar_importacao.sh
```

O script vai:
1. Pedir seu username: `admin`
2. Pedir sua senha: (a senha que você criou)
3. Mostrar menu com opções

**Escolha opção 1** para importar todos os exemplos.

### Opção B: Via cURL Manual

#### 1. Obter Token JWT

```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Resposta esperada:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Copie o valor do campo `access` e salve em uma variável:

```bash
export TOKEN="cole_o_token_aqui"
```

#### 2. Testar Listagem de Tipos Disponíveis

```bash
curl http://localhost:8000/api/terraplanagem/importacoes/tipos-disponiveis/ \
  -H "Authorization: Bearer $TOKEN"
```

**Resposta esperada:**
```json
[
  {"value": "obras", "label": "Obras"},
  {"value": "fornecedores", "label": "Fornecedores"},
  ...
]
```

#### 3. Baixar Template CSV

```bash
curl -o template_obras.csv \
  http://localhost:8000/api/terraplanagem/importacoes/template/obras/ \
  -H "Authorization: Bearer $TOKEN"

cat template_obras.csv
```

#### 4. Importar Obras de Exemplo

```bash
cd /home/victor/projects/tcc-terraplanagem

curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@exemplos_csv/obras_exemplo.csv" \
  -F "tipo_dados=obras"
```

**Resposta esperada (sucesso):**
```json
{
  "id": 1,
  "status": "sucesso",
  "mensagem": "Importação concluída com sucesso! 3 registros importados.",
  "total": 3,
  "sucessos": 3,
  "erros_count": 0,
  "erros": []
}
```

#### 5. Verificar Obras Importadas

```bash
curl http://localhost:8000/api/terraplanagem/obras/ \
  -H "Authorization: Bearer $TOKEN"
```

#### 6. Importar Todos os Exemplos

```bash
# Fornecedores
curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@exemplos_csv/fornecedores_exemplo.csv" \
  -F "tipo_dados=fornecedores"

# Contratos (depende de obras e fornecedores)
curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@exemplos_csv/contratos_exemplo.csv" \
  -F "tipo_dados=contratos"

# Equipamentos (depende de contratos)
curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@exemplos_csv/equipamentos_exemplo.csv" \
  -F "tipo_dados=equipamentos"

# Funcionários
curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@exemplos_csv/funcionarios_exemplo.csv" \
  -F "tipo_dados=funcionarios"

# Atividades
curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@exemplos_csv/atividades_exemplo.csv" \
  -F "tipo_dados=atividades"
```

#### 7. Ver Histórico de Importações

```bash
curl http://localhost:8000/api/terraplanagem/importacoes/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔍 Método 4: Verificar Dados Importados

### Via Admin

1. Acesse http://localhost:8000/admin
2. Clique em cada model para ver os registros:
   - **Obras:** Deve ter 3 obras
   - **Fornecedores:** Deve ter 3 fornecedores
   - **Contratos:** Deve ter 3 contratos
   - **Equipamentos:** Deve ter 8 equipamentos
   - **Funcionários:** Deve ter 10 funcionários
   - **Atividades:** Deve ter 15 atividades

### Via API

```bash
# Contar obras
curl http://localhost:8000/api/terraplanagem/obras/ \
  -H "Authorization: Bearer $TOKEN" | grep -o '"count":[0-9]*'

# Contar equipamentos
curl http://localhost:8000/api/terraplanagem/equipamentos/ \
  -H "Authorization: Bearer $TOKEN" | grep -o '"count":[0-9]*'

# Contar funcionários
curl http://localhost:8000/api/terraplanagem/funcionarios/ \
  -H "Authorization: Bearer $TOKEN" | grep -o '"count":[0-9]*'
```

---

## ✅ Checklist de Validação

### Testes Básicos
- [ ] Servidor inicia sem erros (`python manage.py runserver`)
- [ ] Admin acessível (http://localhost:8000/admin)
- [ ] Login funciona no admin
- [ ] Todos os 25+ models aparecem no admin
- [ ] Consegue criar uma obra manualmente
- [ ] Consegue criar um fornecedor manualmente

### Testes de API
- [ ] Login retorna token JWT
- [ ] Token funciona para acessar endpoints protegidos
- [ ] Lista tipos disponíveis para importação
- [ ] Baixa template CSV
- [ ] Lista de obras vazia inicialmente retorna corretamente

### Testes de Importação
- [ ] Importa obras com sucesso
- [ ] Importa fornecedores com sucesso
- [ ] Importa contratos (com relacionamentos)
- [ ] Importa equipamentos (com relacionamentos)
- [ ] Importa funcionários
- [ ] Importa atividades
- [ ] Dados aparecem no admin
- [ ] Dados aparecem via API

### Testes de Validação
- [ ] Tenta importar CSV com data inválida (deve dar erro)
- [ ] Tenta importar contrato sem obra existente (deve dar erro)
- [ ] Tenta importar equipamento sem contrato (deve dar erro)
- [ ] Verifica que erros são reportados com linha e mensagem

---

## 🐛 Solução de Problemas

### Problema: "ModuleNotFoundError: No module named 'django'"

**Solução:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problema: "no such table: terraplanagem_obra"

**Solução:**
```bash
python manage.py migrate
```

### Problema: "Unauthorized" ao acessar API

**Solução:**
- Verifique se o token está correto
- Token expira em 1 hora, faça login novamente
- Use `Authorization: Bearer TOKEN` (com espaço)

### Problema: Erro ao importar contrato

**Solução:**
- Importe obras e fornecedores primeiro
- Verifique se os códigos no CSV correspondem aos registros existentes

### Problema: "Permission denied" no script

**Solução:**
```bash
chmod +x testar_importacao.sh
```

---

## 📊 Resultados Esperados

Após importar todos os exemplos:

| Model | Quantidade Esperada |
|-------|---------------------|
| Obras | 3 |
| Fornecedores | 3 |
| Contratos | 3 |
| Equipamentos | 8 |
| Funcionários | 10 |
| Atividades | 15 |
| Importações | 6 (histórico) |

---

## 🎯 Teste Completo em 10 Comandos

```bash
# 1. Ativar ambiente
cd /home/victor/projects/tcc-terraplanagem && source venv/bin/activate && cd core

# 2. Criar superusuário (se não existe)
python manage.py createsuperuser --username admin --email admin@teste.com

# 3. Aplicar migrations
python manage.py migrate

# 4. Verificar erros
python manage.py check

# 5. Iniciar servidor (em um terminal)
python manage.py runserver

# EM OUTRO TERMINAL:
# 6. Ativar venv novamente
cd /home/victor/projects/tcc-terraplanagem && source venv/bin/activate

# 7. Testar importação
./testar_importacao.sh

# 8. Escolher opção 1 (importar tudo)

# 9. Escolher opção 8 (ver estatísticas)

# 10. Abrir admin no navegador
# http://localhost:8000/admin
```

---

## 📹 Fluxo de Teste Visual

### 1. Terminal com Servidor
```
Terminal 1:
$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 19, 2025 - 10:30:00
Django version 5.2.6, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 2. Terminal com Testes
```
Terminal 2:
$ ./testar_importacao.sh

=== Sistema de Terraplanagem - Teste de Importação CSV ===

Digite seu username: admin
Digite sua senha: ****

Obtendo token...
✓ Token obtido com sucesso!

=== Menu ===
1. Importar todos os exemplos CSV
...
Escolha uma opção: 1

Importando obras...
✓ obras importado com sucesso! (3 registros)

Importando fornecedores...
✓ fornecedores importado com sucesso! (3 registros)
...
```

### 3. Browser com Admin
```
http://localhost:8000/admin

[Página de login]
Username: admin
Password: ****

[Dashboard Admin]
TERRAPLANAGEM
├── Obras (3)
├── Fornecedores (3)
├── Contratos (3)
├── Equipamentos (8)
├── Funcionários (10)
└── Atividades (15)
```

---

## 🎉 Validação Final

Se você conseguiu:
1. ✅ Fazer login no admin
2. ✅ Ver todos os models
3. ✅ Importar todos os CSVs com sucesso
4. ✅ Ver os dados no admin
5. ✅ Acessar via API

**Parabéns! O sistema está 100% funcional!** 🚀

---

## 📞 Próximos Passos Após Validação

1. **Explorar o Admin:** Navegue pelos dados, edite, crie novos
2. **Testar Filtros:** Use os filtros na API (`?status=operacional`)
3. **Criar seus CSVs:** Baseie-se nos exemplos para criar seus próprios dados
4. **Desenvolver Frontend:** Conecte um frontend aos endpoints
5. **Implementar Funcionalidades:** Partes diárias, validações, etc.

---

**Dúvidas?** Consulte:
- README.md
- DOCUMENTACAO_API.md
- GUIA_RAPIDO.md
