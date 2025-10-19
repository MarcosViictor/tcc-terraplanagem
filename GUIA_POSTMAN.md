# 🚀 Guia de Testes com Postman

## 📋 Configuração Inicial

**URL Base:** `http://localhost:8001`

---

## 🔐 1. Autenticação - Obter Token JWT

### Request
- **Método:** `POST`
- **URL:** `http://localhost:8001/api/accounts/token/`
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```

### Response (Sucesso - 200 OK)
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 3,
    "username": "admin",
    "email": "admin@teste.com",
    "papel": ""
  }
}
```

**⚠️ IMPORTANTE:** Copie o valor de `"access"` - você vai usar em todas as outras requisições!

---

## 🔧 2. Configurar Authorization

Para todas as requisições abaixo:

1. Na aba **Authorization**
2. Selecione **Type:** `Bearer Token`
3. Cole o token obtido no campo **Token**

Ou adicione manualmente no **Headers**:
```
Authorization: Bearer seu_token_aqui
```

---

## 📊 3. Consultar Dados

### 3.1. Listar Obras
- **Método:** `GET`
- **URL:** `http://localhost:8001/api/terraplanagem/obras/`
- **Authorization:** Bearer Token

### 3.2. Listar Fornecedores
- **Método:** `GET`
- **URL:** `http://localhost:8001/api/terraplanagem/fornecedores/`
- **Authorization:** Bearer Token

### 3.3. Listar Contratos
- **Método:** `GET`
- **URL:** `http://localhost:8001/api/terraplanagem/contratos/`
- **Authorization:** Bearer Token

### 3.4. Listar Equipamentos
- **Método:** `GET`
- **URL:** `http://localhost:8001/api/terraplanagem/equipamentos/`
- **Authorization:** Bearer Token

**Com filtro:**
```
http://localhost:8001/api/terraplanagem/equipamentos/?status=operacional
http://localhost:8001/api/terraplanagem/equipamentos/?ativo=true
```

### 3.5. Listar Funcionários
- **Método:** `GET`
- **URL:** `http://localhost:8001/api/terraplanagem/funcionarios/`
- **Authorization:** Bearer Token

### 3.6. Listar Atividades
- **Método:** `GET`
- **URL:** `http://localhost:8001/api/terraplanagem/atividades/`
- **Authorization:** Bearer Token

---

## 📤 4. Importar CSV

### 4.1. Ver Tipos Disponíveis
- **Método:** `GET`
- **URL:** `http://localhost:8001/api/terraplanagem/importacoes/tipos-disponiveis/`
- **Authorization:** Bearer Token

**Response:**
```json
{
  "tipos_disponiveis": [
    "obras",
    "fornecedores",
    "contratos",
    "equipamentos",
    "funcionarios",
    "atividades"
  ]
}
```

### 4.2. Baixar Template CSV
- **Método:** `GET`
- **URL:** `http://localhost:8001/api/terraplanagem/importacoes/template/obras/`
- **Authorization:** Bearer Token

Substitua `obras` por: `fornecedores`, `contratos`, `equipamentos`, `funcionarios`, ou `atividades`

### 4.3. Upload de CSV
- **Método:** `POST`
- **URL:** `http://localhost:8001/api/terraplanagem/importacoes/upload/`
- **Authorization:** Bearer Token
- **Body:** `form-data`
  - **Key:** `arquivo` | **Type:** `File` | **Value:** selecione o arquivo CSV
  - **Key:** `tipo_dados` | **Type:** `Text` | **Value:** `obras` (ou outro tipo)

**Response (Sucesso):**
```json
{
  "status": "sucesso",
  "mensagem": "Importação concluída com sucesso",
  "arquivo": "obras_exemplo.csv",
  "tipo_dados": "obras",
  "sucessos": 3,
  "erros_count": 0,
  "erros": []
}
```

**Response (Erro):**
```json
{
  "status": "erro",
  "mensagem": "Erro ao processar arquivo",
  "erros": [
    {
      "linha": 2,
      "erro": "Campo 'nome' é obrigatório"
    }
  ]
}
```

### 4.4. Ver Histórico de Importações
- **Método:** `GET`
- **URL:** `http://localhost:8001/api/terraplanagem/importacoes/`
- **Authorization:** Bearer Token

---

## ➕ 5. Criar Registros (POST)

### 5.1. Criar Obra
- **Método:** `POST`
- **URL:** `http://localhost:8001/api/terraplanagem/obras/`
- **Authorization:** Bearer Token
- **Body (raw JSON):**
```json
{
  "codigo": "OBR-004",
  "nome": "Obra Nova Teste",
  "localizacao": "São Paulo - SP",
  "data_inicio": "2025-01-15",
  "data_fim_prevista": "2025-12-31",
  "ativo": true
}
```

### 5.2. Criar Fornecedor
- **Método:** `POST`
- **URL:** `http://localhost:8001/api/terraplanagem/fornecedores/`
- **Authorization:** Bearer Token
- **Body (raw JSON):**
```json
{
  "cnpj": "12.345.678/0001-90",
  "razao_social": "Fornecedor Teste LTDA",
  "nome_fantasia": "Fornecedor Teste",
  "telefone": "(11) 98765-4321",
  "email": "contato@fornecedor.com",
  "ativo": true
}
```

