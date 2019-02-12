import uuid

from django.db import models
from django.db.models import UUIDField


class Inimigo(models.Model):

    id = UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    nome = models.CharField(max_length=60)
