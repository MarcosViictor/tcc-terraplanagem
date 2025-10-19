#!/bin/bash

# Script de teste para importação de CSV
# Certifique-se de ter um token JWT válido

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Sistema de Terraplanagem - Teste de Importação CSV ===${NC}\n"

# Variáveis
BASE_URL="http://localhost:8001"
TOKEN=""

# Função para obter token
get_token() {
    echo -e "${BLUE}Digite seu username:${NC}"
    read USERNAME
    echo -e "${BLUE}Digite sua senha:${NC}"
    read -s PASSWORD
    
    echo "🔐 Obtendo token JWT..."
    RESPONSE=$(curl -s -X POST "$BASE_URL/api/accounts/token/" \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")
    
    TOKEN=$(echo $RESPONSE | grep -o '"access":"[^"]*' | cut -d'"' -f4)
    
    if [ -z "$TOKEN" ]; then
        echo -e "${RED}Erro ao obter token. Verifique suas credenciais.${NC}"
        echo "Resposta: $RESPONSE"
        exit 1
    fi
    
    echo -e "${GREEN}Token obtido com sucesso!${NC}\n"
}

# Função para importar CSV
import_csv() {
    local tipo=$1
    local arquivo=$2
    
    echo -e "${BLUE}Importando $tipo...${NC}"
    
    RESPONSE=$(curl -s -X POST "$BASE_URL/api/terraplanagem/importacoes/upload/" \
        -H "Authorization: Bearer $TOKEN" \
        -F "arquivo=@$arquivo" \
        -F "tipo_dados=$tipo")
    
    # Verifica se foi sucesso
    STATUS=$(echo $RESPONSE | grep -o '"status":"[^"]*' | cut -d'"' -f4)
    
    if [ "$STATUS" == "sucesso" ]; then
        SUCESSOS=$(echo $RESPONSE | grep -o '"sucessos":[0-9]*' | cut -d':' -f2)
        echo -e "${GREEN}✓ $tipo importado com sucesso! ($SUCESSOS registros)${NC}"
    elif [ "$STATUS" == "parcial" ]; then
        SUCESSOS=$(echo $RESPONSE | grep -o '"sucessos":[0-9]*' | cut -d':' -f2)
        ERROS=$(echo $RESPONSE | grep -o '"erros_count":[0-9]*' | cut -d':' -f2)
        echo -e "${RED}⚠ $tipo importado parcialmente. Sucessos: $SUCESSOS, Erros: $ERROS${NC}"
    else
        echo -e "${RED}✗ Erro ao importar $tipo${NC}"
        echo "Resposta: $RESPONSE"
    fi
    
    echo ""
}

# Função para listar dados
list_data() {
    local endpoint=$1
    local nome=$2
    
    echo -e "${BLUE}Listando $nome...${NC}"
    
    RESPONSE=$(curl -s "$BASE_URL/api/terraplanagem/$endpoint/" \
        -H "Authorization: Bearer $TOKEN")
    
    COUNT=$(echo $RESPONSE | grep -o '"count":[0-9]*' | cut -d':' -f2)
    
    if [ ! -z "$COUNT" ]; then
        echo -e "${GREEN}Total de $nome: $COUNT${NC}\n"
    else
        echo -e "${RED}Erro ao listar $nome${NC}\n"
    fi
}

# Menu principal
main() {
    get_token
    
    while true; do
        echo -e "${BLUE}=== Menu ===${NC}"
        echo "1. Importar todos os exemplos CSV"
        echo "2. Importar obras"
        echo "3. Importar fornecedores"
        echo "4. Importar contratos"
        echo "5. Importar equipamentos"
        echo "6. Importar funcionários"
        echo "7. Importar atividades"
        echo "8. Listar estatísticas"
        echo "9. Baixar template CSV"
        echo "0. Sair"
        echo ""
        echo -e "${BLUE}Escolha uma opção:${NC}"
        read OPTION
        
        case $OPTION in
            1)
                echo -e "\n${BLUE}=== Importando todos os arquivos CSV de exemplo ===${NC}\n"
                import_csv "obras" "../exemplos_csv/obras_exemplo.csv"
                import_csv "fornecedores" "../exemplos_csv/fornecedores_exemplo.csv"
                import_csv "contratos" "../exemplos_csv/contratos_exemplo.csv"
                import_csv "equipamentos" "../exemplos_csv/equipamentos_exemplo.csv"
                import_csv "funcionarios" "../exemplos_csv/funcionarios_exemplo.csv"
                import_csv "atividades" "../exemplos_csv/atividades_exemplo.csv"
                echo -e "${GREEN}=== Importação completa! ===${NC}\n"
                ;;
            2)
                import_csv "obras" "../exemplos_csv/obras_exemplo.csv"
                ;;
            3)
                import_csv "fornecedores" "../exemplos_csv/fornecedores_exemplo.csv"
                ;;
            4)
                import_csv "contratos" "../exemplos_csv/contratos_exemplo.csv"
                ;;
            5)
                import_csv "equipamentos" "../exemplos_csv/equipamentos_exemplo.csv"
                ;;
            6)
                import_csv "funcionarios" "../exemplos_csv/funcionarios_exemplo.csv"
                ;;
            7)
                import_csv "atividades" "../exemplos_csv/atividades_exemplo.csv"
                ;;
            8)
                echo -e "\n${BLUE}=== Estatísticas ===${NC}\n"
                list_data "obras" "obras"
                list_data "fornecedores" "fornecedores"
                list_data "contratos" "contratos"
                list_data "equipamentos" "equipamentos"
                list_data "funcionarios" "funcionários"
                list_data "atividades" "atividades"
                ;;
            9)
                echo -e "\n${BLUE}Tipos disponíveis: obras, fornecedores, contratos, equipamentos, funcionarios, atividades${NC}"
                echo -e "${BLUE}Digite o tipo:${NC}"
                read TIPO
                curl -O "$BASE_URL/api/terraplanagem/importacoes/template/$TIPO/" \
                    -H "Authorization: Bearer $TOKEN"
                echo -e "${GREEN}Template baixado!${NC}\n"
                ;;
            0)
                echo -e "${GREEN}Saindo...${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Opção inválida!${NC}\n"
                ;;
        esac
    done
}

# Executa o menu principal
main
