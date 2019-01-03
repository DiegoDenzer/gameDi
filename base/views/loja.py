import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from base.models import Personagem, Arma, Armadura, InventarioItem, Inventario, Pocao
from base.util.util import valida_jogador


class LojaListView(LoginRequiredMixin, View):
    login_url = '/'

    def get(self, request):
        jogador = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, jogador):
            jogador.refresh()

            dados = {
                'armas': Arma.objects.all().order_by('nivel'),
                'armaduras': Armadura.objects.all().order_by('nivel'),
                'pocoes': Pocao.objects.all().order_by('nivel'),
                'personagem':jogador
            }

            return render(request, 'base/loja.html', dados)


class ComprarArmaView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request):
        jogador = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, jogador):
            arma_id = request.POST['arma']
            arma = Arma.objects.get(pk=arma_id)
            if jogador.gold > arma.compra:
                InventarioItem.objects.create(id=uuid.uuid4(), arma=arma,
                                              inventario=Inventario.objects.get(personagem=jogador)),
                return redirect('loja')


class ComprarArmaduraView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request):
        jogador = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, jogador):
            armadura_id = request.POST['arma']
            armadura = Armadura.objects.get(pk=armadura_id)
            if jogador.gold >= armadura.compra:
                InventarioItem.objects.create(id=uuid.uuid4(), armadura=armadura,
                                              inventario=Inventario.objects.get(personagem=jogador)),
                return redirect('loja')


class ComprarPocaoView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request):
        jogador = Personagem.objects.get(pk=request.session['player_id'])
        if valida_jogador(request, jogador):
            pocao_id = request.POST['arma']
            pocao = Pocao.objects.get(pk=pocao_id)
            if jogador.gold >= pocao.compra:
                InventarioItem.objects.create(id=uuid.uuid4(), pocao=pocao,
                                              inventario=Inventario.objects.get(personagem=jogador)),
                return redirect('loja')
