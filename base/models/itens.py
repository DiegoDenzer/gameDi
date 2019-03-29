import uuid

from django.db import models
from django.db.models import UUIDField


# Create your models here.
from base.models.arma import Arma
from base.models.armadura import Armadura
from base.models.pocao import Pocao


class MaterialCraft(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Material Craft'
        verbose_name_plural = 'Materiais Craft'

    def __str__(self):
        return '{}'.format(self.nome)


class Receita(models.Model):

    id = UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    level = models.PositiveIntegerField(default=1)
    nome = models.CharField(max_length=100)
    arma = models.ForeignKey(Arma, on_delete=models.CASCADE, null=True, blank=True)
    armadura = models.ForeignKey(Armadura, on_delete=models.CASCADE, null=True, blank=True)
    pocao = models.ForeignKey(Pocao, on_delete=models.CASCADE, null=True, blank=True)

    ingrediente_1 = models.ForeignKey(MaterialCraft, on_delete=models.CASCADE,
                                      null=True, blank=True, related_name='ingredietes1')
    ingrediente_2 = models.ForeignKey(MaterialCraft, on_delete=models.CASCADE,
                                      null=True, blank=True, related_name='ingredietes2')
    ingrediente_3 = models.ForeignKey(MaterialCraft, on_delete=models.CASCADE,
                                      null=True, blank=True, related_name='ingredietes3')
    qtd_1 = models.PositiveIntegerField(default=1)
    qtd_2 = models.PositiveIntegerField(default=1)
    qtd_3 = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
        db_table = 'receita'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.nome