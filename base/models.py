import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Classe(models.Model):

    nome = models.CharField(max_length=100)
    ataque = models.PositiveSmallIntegerField(default=0)
    defesa = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'classe'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.nome


class Arma(models.Model):

    poder = models.PositiveSmallIntegerField(default=1)
    compra = models.FloatField(default=0)  # valor de compra
    venda = models.FloatField(default=0)  # valor de venda
    update = models.PositiveSmallIntegerField(default=0)

    imagem = models.ImageField(upload_to="armas")

    # nome do item
    nome = models.CharField(max_length=100)

    class Meta:
        db_table = 'arma'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('arma_detail', args=(self.pk,))


class Armadura(models.Model):

    poder = models.PositiveSmallIntegerField(default=1)
    compra = models.FloatField(default=0)  # valor de compra
    venda = models.FloatField(default=0)  # valor de venda
    update = models.PositiveSmallIntegerField(default=0)

    imagem = models.ImageField(upload_to="armas")

    # nome do item
    nome = models.CharField(max_length=100)

    class Meta:
        db_table = 'armadura'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('armadura_detail', args=(self.pk,))



class Personagem(models.Model):

    nome = models.CharField(max_length=30)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # campos que definem o player do jogo
    gold = models.PositiveIntegerField(default=0)  # dinheiro na mao

    ataque = models.PositiveSmallIntegerField(default=10)
    defesa = models.PositiveSmallIntegerField(default=10)
    vida = models.PositiveSmallIntegerField(default=10)
    energia = models.PositiveSmallIntegerField(default=20)  # energia para fazer quests
    raiva = models.PositiveSmallIntegerField(default=5)  # raiva para atacar outros players

    hp = models.PositiveIntegerField(default=100)  # hp = vida * 10
    energia_atual = models.PositiveIntegerField(default=20)
    raiva_atual = models.PositiveIntegerField(default=5)

    nivel = models.PositiveSmallIntegerField(default=1)
    experiencia = models.PositiveIntegerField(default=0)

    hp_update = models.DateTimeField(auto_now_add=True)  # 1 de hp a cada 2 minutos
    energia_update = models.DateTimeField(auto_now_add=True)  # 1 de energia a cada minuto
    raiva_update = models.DateTimeField(auto_now_add=True)  # 1 de raiva a cada 5 minutos

    # relacionamentos
    armas = models.ForeignKey(Arma, on_delete=models.CASCADE, null=True)
    armaduras = models.ForeignKey(Armadura, on_delete=models.CASCADE , null=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, null=True)


    # pontos ao subir de nivel
    pontos = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'personagem'
        ordering = ('-pk',)

    def __unicode__(self):
        return u'%s' % self.pk

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('persoangem_detail', args=(self.pk,))



    # verifica se o player subiu de nivel
    def level_up(self):
        # definimos a quantidade de xp para cada nivel
        experiencia_necessaria = {1: 10, 2: 20, 3: 30, 4: 50, 5: 80,
                                  6: 130, 7: 210, 8: 340, 9: 480, 10: 630,
                                  11: 790, 12: 970, 13: 1200, 14: 1600, 15: 2000,
                                  16: 2500, 17: 3000, 18: 4000, 19: 5000, 20: 6000}

        if self.experiencia >= experiencia_necessaria[self.nivel + 1]:
            self.nivel = self.nivel + 1  # sobe de nivel
            self.pontos = self.pontos + 5  # adiciona 5 pontos para o usuario distribuir
            self.hp = self.vida * 10  # recupera a vida
            self.energia_atual = self.energia  # recupera a energia
            self.raiva_atual = self.raiva  # recupera a raiva

            return True
        else:
            return False

    # funcao que recupera o player
    def refresh(self):
        # pega a hora atual
        agora = datetime.datetime.now()

        # verifica se o usuario tem menos HP do que deveria
        if self.hp < self.vida * 10:
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
                if self.hp > self.vida * 10:
                    self.hp = self.vida * 10
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