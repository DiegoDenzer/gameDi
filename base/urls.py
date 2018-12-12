from django.urls import path

from base.views.luta import ListarAdversariosView
from base.views.personagem import PersonagensListView, PersonagemCreatedView, logout_view, SelecionarView, \
    PersonagemDeleteView
from base.views.quest import QuestListView, QuestView

urlpatterns = [
    path('', logout_view , name='logout'),
    path('personagens', PersonagensListView.as_view(), name='personagens'),
    path('novo_personagem', PersonagemCreatedView.as_view(), name='novo_personagem'),
    path('cidade/<int:player>', SelecionarView.as_view(), name='cidade'),
    path('deletar/<int:player>', PersonagemDeleteView.as_view(), name='deletar'),

    # Bases
    path('alvos', ListarAdversariosView.as_view(), name='alvos'),
    path('quests', QuestListView.as_view(), name='quests'),
    path('quest<int:quest>', QuestView.as_view(), name='quest'),

]