### 5.3. Criar Equipamento
- **Método:** `POST`
- **URL:** `http://localhost:8001/api/terraplanagem/equipamentos/`
- **Authorization:** Bearer Token
- **Body (raw JSON):**
```json
{
  "codigo": "EQ-009",
  "tipo": "Escavadeira",
  "modelo": "CAT 320",
  "placa": "ABC-1234",
  "ano_fabricacao": 2023,
  "status": "operacional",
  "contrato": 1,
  "ativo": true
}
```

**Nota:** O campo `contrato` deve ser o ID de um contrato existente.

---

## 🔄 6. Atualizar Registro (PUT/PATCH)

### PUT (Atualização completa)
- **Método:** `PUT`
- **URL:** `http://localhost:8001/api/terraplanagem/obras/1/`
- **Authorization:** Bearer Token
- **Body (raw JSON):** Todos os campos obrigatórios

### PATCH (Atualização parcial)
- **Método:** `PATCH`
- **URL:** `http://localhost:8001/api/terraplanagem/obras/1/`
- **Authorization:** Bearer Token
- **Body (raw JSON):**
```json
{
  "data_fim_prevista": "2026-06-30"
}
```

---

## 🗑️ 7. Deletar Registro (DELETE)

- **Método:** `DELETE`
- **URL:** `http://localhost:8001/api/terraplanagem/obras/1/`
- **Authorization:** Bearer Token

**Response:** `204 No Content` (sucesso)

---

## 🔄 8. Renovar Token

Após 1 hora, o token expira. Use o refresh token:

- **Método:** `POST`
- **URL:** `http://localhost:8001/api/accounts/token/refresh/`
- **Body (raw JSON):**
```json
{
  "refresh": "seu_refresh_token_aqui"
}
```

**Response:**
```json
{
  "access": "novo_token_de_acesso"
}
```

---

## 📦 9. Collection do Postman (Opcional)

Você pode criar uma **Collection** no Postman com todas essas requisições:

### Variáveis de Environment
Crie um Environment com:
- `base_url`: `http://localhost:8001`
- `token`: `{{token}}` (atualize após login)

### Exemplo de Request com variável:
```
{{base_url}}/api/terraplanagem/obras/
```

### Pre-request Script para Auto-refresh Token
```javascript
// Código JavaScript para auto-renovar token quando expirar
const token = pm.environment.get("token");
if (!token || isTokenExpired(token)) {
    // Renovar token
}
```

---

## 🎯 Fluxo Completo de Teste

### 1️⃣ Autenticar
```
POST /api/accounts/token/
```

### 2️⃣ Salvar token no Postman
Copie o `access` token e configure no Authorization

### 3️⃣ Testar endpoints
```
GET /api/terraplanagem/obras/
GET /api/terraplanagem/equipamentos/
```

### 4️⃣ Importar dados via CSV
```
POST /api/terraplanagem/importacoes/upload/
```

### 5️⃣ Verificar dados importados
```
GET /api/terraplanagem/obras/
```

### 6️⃣ Criar novo registro
```
POST /api/terraplanagem/obras/
```

### 7️⃣ Atualizar registro
```
PATCH /api/terraplanagem/obras/1/
```

### 8️⃣ Ver histórico
```
GET /api/terraplanagem/importacoes/
```

---

## 🐛 Troubleshooting

### Erro 401 Unauthorized
- ✅ Verifique se o token está correto
- ✅ Token pode ter expirado (válido por 1 hora)
- ✅ Use `Bearer` antes do token: `Bearer eyJ...`

### Erro 404 Not Found
- ✅ Verifique a URL (porta 8001, não 8000)
- ✅ Endpoint correto: `/api/accounts/token/` (não `/login/`)

### Erro 400 Bad Request
- ✅ Verifique o formato do JSON
- ✅ Campos obrigatórios estão presentes
- ✅ Tipos de dados corretos (strings, números, datas)

### Erro 500 Internal Server Error
- ✅ Verifique logs do servidor: `tail -f /tmp/django_server.log`
- ✅ Pode ser erro de relacionamento (FK inválida)

---

## 📚 Recursos

- **Arquivos CSV de exemplo:** `exemplos_csv/`
- **Documentação API:** [DOCUMENTACAO_API.md](./DOCUMENTACAO_API.md)
- **Início rápido:** [INICIO_RAPIDO.md](./INICIO_RAPIDO.md)

---

## 💡 Dicas Postman

1. **Organize em Folders:** Autenticação, Obras, Equipamentos, etc.
2. **Use Variáveis:** `{{base_url}}` e `{{token}}`
3. **Salve Examples:** Salve responses de sucesso/erro como exemplos
4. **Tests Tab:** Adicione testes automatizados
5. **Export Collection:** Compartilhe com sua equipe

### Exemplo de Test Script:
```javascript
// Validar response 200
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Salvar token automaticamente
if (pm.response.json().access) {
    pm.environment.set("token", pm.response.json().access);
}
```

---

**✅ Tudo pronto para testar no Postman!**

Se precisar de ajuda com algum endpoint específico, é só perguntar! 🚀
