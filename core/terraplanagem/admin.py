from django.contrib import admin
from .models import (
    Perfil, Obra, Fornecedor, Contrato, Equipamento, ParteDiaria,
    AtividadeEquipamento, Funcionario, Equipe, EquipeFuncionario,
    ApropriacaoMaoObra, Atividade, Localizacao, AtividadeLocalizacao,
    MotivoManutencao, Manutencao, ParadaEquipamento, RDO, RDOAtividade,
    CriterioMedicao, BoletimMedicao, ItemMedicao, LogAlteracao,
    EvidenciaFotografica, Importacao
)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['nome', 'created_at']
    search_fields = ['nome']


@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'status', 'data_inicio', 'data_fim_prevista']
    list_filter = ['status', 'data_inicio']
    search_fields = ['codigo', 'nome', 'endereco']
    date_hierarchy = 'data_inicio'


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['razao_social', 'cnpj', 'email', 'telefone']
    search_fields = ['razao_social', 'cnpj', 'email']


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['numero_contrato', 'obra', 'fornecedor', 'valor_total', 'data_inicio', 'data_fim']
    list_filter = ['data_inicio', 'data_fim']
    search_fields = ['numero_contrato', 'obra__codigo', 'fornecedor__razao_social']
    date_hierarchy = 'data_inicio'


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'tipo', 'marca', 'modelo', 'status']
    list_filter = ['status', 'tipo']
    search_fields = ['codigo', 'descricao', 'marca', 'modelo']


@admin.register(ParteDiaria)
class ParteDiariaAdmin(admin.ModelAdmin):
    list_display = ['equipamento', 'data_servico', 'motorista', 'status', 'total_horas_trabalhadas']
    list_filter = ['status', 'data_servico']
    search_fields = ['equipamento__codigo', 'motorista__username']
    date_hierarchy = 'data_servico'


@admin.register(AtividadeEquipamento)
class AtividadeEquipamentoAdmin(admin.ModelAdmin):
    list_display = ['parte_diaria', 'atividade', 'hora_inicio', 'hora_fim', 'duracao_minutos', 'tipo']
    list_filter = ['tipo']
    search_fields = ['parte_diaria__equipamento__codigo', 'atividade__codigo']


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['matricula', 'nome', 'funcao', 'setor', 'ativo']
    list_filter = ['ativo', 'funcao', 'setor']
    search_fields = ['matricula', 'nome', 'funcao']


@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ['nome_equipe', 'obra', 'encarregado', 'data_formacao', 'ativa']
    list_filter = ['ativa', 'data_formacao']
    search_fields = ['nome_equipe', 'obra__codigo', 'encarregado__username']


@admin.register(EquipeFuncionario)
class EquipeFuncionarioAdmin(admin.ModelAdmin):
    list_display = ['equipe', 'funcionario', 'data_entrada', 'data_saida', 'ativo']
    list_filter = ['ativo', 'data_entrada']
    search_fields = ['equipe__nome_equipe', 'funcionario__nome']


@admin.register(ApropriacaoMaoObra)
class ApropriacaoMaoObraAdmin(admin.ModelAdmin):
    list_display = ['funcionario', 'atividade', 'data_servico', 'horas_trabalhadas', 'status']
    list_filter = ['status', 'data_servico']
    search_fields = ['funcionario__nome', 'atividade__codigo']
    date_hierarchy = 'data_servico'


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'unidade_medida', 'preco_unitario', 'categoria', 'ativa']
    list_filter = ['categoria', 'ativa']
    search_fields = ['codigo', 'descricao']


@admin.register(Localizacao)
class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ['obra', 'estaqueamento', 'latitude', 'longitude']
    search_fields = ['obra__codigo', 'estaqueamento']


@admin.register(AtividadeLocalizacao)
class AtividadeLocalizacaoAdmin(admin.ModelAdmin):
    list_display = ['atividade', 'localizacao', 'data_execucao', 'quantidade_executada', 'unidade']
    list_filter = ['data_execucao']
    search_fields = ['atividade__codigo', 'localizacao__estaqueamento']
    date_hierarchy = 'data_execucao'


@admin.register(MotivoManutencao)
class MotivoManutencaoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'descontavel', 'responsabilidade']
    list_filter = ['descontavel', 'responsabilidade']
    search_fields = ['codigo', 'descricao']


@admin.register(Manutencao)
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ['equipamento', 'motivo', 'data_saida', 'data_retorno', 'tipo_manutencao', 'status']
    list_filter = ['tipo_manutencao', 'status', 'data_saida']
    search_fields = ['equipamento__codigo', 'motivo__codigo']
    date_hierarchy = 'data_saida'


@admin.register(ParadaEquipamento)
class ParadaEquipamentoAdmin(admin.ModelAdmin):
    list_display = ['equipamento', 'motivo', 'data_inicio', 'data_fim', 'duracao_minutos']
    list_filter = ['data_inicio']
    search_fields = ['equipamento__codigo', 'motivo__codigo']
    date_hierarchy = 'data_inicio'


@admin.register(RDO)
class RDOAdmin(admin.ModelAdmin):
    list_display = ['obra', 'data_servico', 'administrador', 'status', 'data_finalizacao']
    list_filter = ['status', 'data_servico']
    search_fields = ['obra__codigo', 'administrador__username']
    date_hierarchy = 'data_servico'


@admin.register(RDOAtividade)
class RDOAtividadeAdmin(admin.ModelAdmin):
    list_display = ['rdo', 'atividade', 'quantidade_executada', 'unidade', 'total_funcionarios']
    search_fields = ['rdo__obra__codigo', 'atividade__codigo']


@admin.register(CriterioMedicao)
class CriterioMedicaoAdmin(admin.ModelAdmin):
    list_display = ['contrato', 'tipo_criterio', 'ativo']
    list_filter = ['ativo']
    search_fields = ['contrato__numero_contrato', 'tipo_criterio']


@admin.register(BoletimMedicao)
class BoletimMedicaoAdmin(admin.ModelAdmin):
    list_display = ['contrato', 'mes_referencia', 'ano_referencia', 'valor_liquido', 'status']
    list_filter = ['status', 'ano_referencia', 'mes_referencia']
    search_fields = ['contrato__numero_contrato']


@admin.register(ItemMedicao)
class ItemMedicaoAdmin(admin.ModelAdmin):
    list_display = ['boletim', 'equipamento', 'horas_trabalhadas', 'horas_descontaveis', 'valor_total']
    search_fields = ['boletim__contrato__numero_contrato', 'equipamento__codigo']


@admin.register(LogAlteracao)
class LogAlteracaoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tabela_afetada', 'id_registro', 'operacao', 'created_at']
    list_filter = ['operacao', 'tabela_afetada', 'created_at']
    search_fields = ['usuario__username', 'tabela_afetada']
    date_hierarchy = 'created_at'


@admin.register(EvidenciaFotografica)
class EvidenciaFotograficaAdmin(admin.ModelAdmin):
    list_display = ['id', 'parte_diaria', 'apropriacao', 'data_foto']
    list_filter = ['data_foto']
    search_fields = ['descricao']
    date_hierarchy = 'data_foto'


@admin.register(Importacao)
class ImportacaoAdmin(admin.ModelAdmin):
    list_display = ['tipo_dados', 'nome_arquivo', 'usuario', 'status', 'data_importacao']
    list_filter = ['tipo_dados', 'status', 'data_importacao']
    search_fields = ['nome_arquivo', 'usuario__username']
    date_hierarchy = 'data_importacao'
    readonly_fields = ['resultado_processamento']
