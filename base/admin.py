from django.contrib import admin

# Register your models here.
from base.models.arma import Arma
from base.models.armadura import Armadura
from base.models.classe import Classe
from base.models.inimigo import Inimigo
from base.models.inventario import Inventario, InventarioItem
from base.models.itens import Receita, MaterialCraft
from base.models.personagem import Personagem
from base.models.pocao import Pocao
from base.models.quest import Quest, QuestInimigo


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
    fieldsets = (
        ('Basico', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('nome', 'nivel', 'compra', 'venda'),
        }),
        ('Dano', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('dano_min', 'dano_max'),
        })
    )

class ArmaduraAdmin(admin.ModelAdmin):
    pass


class PersonagemAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Basico', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('nome', 'classe', 'user', 'nivel', 'gold', 'hp', 'hp_atual'),
        }),

        ('Ataque / Defesa', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('dano_minimo', 'dano_max', 'armas', 'armaduras'),
        }),

        ('Atributos', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('agilidade', 'forca', 'inteligencia', 'sabedoria', 'carisma'),
        })
    )

class InventarioItemTabular(admin.TabularInline):
    model = InventarioItem

class InvertarioAdmin(admin.ModelAdmin):
    inlines = (InventarioItemTabular,)

class PocaoAdmin(admin.ModelAdmin):
    pass


class QuestInimigoTabular(admin.TabularInline):
    model = QuestInimigo


class QuestAdmin(admin.ModelAdmin):
    inlines = (QuestInimigoTabular,)


class ReceitaAdmin(admin.ModelAdmin):
    pass


class InimigoAdmin(admin.ModelAdmin):
    pass

class MaterialCraftAdmin(admin.ModelAdmin):
    pass

admin.site.register(MaterialCraft, MaterialCraftAdmin)
admin.site.register(Inimigo, InimigoAdmin)
admin.site.register(Classe, ClasseAdmin)
admin.site.register(Arma, ArmaAdmin)
admin.site.register(Armadura, ArmaduraAdmin)
admin.site.register(Personagem, PersonagemAdmin)
admin.site.register(Pocao, PocaoAdmin)
admin.site.register(Quest, QuestAdmin)
admin.site.register(Inventario, InvertarioAdmin)
admin.site.register(Receita, ReceitaAdmin)

