import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import UUIDField
from django.urls import reverse
from django.utils import timezone

class Armadura(models.Model):
    poder = models.PositiveIntegerField(default=1)
    compra = models.PositiveIntegerField(default=0)  # valor de compra
    venda = models.PositiveIntegerField(default=0)  # valor de venda
    update = models.PositiveSmallIntegerField(default=0)

    imagem = models.ImageField(upload_to="armas", null=True, blank=True)

    nivel = models.PositiveIntegerField(default=0)

    # nome do item
    nome = models.CharField(max_length=100)

    class Meta:
        db_table = 'armadura'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('armadura_detail', args=(self.pk,))