# 🧪 Como Testar o Sistema - INSTRUÇÕES RÁPIDAS

## 🚀 Teste Rápido (3 minutos)

### Passo 0: Preparar ambiente (apenas primeira vez)

```bash
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
cd core
```

**Instalar requests (se ainda não instalou):**
```bash
pip install requests
```

**Aplicar migrations (se ainda não aplicou):**
```bash
python manage.py migrate
```

**Criar superusuário (se ainda não criou):**
```bash
python manage.py createsuperuser
```

Dados sugeridos:
- Username: `admin`
- Email: `admin@teste.com`
- Password: `admin123`

### Passo 1: Iniciar servidor (Terminal 1)

```bash
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
cd core
python manage.py runserver
```

**Deixe rodando** e abra um NOVO terminal para continuar.

---

## ✅ Opção 1: Teste Automatizado (Recomendado)

### Em um NOVO terminal (Terminal 2):

```bash
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
python testar_sistema.py
```

Digite:
- Username: `admin`
- Password: (sua senha)

O script vai testar **TUDO automaticamente**:
- ✅ Servidor rodando
- ✅ Login funcionando
- ✅ Todos os endpoints da API
- ✅ Importação de 6 tipos de CSV
- ✅ Dados importados corretamente

**Resultado esperado:**
```
🎉 TODOS OS TESTES PASSARAM! Sistema 100% funcional!
```

---

## ✅ Opção 2: Teste via Admin (Simples)

### 1. Abrir navegador

```
http://localhost:8000/admin
```

### 2. Fazer login

- Username: `admin`
- Password: (sua senha)

### 3. Verificar models

Deve ver no menu lateral:
- **TERRAPLANAGEM** com ~25 models listados

### 4. Criar uma obra

1. Clique em "Obras" → "Adicionar Obra"
2. Preencha os campos
3. Clique em "Salvar"

Se funcionou, **está OK!** ✅

---

## ✅ Opção 3: Teste com Script Bash

```bash
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
./testar_importacao.sh
```

- Escolha opção `1` para importar tudo
- Escolha opção `8` para ver estatísticas

---

## 📊 Resultados Esperados

Após teste completo:

| Item | Quantidade |
|------|------------|
| Obras | 3 |
| Fornecedores | 3 |
| Contratos | 3 |
| Equipamentos | 8 |
| Funcionários | 10 |
| Atividades | 15 |

---

## 🐛 Problemas Comuns

### "ModuleNotFoundError: No module named 'requests'"
```bash
source venv/bin/activate
pip install requests
# ou
pip install -r requirements.txt
```

### "No module named 'django'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "no such table"
```bash
cd core
python manage.py migrate
```

### "Connection refused"
```bash
# Verifique se o servidor está rodando em outro terminal
cd core
python manage.py runserver
```

### "Unauthorized" ou "Login failed"
```bash
# Crie um superusuário
cd core
python manage.py createsuperuser
```

### Token expirado
- Tokens expiram em 1 hora
- Faça login novamente no script

---

## 📚 Documentação Completa

- **GUIA_TESTES.md** - Guia detalhado de testes
- **DOCUMENTACAO_API.md** - Documentação da API
- **GUIA_RAPIDO.md** - Quick start guide

---

## ✅ Checklist Mínimo

- [ ] Servidor inicia sem erros
- [ ] Admin acessível
- [ ] Login funciona
- [ ] Models aparecem no admin
- [ ] Consegue importar CSVs
- [ ] Dados aparecem no admin

**Se todos passaram: Sistema OK!** 🎉

---

## 🎯 Teste Completo em 5 Comandos

```bash
# 1. Setup
cd /home/victor/projects/tcc-terraplanagem && source venv/bin/activate && cd core

# 2. Migrate (se necessário)
python manage.py migrate

# 3. Criar user (se necessário)
python manage.py createsuperuser

# 4. Iniciar servidor (deixar rodando)
python manage.py runserver

# 5. Em OUTRO terminal: testar
cd /home/victor/projects/tcc-terraplanagem && source venv/bin/activate && python testar_sistema.py
```

---

**Dúvidas?** Veja GUIA_TESTES.md para instruções detalhadas.
