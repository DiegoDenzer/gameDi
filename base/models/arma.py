from django.db import models
from django.urls import reverse


class Arma(models.Model):
    poder = models.PositiveSmallIntegerField(default=1)
    compra = models.PositiveIntegerField(default=0)  # valor de compra
    venda = models.PositiveIntegerField(default=0)  # valor de venda
    update = models.PositiveSmallIntegerField(default=0)
    nivel = models.PositiveIntegerField(default=0)

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