import uuid
from random import randint

from django.contrib.auth.models import User
from django.db import models
from django.db.models import UUIDField
from django.urls import reverse
from django.utils import timezone

from base.models.arma import Arma
from base.models.armadura import Armadura
from base.models.classe import Classe


class Personagem(models.Model):

    id = UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)

    nome = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  verbose_name='Usuário')

    # campos que definem o player do jogo
    gold = models.PositiveIntegerField(default=0)  # dinheiro na mao

    hp = models.PositiveIntegerField(default=0)  # pontos ficsicos
    hp_atual = models.PositiveIntegerField(default=0)  # atuais

    # ATB de batalha

    indice_ataque = models.PositiveSmallIntegerField(default=0)  # Fisico
    indice_defesa = models.PositiveSmallIntegerField(default=0)  # Defesa Fisica
    acurancia_magica = models.PositiveIntegerField(default=0)
    defesa_magica = models.PositiveIntegerField(default=0)

    dano_minimo = models.PositiveIntegerField(default=0)
    dano_max = models.PositiveIntegerField(default=0)

    # ATB basicos

    forca = models.PositiveSmallIntegerField(default=0)
    agilidade = models.PositiveSmallIntegerField(default=0)
    inteligencia = models.PositiveSmallIntegerField(default=0)
    sabedoria = models.PositiveSmallIntegerField(default=0)
    carisma = models.PositiveSmallIntegerField(default=0)

    # Controle de ações do personagem.

    energia = models.PositiveSmallIntegerField(default=20)  # energia para fazer quests
    raiva = models.PositiveSmallIntegerField(default=5)  # raiva para atacar outros players

    energia_atual = models.PositiveIntegerField(default=20)
    raiva_atual = models.PositiveIntegerField(default=5)

    nivel = models.PositiveSmallIntegerField(default=1)
    experiencia = models.PositiveIntegerField(default=0)

    hp_update = models.DateTimeField(auto_now_add=True)  # 1 de hp a cada 2 minutos
    energia_update = models.DateTimeField(auto_now_add=True)  # 1 de energia a cada minuto
    raiva_update = models.DateTimeField(auto_now_add=True)  # 1 de raiva a cada 5 minutos


    # relacionamentos

    armas = models.ForeignKey(Arma, on_delete=models.CASCADE, null=True, blank=True)
    armaduras = models.ForeignKey(Armadura, on_delete=models.CASCADE, null=True, blank=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, null=True)

    # pontos ao subir de nivel
    pontos = models.PositiveSmallIntegerField(default=0)

    def criar_personagem(self, classe=None, user=None, nome=None):
        self.nome = nome
        self.classe = classe
        self.user = user

        self.save()

        # colocar Atb da classe
        self.hp = classe.hp_inicial
        self.hp_atual = self.hp

        # Basicos

        self.forca = classe.forca_inicial
        self.inteligencia = classe.inteligencia_inicial
        self.agilidade = classe.agilidade_inicial
        self.sabedoria = classe.sabedoria_inicial
        self.carisma = classe.carisma_inicial

        # ataque/ defesa

        self.acurancia_magica = classe.acurancia_magica_inicial
        self.defesa_magica = classe.defesa_magica_inicial
        self.indice_defesa = classe.indice_defesa_inicial
        self.indice_ataque = classe.indice_ataque_inicial
        self.dano_minimo = classe.dano_mim_inicial
        self.dano_max = classe.dano_max_inicial
        self.save()

    class Meta:
        db_table = 'personagem'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.nome

    def atacar(self):
        return

    def get_delete_url(self):
        return reverse('deletar', args=(self.pk,))

    def get_absolute_url(self):
        return reverse('selecao', args=(self.pk,))

    # verifica se o player subiu de nível
    def level_up(self):
        # definimos a quantidade de xp para cada nivel
        experiencia_necessaria = {1: 10, 2: 25, 3: 50, 4: 80, 5: 115,
                                  6: 155, 7: 210, 8: 340, 9: 480, 10: 630,
                                  11: 790, 12: 970, 13: 1200, 14: 1600, 15: 2000,
                                  16: 2500, 17: 3000, 18: 4000, 19: 5200, 20: 6500}

        if self.experiencia >= experiencia_necessaria[self.nivel + 1]:
            self.nivel = self.nivel + 1  # sobe de nivel
            self.pontos = self.pontos + 5  # adiciona 5 pontos para o usuario distribuir
            self.hp += self.classe.hp_up# Maximo de vida
            self.hp_atual = self.hp
            self.energia_atual = self.energia  # recupera a energia
            self.raiva_atual = self.raiva  # recupera a raiva

            # Aumentando ATB de Combate.
            self.indice_ataque += self.classe.indice_ataque_up
            self.indice_defesa += self.classe.indice_defesa_up
            self.acurancia_magica += self.classe.acurancia_magica_up
            self.defesa_magica += self.classe.defesa_magica_up
            self.dano_minimo = self.nivel * self.dano_minimo
            self.dano_max = self.nivel * self.dano_max

            return True
        else:
            return False

    # funcao que recupera o player
    def refresh(self):
        # pega a hora atual
        # agora = datetime.datetime.now()
        agora = timezone.now()
        # verifica se o usuario tem menos HP do que deveria
        if self.hp < self.hp_atual:
            # verifica quanto tempo passou desde a ultima atualizacao do hp
            tempo = agora - self.hp_update
            # o hp atualiza a cada dois minutos
            # verifica quantas vezes 2 minutos se passaram no intervalo de tempo
            updates = tempo.total_seconds() // 120

            # verifica se houve algum update
            if updates > 0:
                # adiciona a quantidade de updates no hp
                self.hp = self.hp + updates
                # verifica se ficamos com mais hp do que o maximo permitido
                if self.hp_atual > self.hp:
                    self.hp_atual = self.hp
                # agora que verificou o ultimo update de hp, atualiza a variavel hp_update
                self.hp_update = agora
        else:
            # se nao existe nenhum update para fazer, atualiza o hp_update
            self.hp_update = agora

        # verifica se o usuario tem menos energia do que deveria
        if self.energia_atual < self.energia:
            # verifica quanto tempo passou desde a ultima atualizacao do hp
            tempo = agora - self.energia_update
            # a energia atualiza a cada minuto
            # verifica quantos minutos se passaram no intervalo de tempo
            updates = tempo.total_seconds() // 60

            # verifica se houve algum update
            if updates > 0:
                # adiciona a quantidade de updates na energia
                self.energia_atual = self.energia_atual + updates
                # verifica se ficamos com mais energia do que o maximo permitido
                if self.energia_atual > self.energia:
                    self.energia_atual = self.energia
                # agora que verificou o ultimo update da energia, atualiza a variavel energia_update
                self.energia_update = agora
        else:
            # se nao existe nenhum update para fazer, atualiza o energia_update
            self.energia_update = agora

        # verifica se o usuario tem menos raiva do que deveria
        if self.raiva_atual < self.raiva:
            # verifica quanto tempo passou desde a ultima atualizacao da raiva
            tempo = agora - self.raiva_update
            # a raiva atualiza a cada 5 minutos
            # verifica quantos minutos se passaram no intervalo de tempo
            updates = tempo.total_seconds() // 300

            # verifica se houve algum update
            if updates > 0:
                # adiciona a quantidade de updates na raiva
                self.raiva_atual = self.raiva_atual + updates
                # verifica se ficamos com mais raiva do que o maximo permitido
                if self.raiva_atual > self.raiva:
                    self.raiva_atual = self.raiva
                # agora que verificou o ultimo update da raiva, atualiza a variavel raiva_update
                self.raiva_update = agora
        else:
            # se nao existe nenhum update para fazer, atualiza o raiva_update
            self.raiva_update = agora

    def ataque(self, valor_dado):
        if self.armas:
            if self.armas.atributo_extra:
                if self.armas.atributo_extra == 'IA':
                    return valor_dado + self.indice_ataque + self.armas.valor_extra
        else:
            return valor_dado + self.indice_ataque

    @property
    def dano(self):
        if self.armas:
            return randint(self.dano_minimo, self.dano_max+1) + randint(self.armas.dano_min, self.armas.dano_max)
        else:
            return randint(self.dano_minimo, self.dano_max + 1)

    @property
    def defesa(self):
        return self.indice_defesa
