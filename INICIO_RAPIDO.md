# 🚀 Início Rápido - Sistema de Terraplanagem

## ✅ Sistema já configurado e rodando!

**Porta do servidor:** http://localhost:8001  
**Admin Django:** http://localhost:8001/admin  
**Usuário:** admin  
**Senha:** admin123

---

## 📋 Endpoints Principais

### 🔐 Autenticação

#### Obter Token JWT
```bash
curl -X POST http://localhost:8001/api/accounts/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Resposta:**
```json
{
  "refresh": "eyJ...",
  "access": "eyJ...",
  "user": {"id": 3, "username": "admin", ...}
}
```

Copie o valor de `"access"` para usar nas próximas requisições.

#### Renovar Token (após 1 hora)
```bash
curl -X POST http://localhost:8001/api/accounts/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "seu_refresh_token_aqui"}'
```

---

### 📊 Consultar Dados

```bash
# Salve seu token em uma variável
export TOKEN="seu_access_token_aqui"

# Listar obras
curl http://localhost:8001/api/terraplanagem/obras/ \
  -H "Authorization: Bearer $TOKEN"

# Listar fornecedores
curl http://localhost:8001/api/terraplanagem/fornecedores/ \
  -H "Authorization: Bearer $TOKEN"

# Listar contratos
curl http://localhost:8001/api/terraplanagem/contratos/ \
  -H "Authorization: Bearer $TOKEN"

# Listar equipamentos
curl http://localhost:8001/api/terraplanagem/equipamentos/ \
  -H "Authorization: Bearer $TOKEN"

# Listar funcionários
curl http://localhost:8001/api/terraplanagem/funcionarios/ \
  -H "Authorization: Bearer $TOKEN"

# Listar atividades
curl http://localhost:8001/api/terraplanagem/atividades/ \
  -H "Authorization: Bearer $TOKEN"
```

---

### 📤 Importar CSV

#### 1. Verificar tipos disponíveis
```bash
curl http://localhost:8001/api/terraplanagem/importacoes/tipos-disponiveis/ \
  -H "Authorization: Bearer $TOKEN"
```

#### 2. Baixar template CSV
```bash
curl http://localhost:8001/api/terraplanagem/importacoes/template/obras/ \
  -H "Authorization: Bearer $TOKEN" \
  -o template_obras.csv
```

#### 3. Importar dados
```bash
curl -X POST http://localhost:8001/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@exemplos_csv/obras_exemplo.csv" \
  -F "tipo_dados=obras"
```

---

## 🎯 Teste Rápido (3 minutos)

### Opção 1: Script Automatizado

```bash
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
python testar_sistema.py
```

O script vai:
- ✅ Verificar se o servidor está rodando
- ✅ Fazer login e obter token
- ✅ Testar todos os endpoints
- ✅ Importar CSVs de exemplo
- ✅ Validar dados importados

### Opção 2: Script Interativo

```bash
cd /home/victor/projects/tcc-terraplanagem
./testar_importacao.sh
```

Escolha a opção **7** para importar todos os dados de uma vez.

---

## 📁 Ordem de Importação

**IMPORTANTE:** Siga esta ordem para evitar erros de relacionamento:

1. ✅ **Obras** (obras_exemplo.csv)
2. ✅ **Fornecedores** (fornecedores_exemplo.csv)
3. ✅ **Contratos** (contratos_exemplo.csv) - depende de Obras e Fornecedores
4. ✅ **Equipamentos** (equipamentos_exemplo.csv) - depende de Contratos
5. ✅ **Funcionários** (funcionarios_exemplo.csv) - independente
6. ✅ **Atividades** (atividades_exemplo.csv) - independente

---

## 🔧 Comandos Úteis

### Reiniciar o servidor
```bash
# Parar servidor atual
pkill -f "python manage.py runserver"

# Iniciar novamente
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
cd core
python manage.py runserver 8001
```

### Ver histórico de importações
```bash
curl http://localhost:8001/api/terraplanagem/importacoes/ \
  -H "Authorization: Bearer $TOKEN"
```

### Acessar Admin Django
1. Abra: http://localhost:8001/admin
2. Login: **admin** / **admin123**
3. Explore os dados importados

### Resetar banco de dados (CUIDADO!)
```bash
cd /home/victor/projects/tcc-terraplanagem/core
python manage.py flush
python manage.py createsuperuser
```

---

## 🐛 Solução de Problemas

### "Failed to connect to localhost"
```bash
# Verifique se o servidor está rodando
ps aux | grep "python manage.py runserver"

# Se não estiver, inicie:
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
cd core
nohup python manage.py runserver 8001 > /tmp/django_server.log 2>&1 &
```

### "401 Unauthorized"
Seu token expirou (válido por 1 hora). Faça login novamente para obter um novo token.

### "obra não encontrada" ao importar
Importe as **obras** primeiro, depois os outros dados que dependem delas.

### Ver logs do servidor
```bash
tail -f /tmp/django_server.log
```

---

## 📚 Recursos

- **Documentação completa:** [DOCUMENTACAO_API.md](./DOCUMENTACAO_API.md)
- **Guia de testes:** [COMO_TESTAR.md](./COMO_TESTAR.md)
- **Estrutura do projeto:** [ESTRUTURA_PROJETO.md](./ESTRUTURA_PROJETO.md)
- **Exemplos CSV:** pasta `exemplos_csv/`

---

## 🎉 Próximos Passos

1. ✅ **Servidor rodando** - http://localhost:8001
2. ✅ **Login funcionando** - `/api/accounts/token/`
3. ✅ **API respondendo** - Endpoints testados
4. 🔄 **Importar dados** - Use os scripts ou curl
5. 🔄 **Explorar Admin** - http://localhost:8001/admin
6. 🔄 **Testar formulários** - Próxima fase do projeto

---

**Status atual:** ✅ Backend 100% funcional  
**Servidor:** 🟢 Rodando na porta 8001  
**Banco de dados:** 🟢 Configurado e pronto  
**Autenticação:** 🟢 JWT funcionando  
