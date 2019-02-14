import uuid
from random import randint

from django.db import models
from django.db.models import UUIDField


class Inimigo(models.Model):

    id = UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    nome = models.CharField(max_length=60)

    agilidade = models.PositiveIntegerField(default=1)

    dano_min = models.PositiveIntegerField(default=1)
    dano_max = models.PositiveIntegerField(default=1)

    hp = models.PositiveIntegerField(default=0)

    indice_ataque = models.PositiveSmallIntegerField(default=0)  # Fisico
    indice_defesa = models.PositiveSmallIntegerField(default=0)  # Defesa Fisica

    def __str__(self):
        return self.nome

    def ataque(self, valor_dado):
        return valor_dado + self.indice_ataque

    @property
    def dano(self):
        return randint(self.dano_min, self.dano_max + 1)

    @property
    def defesa(self):
        return self.indice_defesa
