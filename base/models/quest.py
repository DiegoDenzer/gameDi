import uuid

from django.db import models
from django.db.models import UUIDField

from base.models.inimigo import Inimigo
from base.models.itens import MaterialCraft


class Quest(models.Model):

    nivel = models.PositiveIntegerField(default=0)  # nível necessário
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=250)

    gasto_energia = models.PositiveIntegerField(default=0)  # gasto de energia

    ganho_experiencia = models.PositiveIntegerField(default=0)  # ganho de experiencia
    ganho_gold = models.PositiveIntegerField(default=0)  # ganho de gold

    materialDrop = models.ForeignKey(MaterialCraft, on_delete=models.CASCADE, null=True, blank=True)  # Material para craft

    chance_material_drop = models.PositiveIntegerField(default=0)
       

    class Meta:
        db_table = 'quest'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.nome


class QuestInimigo(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE, related_name='inimigos')
    inimigo = models.ForeignKey(Inimigo, on_delete=models.CASCADE)
