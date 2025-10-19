#!/usr/bin/env python
"""
Script de teste automatizado para o Sistema de Terraplanagem
Executa uma bateria completa de testes para validar o sistema
"""

import requests
import sys
import json
from pathlib import Path

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

class TerraplagemTester:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.token = None
        self.tests_passed = 0
        self.tests_failed = 0
        
    def test_server_running(self):
        """Testa se o servidor está rodando"""
        print_info("Testando se o servidor está rodando...")
        try:
            response = requests.get(f"{self.base_url}/admin/", timeout=5)
            if response.status_code in [200, 302]:
                print_success("Servidor está rodando")
                self.tests_passed += 1
                return True
            else:
                print_error(f"Servidor respondeu com status {response.status_code}")
                self.tests_failed += 1
                return False
        except requests.exceptions.ConnectionError:
            print_error("Não foi possível conectar ao servidor")
            print_warning("Execute: python manage.py runserver")
            self.tests_failed += 1
            return False
        except Exception as e:
            print_error(f"Erro inesperado: {e}")
            self.tests_failed += 1
            return False
    
    def test_login(self, username, password):
        """Testa login e obtém token JWT"""
        print_info(f"Testando login com usuário '{username}'...")
        try:
            response = requests.post(
                f"{self.base_url}/api/accounts/token/",
                json={"username": username, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'access' in data:
                    self.token = data['access']
                    print_success("Login realizado com sucesso")
                    print_info(f"Token obtido: {self.token[:20]}...")
                    self.tests_passed += 1
                    return True
                else:
                    print_error("Resposta não contém token de acesso")
                    self.tests_failed += 1
                    return False
            else:
                print_error(f"Login falhou com status {response.status_code}")
                print_warning("Verifique se o usuário existe: python manage.py createsuperuser")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Erro ao fazer login: {e}")
            self.tests_failed += 1
            return False
    
    def test_api_endpoint(self, endpoint, method="GET", expected_status=200):
        """Testa um endpoint da API"""
        print_info(f"Testando {method} {endpoint}...")
        
        if not self.token:
            print_error("Token não disponível. Faça login primeiro.")
            self.tests_failed += 1
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            if method == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", headers=headers, timeout=10)
            else:
                print_error(f"Método {method} não implementado ainda")
                return False
            
            if response.status_code == expected_status:
                print_success(f"Endpoint {endpoint} respondeu corretamente")
                self.tests_passed += 1
                return response.json() if response.content else None
            else:
                print_error(f"Endpoint {endpoint} retornou status {response.status_code}")
                self.tests_failed += 1
                return False
        except Exception as e:
            print_error(f"Erro ao testar endpoint: {e}")
            self.tests_failed += 1
            return False
    
    def test_csv_import(self, tipo, arquivo_path):
        """Testa importação de CSV"""
        print_info(f"Testando importação de {tipo}...")
        
        if not self.token:
            print_error("Token não disponível. Faça login primeiro.")
            self.tests_failed += 1
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            with open(arquivo_path, 'rb') as f:
                files = {'arquivo': f}
                data = {'tipo_dados': tipo}
                response = requests.post(
                    f"{self.base_url}/api/terraplanagem/importacoes/upload/",
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'sucesso':
                    print_success(f"{tipo} importado: {result.get('sucessos')} registros")
                    self.tests_passed += 1
                    return True
                elif result.get('status') == 'parcial':
                    print_warning(f"{tipo} importado parcialmente: {result.get('sucessos')} sucessos, {result.get('erros_count')} erros")
                    self.tests_passed += 1
                    return True
                else:
                    print_error(f"Importação falhou: {result.get('mensagem')}")
                    if result.get('erros'):
                        for erro in result['erros'][:3]:
                            print_error(f"  Linha {erro.get('linha')}: {erro.get('erro')}")
                    self.tests_failed += 1
                    return False
            else:
                print_error(f"Importação retornou status {response.status_code}")
                self.tests_failed += 1
                return False
        except FileNotFoundError:
            print_error(f"Arquivo não encontrado: {arquivo_path}")
            self.tests_failed += 1
            return False
        except Exception as e:
            print_error(f"Erro ao importar CSV: {e}")
            self.tests_failed += 1
            return False
    
    def test_data_count(self, endpoint, expected_min=0):
        """Testa se há dados em um endpoint"""
        print_info(f"Verificando dados em {endpoint}...")
        
        data = self.test_api_endpoint(endpoint)
        if data and 'count' in data:
            count = data['count']
            if count >= expected_min:
                print_success(f"Encontrados {count} registros (esperado: >= {expected_min})")
                self.tests_passed += 1
                return True
            else:
                print_warning(f"Apenas {count} registros encontrados (esperado: >= {expected_min})")
                self.tests_failed += 1
                return False
        else:
            print_error("Não foi possível contar registros")
            self.tests_failed += 1
            return False
    
    def run_all_tests(self, username, password):
        """Executa todos os testes"""
        print_header("TESTE AUTOMATIZADO - SISTEMA DE TERRAPLANAGEM")
        
        # Teste 1: Servidor
        print_header("1. Testando Servidor")
        if not self.test_server_running():
            print_error("Servidor não está rodando. Abortando testes.")
            return False
        
        # Teste 2: Login
        print_header("2. Testando Autenticação")
        if not self.test_login(username, password):
            print_error("Login falhou. Abortando testes.")
            return False
        
        # Teste 3: Endpoints básicos
        print_header("3. Testando Endpoints da API")
        self.test_api_endpoint("/api/terraplanagem/importacoes/tipos-disponiveis/")
        self.test_api_endpoint("/api/terraplanagem/obras/")
        self.test_api_endpoint("/api/terraplanagem/fornecedores/")
        self.test_api_endpoint("/api/terraplanagem/equipamentos/")
        self.test_api_endpoint("/api/terraplanagem/funcionarios/")
        self.test_api_endpoint("/api/terraplanagem/atividades/")
        
        # Teste 4: Importação de CSVs
        print_header("4. Testando Importação de CSVs")
        base_path = Path(__file__).parent / "exemplos_csv"
        
        importacoes = [
            ("obras", "obras_exemplo.csv", 3),
            ("fornecedores", "fornecedores_exemplo.csv", 3),
            ("contratos", "contratos_exemplo.csv", 3),
            ("equipamentos", "equipamentos_exemplo.csv", 8),
            ("funcionarios", "funcionarios_exemplo.csv", 10),
            ("atividades", "atividades_exemplo.csv", 15),
        ]
        
        for tipo, arquivo, expected in importacoes:
            arquivo_path = base_path / arquivo
            if arquivo_path.exists():
                self.test_csv_import(tipo, arquivo_path)
            else:
                print_warning(f"Arquivo {arquivo} não encontrado, pulando...")
        
        # Teste 5: Verificar dados importados
        print_header("5. Verificando Dados Importados")
        self.test_data_count("/api/terraplanagem/obras/", 3)
        self.test_data_count("/api/terraplanagem/fornecedores/", 3)
        self.test_data_count("/api/terraplanagem/contratos/", 3)
        self.test_data_count("/api/terraplanagem/equipamentos/", 8)
        self.test_data_count("/api/terraplanagem/funcionarios/", 10)
        self.test_data_count("/api/terraplanagem/atividades/", 15)
        
        # Teste 6: Histórico de importações
        print_header("6. Verificando Histórico de Importações")
        self.test_api_endpoint("/api/terraplanagem/importacoes/")
        
        # Resumo
        print_header("RESUMO DOS TESTES")
        total = self.tests_passed + self.tests_failed
        print(f"Total de testes: {total}")
        print_success(f"Testes aprovados: {self.tests_passed}")
        if self.tests_failed > 0:
            print_error(f"Testes falhados: {self.tests_failed}")
        
        success_rate = (self.tests_passed / total * 100) if total > 0 else 0
        print(f"\nTaxa de sucesso: {success_rate:.1f}%")
        
        if success_rate == 100:
            print_success("\n🎉 TODOS OS TESTES PASSARAM! Sistema 100% funcional!")
            return True
        elif success_rate >= 80:
            print_warning("\n⚠️  Maioria dos testes passou, mas há alguns problemas.")
            return True
        else:
            print_error("\n❌ Muitos testes falharam. Verifique o sistema.")
            return False

def main():
    print(f"{Colors.BOLD}Sistema de Terraplanagem - Teste Automatizado{Colors.END}\n")
    
    # Solicitar credenciais
    username = input("Username: ").strip()
    if not username:
        username = "admin"
        print(f"Usando username padrão: {username}")
    
    import getpass
    password = getpass.getpass("Password: ")
    
    # Executar testes
    tester = TerraplagemTester()
    success = tester.run_all_tests(username, password)
    
    # Exit code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
