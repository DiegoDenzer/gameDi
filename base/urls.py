from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from base.views.forja import ForjaView, MostrarReceitasView
from base.views.inventario import UsarPocaoView, EquiparView
from base.views.loja import LojaListView, ComprarArmaView, ComprarPocaoView
from base.views.luta import ListarAdversariosView, AtacarView
from base.views.personagem import PersonagensListView, PersonagemCreatedView, logout_view, SelecionarView, \
    PersonagemDeleteView, PesonagemDetailView, AddAtaque, AddEnergia, AddRaiva, ClasseViewSet, \
    AddAgilidade, AddInteligencia, AddSabedoria, AddCarisma
from base.views.quest import QuestListView, QuestView

router = routers.DefaultRouter()
router.register(r'classes', ClasseViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('', logout_view, name='logout'),
    path('personagens', PersonagensListView.as_view(), name='personagens'),
    path('novo_personagem', PersonagemCreatedView.as_view(), name='novo_personagem'),
    path('personagem_detail', PesonagemDetailView.as_view(), name='personagem_detail'),
    path('mundo', SelecionarView.as_view(), name='mundo'),
    path('deletar/<str:player>', PersonagemDeleteView.as_view(), name='deletar'),
    path('add_ataque', AddAtaque.as_view(), name='add_ataque'),
    path('add_agilidae', AddAgilidade.as_view(), name='add_agilidade'),
    path('add_inteligencia', AddInteligencia.as_view(), name='add_inteligencia'),
    path('add_sabedoria', AddSabedoria.as_view(), name='add_sabedoria'),
    path('add_carisma', AddCarisma.as_view(), name='add_carisma'),
    path('add_energia', AddEnergia.as_view(), name='add_energia'),
    path('add_raiva', AddRaiva.as_view(), name='add_raiva'),

    path('atacar/<str:alvo>', AtacarView.as_view(), name='atacar'),

    # Bases
    path('alvos', ListarAdversariosView.as_view(), name='alvos'),
    path('quests', QuestListView.as_view(), name='quests'),
    path('quest<int:quest>', QuestView.as_view(), name='quest'),

    # Usar itens Inventario
    path('pocao/<str:item>', UsarPocaoView.as_view(), name='pocao'),
    path('equipar/<str:item>', EquiparView.as_view(), name='equipar'),

    # Loja
    path('loja', LojaListView.as_view(), name='loja'),
    path('comprar_arma', ComprarArmaView.as_view(), name='comprar_arma'),
    path('comprar_armadura', ComprarArmaView.as_view(), name='comprar_armadura'),
    path('comprar_pocao', ComprarPocaoView.as_view(), name='comprar_pocao'),

    # Forja
    path('forja', ForjaView.as_view(), name='forja'),
    path('criar_item', MostrarReceitasView.as_view(), name='receitas'),

    # path('token/', obtain_jwt_token),
]