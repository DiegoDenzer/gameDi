from django.urls import path


from base.views.personagem import PersonagensListView, PersonagemCreatedView, logout_view, Selecionar

urlpatterns = [
    path('', logout_view , name='logout'),
    path('personagens', PersonagensListView.as_view(), name='personagens'),
    path('novo_personagem', PersonagemCreatedView.as_view(), name='novo_personagem'),
    path('selecionar/<int:player>', Selecionar.as_view(), name='selecao')
]