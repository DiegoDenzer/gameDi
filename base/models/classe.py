from django.db import models


class Classe(models.Model):

    nome = models.CharField(max_length=100)

    # ATB de batalha Iniciais de cada classe

    indice_ataque_inicial = models.PositiveSmallIntegerField(default=0)
    indice_defesa_inicial = models.PositiveSmallIntegerField(default=0)
    acurancia_magica_inicial = models.PositiveIntegerField(default=0)
    defesa_magica_inicial = models.PositiveIntegerField(default=0)
    dano_base_inicial = models.PositiveIntegerField(default=0)
    dano_mim_inicial = models.PositiveIntegerField(default=0)
    dano_max_inicial = models.PositiveIntegerField(default=0)


    # ATB de batalha Por Level de cada classe
    indice_ataque_up = models.PositiveSmallIntegerField(default=0)
    indice_defesa_up = models.PositiveSmallIntegerField(default=0)
    acurancia_magica_up = models.PositiveIntegerField(default=0)
    defesa_magica_up = models.PositiveIntegerField(default=0)

    hp_up = models.PositiveIntegerField(default=0)

    # ATB basicos que definem casa classe

    hp_inicial = models.PositiveIntegerField(default=0)  # pontos ficsicos
    forca_inicial = models.PositiveSmallIntegerField(default=0)
    agilidade_inicial = models.PositiveSmallIntegerField(default=0)
    inteligencia_inicial = models.PositiveSmallIntegerField(default=0)
    sabedoria_inicial = models.PositiveSmallIntegerField(default=0)
    carisma_inicial = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'classe'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return f"{self.nome}"
