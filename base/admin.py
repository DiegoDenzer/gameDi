from django.contrib import admin

# Register your models here.
from base.models import Classe, Arma, Armadura, Personagem, Inventario, Pocao, Quest


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


admin.site.register(Classe, ClasseAdmin)
admin.site.register(Arma, ArmaAdmin)
admin.site.register(Armadura, ArmaduraAdmin)
admin.site.register(Personagem, PersonagemAdmin)
admin.site.register(Pocao, PocaoAdmin)
admin.site.register(Quest, QuestAdmin)
admin.site.register(Inventario, InvertarioAdmin)

