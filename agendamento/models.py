from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    prestador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='servicos',
        null=True,
        blank=True,
    )
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    duracao_estimada = models.PositiveIntegerField(help_text="Duração em minutos")

    def __str__(self):
        return self.nome


class LocalAtendimento(models.Model):
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    referencia = models.TextField(blank=True)

    def __str__(self):
        return f"{self.endereco} - {self.bairro}"


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    local = models.ForeignKey(LocalAtendimento, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.servico.nome} - {self.data} {self.horario}"


class CustomizacaoHeader(models.Model):
    LOGO_POSICAO_CHOICES = [
        ('esquerda', 'Esquerda'),
        ('centro', 'Centro'),
    ]

    titulo = models.CharField(max_length=100, default='Agenda Fácil', blank=True)
    subtitulo = models.CharField(
        max_length=255,
        default='Agende serviços de forma simples, rápida e organizada.',
        blank=True,
    )
    exibir_titulo_subtitulo = models.BooleanField(default=True)
    cor_header = models.CharField(max_length=7, default='#6b7b4b')
    logo = models.ImageField(upload_to='header_logos/', null=True, blank=True)
    logo_posicao = models.CharField(max_length=10, choices=LOGO_POSICAO_CHOICES, default='esquerda')

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Customização do Header'


class Reclamacao(models.Model):
    NOTA_CHOICES = [
        ('1', '1 estrela'),
        ('2', '2 estrelas'),
        ('3', '3 estrelas'),
        ('4', '4 estrelas'),
        ('5', '5 estrelas'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField()
    servico_contratado = models.CharField(max_length=200)
    descricao = models.TextField()
    nota = models.CharField(max_length=1, choices=NOTA_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} — {self.servico_contratado} ({self.nota}★)"