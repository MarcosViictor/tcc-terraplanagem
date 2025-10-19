"""
Serviço para processamento de arquivos CSV
"""
import csv
import io
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import (
    Obra, Fornecedor, Contrato, Equipamento, 
    Funcionario, Atividade, MotivoManutencao, Importacao
)


class CSVImportService:
    """Serviço para importação de dados via CSV"""
    
    def __init__(self, usuario, tipo_dados):
        self.usuario = usuario
        self.tipo_dados = tipo_dados
        self.erros = []
        self.sucessos = 0
        self.total = 0
    
    def processar_arquivo(self, arquivo):
        """Processa o arquivo CSV e retorna o resultado"""
        try:
            # Lê o arquivo CSV
            decoded_file = arquivo.read().decode('utf-8-sig')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            # Processa cada linha
            self.total = 0
            self.sucessos = 0
            self.erros = []
            
            for linha_num, row in enumerate(reader, start=2):
                self.total += 1
                try:
                    self._processar_linha(row, linha_num)
                    self.sucessos += 1
                except Exception as e:
                    self.erros.append({
                        'linha': linha_num,
                        'erro': str(e),
                        'dados': row
                    })
            
            # Determina o status
            if self.erros and self.sucessos == 0:
                status = 'erro'
            elif self.erros and self.sucessos > 0:
                status = 'parcial'
            else:
                status = 'sucesso'
            
            return {
                'status': status,
                'total': self.total,
                'sucessos': self.sucessos,
                'erros_count': len(self.erros),
                'erros': self.erros[:10],  # Limita a 10 primeiros erros
                'mensagem': self._gerar_mensagem(status)
            }
            
        except Exception as e:
            return {
                'status': 'erro',
                'total': 0,
                'sucessos': 0,
                'erros_count': 1,
                'erros': [{'erro': f'Erro ao ler arquivo: {str(e)}'}],
                'mensagem': f'Erro ao processar arquivo: {str(e)}'
            }
    
    def _processar_linha(self, row, linha_num):
        """Processa uma linha do CSV baseado no tipo de dados"""
        processadores = {
            'obras': self._processar_obra,
            'fornecedores': self._processar_fornecedor,
            'contratos': self._processar_contrato,
            'equipamentos': self._processar_equipamento,
            'funcionarios': self._processar_funcionario,
            'atividades': self._processar_atividade,
        }
        
        processador = processadores.get(self.tipo_dados)
        if not processador:
            raise ValueError(f"Tipo de dados '{self.tipo_dados}' não suportado")
        
        with transaction.atomic():
            processador(row)
    
    def _processar_obra(self, row):
        """Processa dados de obra"""
        Obra.objects.create(
            nome=row['nome'],
            codigo=row['codigo'],
            descricao=row.get('descricao', ''),
            data_inicio=self._parse_date(row['data_inicio']),
            data_fim_prevista=self._parse_date(row['data_fim_prevista']),
            endereco=row['endereco'],
            orcamento_total=self._parse_decimal(row['orcamento_total']),
            status=row.get('status', 'planejamento')
        )
    
    def _processar_fornecedor(self, row):
        """Processa dados de fornecedor"""
        Fornecedor.objects.create(
            razao_social=row['razao_social'],
            cnpj=row['cnpj'],
            contato=row['contato'],
            telefone=row['telefone'],
            email=row['email']
        )
    
    def _processar_contrato(self, row):
        """Processa dados de contrato"""
        obra = Obra.objects.get(codigo=row['obra_codigo'])
        fornecedor = Fornecedor.objects.get(cnpj=row['fornecedor_cnpj'])
        
        Contrato.objects.create(
            obra=obra,
            fornecedor=fornecedor,
            numero_contrato=row['numero_contrato'],
            valor_total=self._parse_decimal(row['valor_total']),
            data_inicio=self._parse_date(row['data_inicio']),
            data_fim=self._parse_date(row['data_fim']),
            observacoes=row.get('observacoes', '')
        )
    
    def _processar_equipamento(self, row):
        """Processa dados de equipamento"""
        contrato = Contrato.objects.get(numero_contrato=row['contrato_numero'])
        
        Equipamento.objects.create(
            contrato=contrato,
            codigo=row['codigo'],
            descricao=row['descricao'],
            tipo=row['tipo'],
            marca=row['marca'],
            modelo=row['modelo'],
            horimetro_inicial=int(row.get('horimetro_inicial', 0)),
            status=row.get('status', 'operacional')
        )
    
    def _processar_funcionario(self, row):
        """Processa dados de funcionário"""
        Funcionario.objects.create(
            nome=row['nome'],
            matricula=row['matricula'],
            funcao=row['funcao'],
            setor=row['setor'],
            salario_base=self._parse_decimal(row['salario_base']),
            ativo=row.get('ativo', 'true').lower() in ['true', '1', 'sim', 's']
        )
    
    def _processar_atividade(self, row):
        """Processa dados de atividade"""
        Atividade.objects.create(
            codigo=row['codigo'],
            descricao=row['descricao'],
            unidade_medida=row['unidade_medida'],
            preco_unitario=self._parse_decimal(row['preco_unitario']),
            categoria=row.get('categoria', 'terraplenagem'),
            ativa=row.get('ativa', 'true').lower() in ['true', '1', 'sim', 's']
        )
    
    def _parse_date(self, date_str):
        """Converte string para data"""
        if not date_str:
            raise ValueError("Data não pode ser vazia")
        
        # Tenta vários formatos
        formatos = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
        for formato in formatos:
            try:
                return datetime.strptime(date_str.strip(), formato).date()
            except ValueError:
                continue
        
        raise ValueError(f"Formato de data inválido: {date_str}. Use YYYY-MM-DD ou DD/MM/YYYY")
    
    def _parse_decimal(self, value_str):
        """Converte string para Decimal"""
        if not value_str:
            raise ValueError("Valor decimal não pode ser vazio")
        
        try:
            # Remove espaços e substitui vírgula por ponto
            value_str = value_str.strip().replace(',', '.')
            return Decimal(value_str)
        except (InvalidOperation, ValueError):
            raise ValueError(f"Valor decimal inválido: {value_str}")
    
    def _gerar_mensagem(self, status):
        """Gera mensagem de resultado"""
        if status == 'sucesso':
            return f"Importação concluída com sucesso! {self.sucessos} registros importados."
        elif status == 'parcial':
            return f"Importação parcial: {self.sucessos} sucessos, {len(self.erros)} erros."
        else:
            return f"Erro na importação: {len(self.erros)} erros encontrados."


