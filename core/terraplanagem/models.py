from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


# ============================================================================
# PERFIS E USUÁRIOS
# ============================================================================

class Perfil(models.Model):
    """Model para perfis de usuário com permissões"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    permissoes = models.JSONField(default=dict, help_text="Permissões do perfil em formato JSON")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


# ============================================================================
# OBRAS, CONTRATOS E FORNECEDORES
# ============================================================================

class Obra(models.Model):
    """Model para obras"""
    STATUS_CHOICES = [
        ('planejamento', 'Planejamento'),
        ('em_andamento', 'Em Andamento'),
        ('paralisada', 'Paralisada'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    nome = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateField()
    data_fim_prevista = models.DateField()
    endereco = models.CharField(max_length=300)
    orcamento_total = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejamento')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Fornecedor(models.Model):
    """Model para fornecedores"""
    razao_social = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True)
    contato = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['razao_social']
    
    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"


class Contrato(models.Model):
    """Model para contratos de obra"""
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='contratos')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name='contratos')
    numero_contrato = models.CharField(max_length=50, unique=True)
    valor_total = models.DecimalField(
        max_digits=15, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    data_inicio = models.DateField()
    data_fim = models.DateField()
    observacoes = models.TextField(blank=True)
    regras_medicao = models.JSONField(default=dict, help_text="Regras de medição em formato JSON")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.numero_contrato} - {self.fornecedor.razao_social}"


# ============================================================================
# EQUIPAMENTOS
# ============================================================================

class Equipamento(models.Model):
    """Model para equipamentos"""
    STATUS_CHOICES = [
        ('operacional', 'Operacional'),
        ('manutencao', 'Em Manutenção'),
        ('parado', 'Parado'),
        ('inativo', 'Inativo'),
    ]
    
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='equipamentos')
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    horimetro_inicial = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operacional')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class ParteDiaria(models.Model):
    """Model para parte diária de equipamentos"""
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_validacao', 'Em Validação'),
        ('validado', 'Validado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='partes_diarias')
    apontador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='partes_apontadas'
    )
    motorista = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='partes_operadas'
    )
    data_servico = models.DateField()
    horimetro_inicial = models.IntegerField()
    horimetro_final = models.IntegerField()
    total_horas_trabalhadas = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    data_inicio = models.DateTimeField()
    data_fechamento = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Parte Diária'
        verbose_name_plural = 'Partes Diárias'
        ordering = ['-data_servico']
    
    def __str__(self):
        return f"PD {self.equipamento.codigo} - {self.data_servico}"


class AtividadeEquipamento(models.Model):
    """Model para atividades executadas por equipamentos"""
    TIPO_CHOICES = [
        ('produtiva', 'Produtiva'),
        ('improdutiva', 'Improdutiva'),
        ('manutencao', 'Manutenção'),
    ]
    
    parte_diaria = models.ForeignKey(ParteDiaria, on_delete=models.CASCADE, related_name='atividades')
    atividade = models.ForeignKey('Atividade', on_delete=models.PROTECT, related_name='atividades_equipamento')
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    duracao_minutos = models.IntegerField()
    observacoes = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='produtiva')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Atividade de Equipamento'
        verbose_name_plural = 'Atividades de Equipamentos'
        ordering = ['parte_diaria', 'hora_inicio']
    
    def __str__(self):
        return f"{self.parte_diaria.equipamento.codigo} - {self.atividade.codigo}"


# ============================================================================
# MÃO DE OBRA
# ============================================================================

class Funcionario(models.Model):
    """Model para funcionários"""
    nome = models.CharField(max_length=150)
    matricula = models.CharField(max_length=20, unique=True)
    funcao = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)
    salario_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.matricula} - {self.nome}"


class Equipe(models.Model):
    """Model para equipes de trabalho"""
    encarregado = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='equipes_encarregadas'
    )
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='equipes')
    nome_equipe = models.CharField(max_length=100)
    data_formacao = models.DateField()
    ativa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'
        ordering = ['obra', 'nome_equipe']
    
    def __str__(self):
        return f"{self.nome_equipe} - {self.obra.codigo}"


class EquipeFuncionario(models.Model):
    """Model para relacionamento entre equipes e funcionários"""
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='membros')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='equipes')
    data_entrada = models.DateField()
    data_saida = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Membro de Equipe'
        verbose_name_plural = 'Membros de Equipe'
        ordering = ['equipe', 'funcionario']
        unique_together = [['equipe', 'funcionario', 'data_entrada']]
    
    def __str__(self):
        return f"{self.funcionario.nome} - {self.equipe.nome_equipe}"


class ApropriacaoMaoObra(models.Model):
    """Model para apropriação de mão de obra"""
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_validacao', 'Em Validação'),
        ('validado', 'Validado'),
        ('rejeitado', 'Rejeitado'),
    ]
    
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='apropriacoes')
    atividade = models.ForeignKey('Atividade', on_delete=models.PROTECT, related_name='apropriacoes_mao_obra')
    encarregado = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='apropriacoes_validadas'
    )
    data_servico = models.DateField()
    horas_trabalhadas = models.IntegerField()
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Apropriação de Mão de Obra'
        verbose_name_plural = 'Apropriações de Mão de Obra'
        ordering = ['-data_servico']
    
    def __str__(self):
        return f"{self.funcionario.nome} - {self.atividade.codigo} - {self.data_servico}"


# ============================================================================
# ATIVIDADES E LOCALIZAÇÕES
# ============================================================================

class Atividade(models.Model):
    """Model para atividades de obra"""
    CATEGORIA_CHOICES = [
        ('terraplenagem', 'Terraplenagem'),
        ('drenagem', 'Drenagem'),
        ('pavimentacao', 'Pavimentação'),
        ('obras_arte', 'Obras de Arte'),
        ('sinalizacao', 'Sinalização'),
        ('outros', 'Outros'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.CharField(max_length=300)
    unidade_medida = models.CharField(max_length=20, help_text="Ex: m³, m², km, un")
    preco_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES, default='terraplenagem')
    ativa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class Localizacao(models.Model):
    """Model para localizações dentro da obra"""
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='localizacoes')
    estaqueamento = models.CharField(max_length=50, help_text="Ex: EST 120+10")
    descricao = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Localização'
        verbose_name_plural = 'Localizações'
        ordering = ['obra', 'estaqueamento']
    
    def __str__(self):
        return f"{self.obra.codigo} - {self.estaqueamento}"


class AtividadeLocalizacao(models.Model):
    """Model para registro de atividades em localizações específicas"""
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, related_name='localizacoes')
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE, related_name='atividades')
    data_execucao = models.DateField()
    quantidade_executada = models.DecimalField(max_digits=10, decimal_places=2)
    unidade = models.CharField(max_length=20)
    apontador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='atividades_localizacao_apontadas'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Atividade em Localização'
        verbose_name_plural = 'Atividades em Localizações'
        ordering = ['-data_execucao']
    
    def __str__(self):
        return f"{self.atividade.codigo} - {self.localizacao.estaqueamento}"


# ============================================================================
# MANUTENÇÃO
# ============================================================================

class MotivoManutencao(models.Model):
    """Model para motivos de manutenção"""
    RESPONSABILIDADE_CHOICES = [
        ('contratada', 'Contratada'),
        ('contratante', 'Contratante'),
        ('terceiro', 'Terceiro'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True)
    descricao = models.CharField(max_length=200)
    descontavel = models.BooleanField(default=False, help_text="Se deve ser descontado da medição")
    responsabilidade = models.CharField(max_length=20, choices=RESPONSABILIDADE_CHOICES, default='contratada')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Motivo de Manutenção'
        verbose_name_plural = 'Motivos de Manutenção'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class Manutencao(models.Model):
    """Model para manutenções de equipamentos"""
    TIPO_CHOICES = [
        ('preventiva', 'Preventiva'),
        ('corretiva', 'Corretiva'),
        ('preditiva', 'Preditiva'),
    ]
    
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='manutencoes')
    motivo = models.ForeignKey(MotivoManutencao, on_delete=models.PROTECT, related_name='manutencoes')
    apontador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='manutencoes_apontadas'
    )
    data_saida = models.DateTimeField()
    data_retorno = models.DateTimeField(null=True, blank=True)
    descricao_problema = models.TextField()
    solucao_aplicada = models.TextField(blank=True)
    tipo_manutencao = models.CharField(max_length=20, choices=TIPO_CHOICES, default='corretiva')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'
        ordering = ['-data_saida']
    
    def __str__(self):
        return f"{self.equipamento.codigo} - {self.motivo.codigo} - {self.data_saida.date()}"


class ParadaEquipamento(models.Model):
    """Model para paradas de equipamento"""
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='paradas')
    motivo = models.ForeignKey(MotivoManutencao, on_delete=models.PROTECT, related_name='paradas')
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField(null=True, blank=True)
    duracao_minutos = models.IntegerField()
    observacoes = models.TextField(blank=True)
    origem = models.CharField(max_length=50, help_text="Sistema ou módulo de origem")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Parada de Equipamento'
        verbose_name_plural = 'Paradas de Equipamento'
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f"{self.equipamento.codigo} - {self.data_inicio.date()}"


# ============================================================================
# RDO E MEDIÇÃO
# ============================================================================

class RDO(models.Model):
    """Model para Relatório Diário de Obra"""
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('finalizado', 'Finalizado'),
        ('aprovado', 'Aprovado'),
    ]
    
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='rdos')
    administrador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='rdos_administrados'
    )
    data_servico = models.DateField()
    condicoes_climaticas = models.JSONField(default=dict, help_text="Temperatura, chuva, etc.")
    condicoes_area = models.JSONField(default=dict, help_text="Condições da área de trabalho")
    resumo_atividades = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    caminho_arquivo_pdf = models.CharField(max_length=500, blank=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'RDO'
        verbose_name_plural = 'RDOs'
        ordering = ['-data_servico']
        unique_together = [['obra', 'data_servico']]
    
    def __str__(self):
        return f"RDO {self.obra.codigo} - {self.data_servico}"


class RDOAtividade(models.Model):
    """Model para atividades executadas no RDO"""
    rdo = models.ForeignKey(RDO, on_delete=models.CASCADE, related_name='atividades')
    atividade = models.ForeignKey(Atividade, on_delete=models.PROTECT, related_name='rdos')
    quantidade_executada = models.DecimalField(max_digits=10, decimal_places=2)
    unidade = models.CharField(max_length=20)
    total_funcionarios = models.IntegerField()
    total_horas_homem = models.IntegerField()
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Atividade do RDO'
        verbose_name_plural = 'Atividades do RDO'
        ordering = ['rdo', 'atividade']
    
    def __str__(self):
        return f"{self.rdo} - {self.atividade.codigo}"


class CriterioMedicao(models.Model):
    """Model para critérios de medição de contratos"""
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='criterios_medicao')
    tipo_criterio = models.CharField(max_length=100)
    regras = models.JSONField(default=dict, help_text="Regras do critério em JSON")
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Critério de Medição'
        verbose_name_plural = 'Critérios de Medição'
        ordering = ['contrato', 'tipo_criterio']
    
    def __str__(self):
        return f"{self.contrato.numero_contrato} - {self.tipo_criterio}"


class BoletimMedicao(models.Model):
    """Model para boletins de medição"""
    STATUS_CHOICES = [
        ('em_preparacao', 'Em Preparação'),
        ('enviado', 'Enviado'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
        ('pago', 'Pago'),
    ]
    
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='boletins_medicao')
    mes_referencia = models.IntegerField(help_text="Mês de 1 a 12")
    ano_referencia = models.IntegerField()
    valor_bruto = models.DecimalField(max_digits=15, decimal_places=2)
    valor_descontos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    valor_liquido = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_preparacao')
    data_geracao = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Boletim de Medição'
        verbose_name_plural = 'Boletins de Medição'
        ordering = ['-ano_referencia', '-mes_referencia']
        unique_together = [['contrato', 'mes_referencia', 'ano_referencia']]
    
    def __str__(self):
        return f"BM {self.contrato.numero_contrato} - {self.mes_referencia}/{self.ano_referencia}"


class ItemMedicao(models.Model):
    """Model para itens de medição"""
    boletim = models.ForeignKey(BoletimMedicao, on_delete=models.CASCADE, related_name='itens')
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT, related_name='itens_medicao')
    horas_trabalhadas = models.DecimalField(max_digits=10, decimal_places=2)
    horas_descontaveis = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)
    justificativa_desconto = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Item de Medição'
        verbose_name_plural = 'Itens de Medição'
        ordering = ['boletim', 'equipamento']
    
    def __str__(self):
        return f"{self.boletim} - {self.equipamento.codigo}"


# ============================================================================
# AUDITORIA E EVIDÊNCIAS
# ============================================================================

class LogAlteracao(models.Model):
    """Model para log de alterações no sistema"""
    OPERACAO_CHOICES = [
        ('CREATE', 'Criação'),
        ('UPDATE', 'Atualização'),
        ('DELETE', 'Exclusão'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='logs_alteracoes'
    )
    tabela_afetada = models.CharField(max_length=100)
    id_registro = models.IntegerField()
    dados_anteriores = models.JSONField(null=True, blank=True)
    dados_novos = models.JSONField(null=True, blank=True)
    operacao = models.CharField(max_length=10, choices=OPERACAO_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log de Alteração'
        verbose_name_plural = 'Logs de Alterações'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tabela_afetada', 'id_registro']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.operacao} - {self.tabela_afetada} #{self.id_registro}"


class EvidenciaFotografica(models.Model):
    """Model para evidências fotográficas"""
    parte_diaria = models.ForeignKey(
        ParteDiaria, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='evidencias'
    )
    apropriacao = models.ForeignKey(
        ApropriacaoMaoObra, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='evidencias'
    )
    caminho_arquivo = models.CharField(max_length=500)
    descricao = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    data_foto = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Evidência Fotográfica'
        verbose_name_plural = 'Evidências Fotográficas'
        ordering = ['-data_foto']
    
    def __str__(self):
        if self.parte_diaria:
            return f"Evidência PD {self.parte_diaria.id}"
        elif self.apropriacao:
            return f"Evidência APR {self.apropriacao.id}"
        return f"Evidência {self.id}"


class Importacao(models.Model):
    """Model para controle de importações de dados"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('processando', 'Processando'),
        ('sucesso', 'Sucesso'),
        ('erro', 'Erro'),
        ('parcial', 'Parcial'),
    ]
    
    TIPO_CHOICES = [
        ('obras', 'Obras'),
        ('equipamentos', 'Equipamentos'),
        ('funcionarios', 'Funcionários'),
        ('atividades', 'Atividades'),
        ('contratos', 'Contratos'),
        ('fornecedores', 'Fornecedores'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='importacoes'
    )
    tipo_dados = models.CharField(max_length=30, choices=TIPO_CHOICES)
    nome_arquivo = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    resultado_processamento = models.JSONField(
        default=dict, 
        help_text="Estatísticas e mensagens do processamento"
    )
    data_importacao = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Importação'
        verbose_name_plural = 'Importações'
        ordering = ['-data_importacao']
    
    def __str__(self):
        return f"{self.tipo_dados} - {self.nome_arquivo} ({self.status})"
