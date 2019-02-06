from django.contrib import admin

# Register your models here.
from base.models import arma, personagem
from base.models.arma import Arma
from base.models.armadura import Armadura
from base.models.classe import Classe
from base.models.inventario import Inventario
from base.models.itens import Receita
from base.models.personagem import Personagem
from base.models.pocao import Pocao
from base.models.quest import Quest


class ClasseAdmin(admin.ModelAdmin):
    pass


class ArmaAdmin(admin.ModelAdmin):
    pass


class ArmaduraAdmin(admin.ModelAdmin):
    pass


class PersonagemAdmin(admin.ModelAdmin):
    pass


class InvertarioAdmin(admin.ModelAdmin):
    pass


class PocaoAdmin(admin.ModelAdmin):
    pass


class QuestAdmin(admin.ModelAdmin):
    pass


class ReceitaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Classe, ClasseAdmin)
admin.site.register(Arma, ArmaAdmin)
admin.site.register(Armadura, ArmaduraAdmin)
admin.site.register(Personagem, PersonagemAdmin)
admin.site.register(Pocao, PocaoAdmin)
admin.site.register(Quest, QuestAdmin)
admin.site.register(Inventario, InvertarioAdmin)
admin.site.register(Receita, ReceitaAdmin)

