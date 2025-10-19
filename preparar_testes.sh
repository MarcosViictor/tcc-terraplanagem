#!/bin/bash

# Script auxiliar para preparar ambiente de testes
# Execute este script ANTES de rodar os testes

echo "======================================"
echo "  Preparando Ambiente de Testes"
echo "======================================"
echo ""

# Ativar venv
echo "1. Ativando virtual environment..."
cd /home/victor/projects/tcc-terraplanagem
source venv/bin/activate

# Verificar se está na venv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Erro: Virtual environment não foi ativado"
    exit 1
fi
echo "✓ Virtual environment ativada"
echo ""

# Entrar na pasta core
cd core

# Verificar dependências
echo "2. Verificando dependências..."
pip install -q requests 2>/dev/null
echo "✓ Dependências OK"
echo ""

# Aplicar migrations
echo "3. Aplicando migrations..."
python manage.py migrate --no-input
echo "✓ Migrations aplicadas"
echo ""

# Verificar se existe superusuário
echo "4. Verificando superusuário..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Usuários:', User.objects.count())" 2>/dev/null

echo ""
echo "======================================"
echo "  Ambiente Preparado!"
echo "======================================"
echo ""
echo "Agora você pode:"
echo ""
echo "1. Iniciar o servidor (em um terminal):"
echo "   cd /home/victor/projects/tcc-terraplanagem"
echo "   source venv/bin/activate"
echo "   cd core"
echo "   python manage.py runserver"
echo ""
echo "2. Rodar os testes (em OUTRO terminal):"
echo "   cd /home/victor/projects/tcc-terraplanagem"
echo "   source venv/bin/activate"
echo "   python testar_sistema.py"
echo ""
echo "Se ainda não criou superusuário, execute:"
echo "   python manage.py createsuperuser"
echo ""
