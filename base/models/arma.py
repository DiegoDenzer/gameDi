from django.db import models
from django.urls import reverse

from base.util.enum import ATRIBUTO_EXTRA


class Arma(models.Model):

    dano_min = models.PositiveIntegerField(default=1)
    dano_max = models.PositiveIntegerField(default=1)
    compra = models.PositiveIntegerField(default=0)  # valor de compra
    venda = models.PositiveIntegerField(default=0)  # valor de venda
    update = models.PositiveSmallIntegerField(default=0)
    nivel = models.PositiveIntegerField(default=0)

    forca_minima = models.PositiveIntegerField(default=0)
    agilidade_minima = models.PositiveIntegerField(default=0)
    inteligenica_minima = models.PositiveIntegerField(default=0)



    atributo_extra = models.CharField(choices=ATRIBUTO_EXTRA, null=True, blank=True, max_length = 2)
    valor_extra = models.PositiveIntegerField(default=0)

    imagem = models.ImageField(upload_to="armas", null=True, blank=True)

    # nome do item
    nome = models.CharField(max_length=100)

    class Meta:
        db_table = 'arma'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('arma_detail', args=(self.pk,))
