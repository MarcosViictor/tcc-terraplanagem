# Guia Rápido de Início

## Configuração Inicial (5 minutos)

### 1. Ativar ambiente virtual e entrar no projeto

```bash
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate
cd core
```

### 2. Criar superusuário

```bash
python manage.py createsuperuser
```

Preencha:
- Username: admin
- Email: admin@exemplo.com
- Password: (sua senha)

### 3. Iniciar o servidor

```bash
python manage.py runserver
```

Acesse: http://localhost:8000/admin

## Testando a Importação CSV

### Opção 1: Via Script Interativo

```bash
cd /home/victor/projects/tcc-terraplanagem
./testar_importacao.sh
```

O script vai:
1. Pedir seu username e senha
2. Obter token JWT automaticamente
3. Mostrar menu com opções de importação

### Opção 2: Via cURL Manual

#### 1. Obter token

```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "sua_senha"}'
```

Salve o token retornado no campo "access".

#### 2. Importar obras

```bash
export TOKEN="seu_token_aqui"

curl -X POST http://localhost:8000/api/terraplanagem/importacoes/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "arquivo=@exemplos_csv/obras_exemplo.csv" \
  -F "tipo_dados=obras"
```

#### 3. Verificar obras importadas

```bash
curl http://localhost:8000/api/terraplanagem/obras/ \
  -H "Authorization: Bearer $TOKEN"
```

### Opção 3: Via Admin Django

1. Acesse http://localhost:8000/admin
2. Faça login com seu superusuário
3. Navegue pelos models criados
4. Adicione dados manualmente ou veja os importados via CSV

## Ordem Recomendada de Importação

Para evitar erros de relacionamento, importe nesta ordem:

1. **Obras** (obras_exemplo.csv)
2. **Fornecedores** (fornecedores_exemplo.csv)
3. **Contratos** (contratos_exemplo.csv) - depende de Obras e Fornecedores
4. **Equipamentos** (equipamentos_exemplo.csv) - depende de Contratos
5. **Funcionários** (funcionarios_exemplo.csv) - independente
6. **Atividades** (atividades_exemplo.csv) - independente

## Verificando os Dados

### Via API

```bash
# Listar obras
curl http://localhost:8000/api/terraplanagem/obras/ \
  -H "Authorization: Bearer $TOKEN"

# Listar equipamentos
curl http://localhost:8000/api/terraplanagem/equipamentos/ \
  -H "Authorization: Bearer $TOKEN"

# Filtrar por status
curl "http://localhost:8000/api/terraplanagem/equipamentos/?status=operacional" \
  -H "Authorization: Bearer $TOKEN"
```

### Via Admin

1. Acesse http://localhost:8000/admin
2. Navegue em "Terraplanagem" no menu lateral
3. Clique em qualquer model para ver os registros

### Ver Histórico de Importações

```bash
curl http://localhost:8000/api/terraplanagem/importacoes/ \
  -H "Authorization: Bearer $TOKEN"
```

Ou acesse via admin: http://localhost:8000/admin/terraplanagem/importacao/

## Endpoints Principais

### Autenticação
- `POST /api/accounts/login/` - Obter token JWT
- `POST /api/accounts/register/` - Registrar novo usuário

### Importação
- `GET /api/terraplanagem/importacoes/tipos-disponiveis/` - Tipos disponíveis
- `GET /api/terraplanagem/importacoes/template/{tipo}/` - Baixar template
- `POST /api/terraplanagem/importacoes/upload/` - Upload CSV
- `GET /api/terraplanagem/importacoes/` - Histórico

### Dados
- `GET/POST /api/terraplanagem/obras/`
- `GET/POST /api/terraplanagem/fornecedores/`
- `GET/POST /api/terraplanagem/contratos/`
- `GET/POST /api/terraplanagem/equipamentos/`
- `GET/POST /api/terraplanagem/funcionarios/`
- `GET/POST /api/terraplanagem/atividades/`

## Solução de Problemas

### Erro: "No module named 'django'"

```bash
# Certifique-se de estar na venv
source venv/bin/activate
pip install -r requirements.txt
```

### Erro: "no such table"

```bash
python manage.py migrate
```

### Erro ao importar CSV: "obra não encontrada"

Importe as obras primeiro! Siga a ordem recomendada acima.

### Token expirado

Os tokens JWT expiram após 1 hora. Faça login novamente para obter um novo token.

## Próximos Passos

1. **Explorar o Admin**: Veja todos os models criados
2. **Testar API**: Use Postman ou Insomnia para testar os endpoints
3. **Importar mais dados**: Crie seus próprios CSVs baseados nos exemplos
4. **Desenvolver frontend**: Conecte um frontend React/Vue aos endpoints

## Recursos Úteis

- Documentação completa: [DOCUMENTACAO_API.md](./DOCUMENTACAO_API.md)
- Exemplos de CSV: pasta `exemplos_csv/`
- Script de teste: `testar_importacao.sh`
- Admin Django: http://localhost:8000/admin
- API Root: http://localhost:8000/api/terraplanagem/

## Dicas

1. **Use o script de teste** para importar todos os exemplos de uma vez
2. **Explore o admin Django** para entender a estrutura dos dados
3. **Baixe os templates CSV** para entender o formato esperado
4. **Leia os erros** retornados pela API - eles são detalhados e úteis
5. **Verifique o histórico de importações** para debug

## Comandos Úteis

```bash
# Resetar banco de dados (CUIDADO!)
python manage.py flush

# Criar novo superusuário
python manage.py createsuperuser

# Ver todas as URLs disponíveis
python manage.py show_urls  # requer django-extensions

# Abrir shell Django
python manage.py shell

# Ver migrações pendentes
python manage.py showmigrations
```

## Contato

Para dúvidas, abra uma issue no GitHub ou consulte a documentação completa.