def gerar_template_csv(tipo_dados):
    """Gera um template CSV para o tipo de dados especificado"""
    templates = {
        'obras': [
            'nome,codigo,descricao,data_inicio,data_fim_prevista,endereco,orcamento_total,status',
            'Obra Exemplo,OBR-001,Descrição da obra,2025-01-01,2025-12-31,Rua Exemplo 123,1000000.00,planejamento'
        ],
        'fornecedores': [
            'razao_social,cnpj,contato,telefone,email',
            'Fornecedor Exemplo LTDA,12.345.678/0001-90,João Silva,(11) 98765-4321,contato@exemplo.com'
        ],
        'contratos': [
            'obra_codigo,fornecedor_cnpj,numero_contrato,valor_total,data_inicio,data_fim,observacoes',
            'OBR-001,12.345.678/0001-90,CTR-001,500000.00,2025-01-01,2025-12-31,Observações do contrato'
        ],
        'equipamentos': [
            'contrato_numero,codigo,descricao,tipo,marca,modelo,horimetro_inicial,status',
            'CTR-001,EQ-001,Escavadeira Hidráulica,Escavadeira,Caterpillar,320D,1000,operacional'
        ],
        'funcionarios': [
            'nome,matricula,funcao,setor,salario_base,ativo',
            'João da Silva,MAT-001,Operador,Operação,5000.00,true'
        ],
        'atividades': [
            'codigo,descricao,unidade_medida,preco_unitario,categoria,ativa',
            'AT-001,Escavação de material 1ª categoria,m³,25.50,terraplenagem,true'
        ]
    }
    
    return templates.get(tipo_dados, [])
