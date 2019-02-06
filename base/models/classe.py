from django.db import models


class Classe(models.Model):

    nome = models.CharField(max_length=100)
    ataque = models.PositiveSmallIntegerField(default=0)
    defesa = models.PositiveSmallIntegerField(default=0)
    destreza = models.PositiveSmallIntegerField(default=0)
    vida = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'classe'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return f"{self.nome}"
