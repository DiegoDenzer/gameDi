from django.contrib import admin

# Register your models here.
from base.models.arma import Arma
from base.models.armadura import Armadura
from base.models.classe import Classe
from base.models.inventario import Inventario
from base.models.itens import Receita
from base.models.personagem import Personagem
from base.models.pocao import Pocao
from base.models.quest import Quest


class ClasseAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Basico', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('nome', ),
        }),
        ('Ataque', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('indice_ataque_inicial','indice_ataque_up', 'dano_mim_inicial', 'dano_max_inicial',
                       'acurancia_magica_inicial', 'acurancia_magica_up', ),
        }),
        ('Defesa', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('indice_defesa_inicial', 'indice_defesa_up','defesa_magica_inicial', 'defesa_magica_up'),
        }),

        ('Atributos', {
            'classes': ('grp-collapse grp-open',),
            'fields': (('forca_inicial', 'agilidade_inicial', 'inteligencia_inicial', 'sabedoria_inicial',
                        'carisma_inicial', 'hp_inicial', 'hp_up')),
        })
    )


class ArmaAdmin(admin.ModelAdmin):
    pass


class ArmaduraAdmin(admin.ModelAdmin):
    pass


class PersonagemAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Basico', {
            'classes': ('grp-collapse grp-open',),
            'fields': (('nome', 'classe', 'user', 'nivel', 'gold')),
        }),
        ('Atributos', {
            'classes': ('grp-collapse grp-open',),
            'fields': (('agilidade', 'forca','inteligencia', 'sabedoria', 'carisma')),
        })
    )



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

