from rest_framework import serializers
from .models import (
    Perfil, Obra, Fornecedor, Contrato, Equipamento, Funcionario, 
    Atividade, MotivoManutencao, Importacao
)


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'


class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = '__all__'


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'


class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'


class EquipamentoSerializer(serializers.ModelSerializer):
    contrato_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Equipamento
        fields = '__all__'
    
    def get_contrato_info(self, obj):
        return {
            'numero': obj.contrato.numero_contrato,
            'fornecedor': obj.contrato.fornecedor.razao_social
        }


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'


class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = '__all__'


class MotivoManutencaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivoManutencao
        fields = '__all__'


class ImportacaoSerializer(serializers.ModelSerializer):
    arquivo = serializers.FileField(write_only=True, required=False)
    
    class Meta:
        model = Importacao
        fields = ['id', 'tipo_dados', 'nome_arquivo', 'status', 
                  'resultado_processamento', 'data_importacao', 'arquivo']
        read_only_fields = ['status', 'resultado_processamento', 'data_importacao']
    
    def validate_arquivo(self, value):
        """Valida se o arquivo é um CSV"""
        if value:
            if not value.name.endswith('.csv'):
                raise serializers.ValidationError("Apenas arquivos CSV são permitidos.")
        return value


class ImportacaoListSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Importacao
        fields = ['id', 'tipo_dados', 'nome_arquivo', 'status', 
                  'resultado_processamento', 'data_importacao', 'usuario_nome']
