from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.db.models import Q

from .models import (
    Perfil, Obra, Fornecedor, Contrato, Equipamento, 
    Funcionario, Atividade, MotivoManutencao, Importacao
)
from .serializers import (
    PerfilSerializer, ObraSerializer, FornecedorSerializer,
    ContratoSerializer, EquipamentoSerializer, FuncionarioSerializer,
    AtividadeSerializer, MotivoManutencaoSerializer, 
    ImportacaoSerializer, ImportacaoListSerializer
)
from .csv_service import CSVImportService, gerar_template_csv


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    permission_classes = [IsAuthenticated]


class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsAuthenticated]


class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        ativo_filter = self.request.query_params.get('ativo', None)
        if ativo_filter is not None:
            queryset = queryset.filter(ativo=ativo_filter.lower() == 'true')
        return queryset


class AtividadeViewSet(viewsets.ModelViewSet):
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer
    permission_classes = [IsAuthenticated]


class MotivoManutencaoViewSet(viewsets.ModelViewSet):
    queryset = MotivoManutencao.objects.all()
    serializer_class = MotivoManutencaoSerializer
    permission_classes = [IsAuthenticated]


class ImportacaoViewSet(viewsets.ModelViewSet):
    queryset = Importacao.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ImportacaoListSerializer
        return ImportacaoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo_filter = self.request.query_params.get('tipo_dados', None)
        if tipo_filter:
            queryset = queryset.filter(tipo_dados=tipo_filter)
        return queryset.order_by('-data_importacao')
    
    @action(detail=False, methods=['post'], url_path='upload')
    def upload_csv(self, request):
        """
        Upload e processamento de arquivo CSV
        
        Parâmetros:
        - arquivo: arquivo CSV
        - tipo_dados: tipo de dados a importar (obras, equipamentos, etc)
        """
        arquivo = request.FILES.get('arquivo')
        tipo_dados = request.data.get('tipo_dados')
        
        if not arquivo:
            return Response(
                {'erro': 'Nenhum arquivo foi enviado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not tipo_dados:
            return Response(
                {'erro': 'Tipo de dados não especificado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Valida o tipo de dados
        tipos_validos = ['obras', 'equipamentos', 'funcionarios', 
                         'atividades', 'contratos', 'fornecedores']
        if tipo_dados not in tipos_validos:
            return Response(
                {'erro': f'Tipo de dados inválido. Use um dos seguintes: {", ".join(tipos_validos)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cria registro de importação
        importacao = Importacao.objects.create(
            usuario=request.user,
            tipo_dados=tipo_dados,
            nome_arquivo=arquivo.name,
            status='processando'
        )
        
        try:
            # Processa o arquivo
            service = CSVImportService(request.user, tipo_dados)
            resultado = service.processar_arquivo(arquivo)
            
            # Atualiza o registro de importação
            importacao.status = resultado['status']
            importacao.resultado_processamento = resultado
            importacao.save()
            
            return Response({
                'id': importacao.id,
                'status': resultado['status'],
                'mensagem': resultado['mensagem'],
                'total': resultado['total'],
                'sucessos': resultado['sucessos'],
                'erros_count': resultado['erros_count'],
                'erros': resultado['erros']
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            importacao.status = 'erro'
            importacao.resultado_processamento = {
                'erro': str(e)
            }
            importacao.save()
            
            return Response(
                {'erro': f'Erro ao processar arquivo: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='template/(?P<tipo_dados>[^/.]+)')
    def baixar_template(self, request, tipo_dados=None):
        """
        Baixa um template CSV para o tipo de dados especificado
        
        Exemplo: /api/importacoes/template/obras/
        """
        if not tipo_dados:
            return Response(
                {'erro': 'Tipo de dados não especificado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        template = gerar_template_csv(tipo_dados)
        
        if not template:
            return Response(
                {'erro': f'Template não disponível para tipo: {tipo_dados}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Cria resposta CSV
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="template_{tipo_dados}.csv"'
        response.write('\n'.join(template))
        
        return response
    
    @action(detail=False, methods=['get'], url_path='tipos-disponiveis')
    def tipos_disponiveis(self, request):
        """
        Retorna os tipos de dados disponíveis para importação
        """
        tipos = [
            {'value': 'obras', 'label': 'Obras'},
            {'value': 'fornecedores', 'label': 'Fornecedores'},
            {'value': 'contratos', 'label': 'Contratos'},
            {'value': 'equipamentos', 'label': 'Equipamentos'},
            {'value': 'funcionarios', 'label': 'Funcionários'},
            {'value': 'atividades', 'label': 'Atividades'},
        ]
        return Response(tipos)
