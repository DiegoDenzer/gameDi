import uuid

from django.db import models
from django.db.models import UUIDField


class Inimigo(models.Model):

    id = UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    nome = models.CharField(max_length=60)

    agilidade = models.PositiveIntegerField(default=1)

    dano_min = models.PositiveIntegerField(default=1)
    dano_max = models.PositiveIntegerField(default=1)

    hp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome
