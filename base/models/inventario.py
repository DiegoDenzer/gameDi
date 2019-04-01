import uuid

from django.db import models
from django.db.models import UUIDField

from base.models.arma import Arma
from base.models.armadura import Armadura
from base.models.itens import MaterialCraft
from base.models.personagem import Personagem
from base.models.pocao import Pocao


class Inventario(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    personagem = models.ForeignKey(Personagem, on_delete=models.CASCADE)
    limite_max = models.IntegerField(default=30)

    def criar_inventario(self, personagem):
        self.personagem = personagem
        self.save()

    @property
    def numero_itens(self):
        return self.itens.all().count()

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        db_table = 'inventario'

    def __str__(self):
        return '{} {}/{} '.format(self.personagem.nome, self.numero_itens, self.limite_max)


class InventarioItem(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    inventario = models.ForeignKey(Inventario, related_name='itens', on_delete=models.CASCADE)
    arma = models.ForeignKey(Arma, on_delete=models.CASCADE, null=True, blank=True)
    armadura = models.ForeignKey(Armadura, on_delete=models.CASCADE, null=True, blank=True)
    itemDrop = models.ForeignKey(MaterialCraft, on_delete=models.CASCADE, null=True, blank=True)
    pocao = models.ForeignKey(Pocao, on_delete=models.CASCADE, null=True, blank=True)
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.arma is not None:
            return '{}'.format(self.arma)
        elif self.armadura is not None:
            return '{}'.format(self.armadura)
        elif self.pocao is not None:
            return '{}'.format(self.pocao)
        else:
            return '{}'.format(self.itemDrop)