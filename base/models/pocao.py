from django.db import models


class Pocao(models.Model):
    nivel = models.PositiveIntegerField(default=0)  # Nivel necessario
    nome = models.CharField(max_length=100)
    hp = models.PositiveIntegerField(default=0)
    energia = models.PositiveIntegerField(default=0)
    raiva = models.PositiveIntegerField(default=0)

    compra = models.PositiveIntegerField(default=0)  # valor de compra

    class Meta:
        verbose_name = 'Poção'
        verbose_name_plural = 'Poçoẽs'
        db_table = 'pocao'

    def __str__(self):
        return '{}'.format(self.nome)