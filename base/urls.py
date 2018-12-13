from django.urls import path

from base.views.luta import ListarAdversariosView
from base.views.personagem import PersonagensListView, PersonagemCreatedView, logout_view, SelecionarView, \
    PersonagemDeleteView, PesonagemDetailView, AddAtaque
from base.views.quest import QuestListView, QuestView

urlpatterns = [
    path('', logout_view , name='logout'),
    path('personagens', PersonagensListView.as_view(), name='personagens'),
    path('novo_personagem', PersonagemCreatedView.as_view(), name='novo_personagem'),
    path('personagem_detail', PesonagemDetailView.as_view(), name='personagem_detail'),
    path('mundo', SelecionarView.as_view(), name='mundo'),
    path('deletar/<int:player>', PersonagemDeleteView.as_view(), name='deletar'),
    path('add_ataque', AddAtaque.as_view(), name='add_ataque'),
    path('add_defesa', AddAtaque.as_view(), name='add_defesa'),
    path('add_vida', AddAtaque.as_view(), name='add_vida'),
    path('add_energia', AddAtaque.as_view(), name='add_energia'),
    path('add_raiva', AddAtaque.as_view(), name='add_raiva'),

    # Bases
    path('alvos', ListarAdversariosView.as_view(), name='alvos'),
    path('quests', QuestListView.as_view(), name='quests'),
    path('quest<int:quest>', QuestView.as_view(), name='quest'),

]