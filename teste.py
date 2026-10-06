import pyxel
import math

class Personagem:

    #difinições dos atributos dos personagens
    def __init__(self, x, y, largura, altura, cor,vida, velocidade, massa):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.vida = vida
        self.velocidade = velocidade
        self.massa = massa
        self.dano = massa*velocidade
        self.chao = True
        self.original_y = 0
        #velocidade é usada no lugar da aceleração
   
    """def set_cor(self, cor):
        self.cor = cor"""

    #desenhar o personagem
    def desenhar(self):
        if self.vida > 0:
            pyxel.rect(
                self.x,
                self.y,
                self.largura,
                self.altura,
                self.cor
        )

    def colisao(self, personagemB, inimigo):
       
        #colisao com o personagem não utilizado
        colisao_B = (
            personagemB.vida > 0 #para a colisao sumir apos o personagem morrer
            and
            self.x < personagemB.x + personagemB.largura #coodenada x do personagem < que o quadrado do outro
            and
            self.x + self.largura > personagemB.x #quadrado do personagem > que coodernada x do outro personagem
            and
            self.y < personagemB.y + personagemB.altura #coodenada y do personagem < que o quadrado do outro (y cresce para baixo)
            and
            self.y + self.altura > personagemB.y #quadrado do personagem > que coodernada y do outro personagem (y cresce para baixo)
        )

        colisao_inimigo =(
            inimigo.vida > 0 #para a colisao sumir apos o inimigo morrer
            and
            self.x < inimigo.x + inimigo.largura #coodenada x do personagem < que o quadrado do inimigo
            and self.x + self.largura > inimigo.x #quadrado do personagem > que coodernada x do inimigo
            and self.y < inimigo.y + inimigo.altura #coodenada y do personagem < que o quadrado do inimigo (y cresce para baixo)
            and self.y + self.altura > inimigo.y #quadrado do personagem > que coodernada y do inimigo (y cresce para baixo)
        )

        return colisao_B or colisao_inimigo

    def movimentacao(
        self,
        cima,
        baixo,
        esquerda,
        direita,
        personagemB,
        inimigo
    ):

        segundo_terceiro_y_original = self.y
        if pyxel.btn(direita):
            self.x += self.velocidade #caminha o equivalente a velocidade

            if self.colisao(personagemB, inimigo):# chamei a funcao colisao
                self.x -= self.velocidade #se a colisao for True, personagens não ocupam o mesmo espaço

            if self.x > 160 - self.largura:#fica dentro do espaço da tela
                self.x = 160 - self.largura

        if pyxel.btn(esquerda):
            self.x -= self.velocidade #caminha o equivalente a velocidade

            if self.colisao(personagemB, inimigo):# chamei a funcao colisao
                self.x += self.velocidade

            if self.x < 0: #fica dentro do espaço da tela
                self.x = 0

        if pyxel.btn(baixo):
            self.y += self.velocidade

            if self.colisao(personagemB, inimigo):
                self.y -= self.velocidade

            if self.y > 120 - self.altura:
                self.y = 120 - self.altura

        if pyxel.btn(cima):
            self.y -= self.velocidade
            self.original_y = self.y

            if self.colisao(personagemB, inimigo):
                self.y += self.velocidade

            if self.y < 0:
                self.y = 0

    def combate(self, ataque,pulo, Inimigo):
        if Inimigo.vida > 0:
            if pyxel.btnp(ataque):
                Inimigo.vida -= self.dano
        if pyxel.btnp(pulo):
            self.chao = False
            self.original_y = self.y
        if not self.chao:
            #se andar para cima ele cai
            if self.original_y - 10 < self.y:
                self.y -= 0.5
            else:
                self.chao = True
           
        else:
            if self.y < self.original_y:#erro esta aqui
                self.y += 0.5
                print(self.y, "y")
                print(self.original_y, "original y")
               
           
class Inimigo:

    def __init__(self, x, y, largura, altura, cor, vida, velocidade, massa, personagemA, personagemB):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.vida = vida
        self.velocidade = velocidade
        self.massa = massa
        self.dano = massa*velocidade
        self.personagemA_x = personagemA.x
        self.personagemB_x = personagemB.x
        self.personagemA_y = personagemA.y
        self.personagemB_y = personagemB.y


    def desenhar(self):
        if self.vida>0:
            pyxel.rect(
                self.x,
                self.y,
                self.largura,
                self.altura,
                self.cor
        )

    def colisao_i(self, personagemB, personagemA):

        colisao_B = (
            self.x < personagemB.x + personagemB.largura
            and
            self.x + self.largura > personagemB.x
            and
            self.y < personagemB.y + personagemB.altura
            and
            self.y + self.altura > personagemB.y
        )

        colisao_A = (
            self.x < personagemA.x + personagemA.largura
            and self.x + self.largura > personagemA.x
            and self.y < personagemA.y + personagemA.altura
            and self.y + self.altura > personagemA.y
        )

        return colisao_B or colisao_A
   
    def perseguir(self, personagemA, personagemB):
        if self.vida <= 0:#sem isso tu continua sendo perseguida, mesmo se o inimigo morrer
            return
       
       #salvar posições originais
        x_anterior = self.x
        y_anterior = self.y
       
        # "a" e "b" de pitagoras
        dx1 = personagemA.x - self.x
        dx2 = personagemB.x - self.x
        dy1 = personagemA.y - self.y
        dy2 = personagemB.y - self.y
       
        #pitagoras para indentificamos quem esta mais perto
        pitagoras1 = math.sqrt(dx1**2 + dy1**2)
        pitagoras2 = math.sqrt(dx2**2 + dy2**2)
       
        if pitagoras2 > pitagoras1:#True, persegue personagem1
           
           #personagemA.set_cor(15)

           if personagemA.x > self.x:#Se personagem1 mais a direita
                self.x += self.velocidade
           else:#Se personagem1 mais a esquerda
                self.x -= self.velocidade
           if personagemA.y > self.y:#Se personagem1 mais a baixo
                self.y += self.velocidade
           else:#Se personagem1 mais a cima
                self.y -= self.velocidade

        else:
           
           #personagemB.set_cor(8)

           if personagemB.x > self.x:#Se personagem2 mais a direita
                self.x += self.velocidade
           else:#Se personagem2 mais a esquerda
                self.x -= self.velocidade
           if personagemB.y > self.y:#Se personagem2 mais a baixo
                self.y += self.velocidade
           else:#Se personagem2 mais a cima
                self.y -= self.velocidade

        if self.colisao_i(
           personagemA,
           personagemB
        ):#não invadir na colisão
       

            #recuperando os valores originais, eles mudaram em pitagoras
            self.x = x_anterior
            self.y = y_anterior
           
class Jogo:

    def __init__(self):

        pyxel.init(160, 120)#tamanho da tela

        self.personagem1 = Personagem(
            20, 20, 10, 10, 5, 100, 5, 10)
            #x, y, largura, altura, cor,vida, velocidade, massa

        self.personagem2 = Personagem(
            20, 80, 10, 10, 6, 100, 5, 10)
            #x, y, largura, altura, cor,vida, velocidade, massa

        self.inimigo = Inimigo(
            80, 40, 10, 10, 8,300, 2, 5, self.personagem1, self.personagem2)
            #x, y, largura, altura, cor, vida, velocidade, massa, personagemA, personagemB

        pyxel.run(self.update, self.draw)#deixei nenhum ponha algo depois disso

    def update(self):
        # Personagem 1 - WASD
        self.personagem1.movimentacao(
            pyxel.KEY_W,
            pyxel.KEY_S,
            pyxel.KEY_A,
            pyxel.KEY_D,
            self.personagem2,
            self.inimigo
        )

        # Personagem 2 - Setas
        self.personagem2.movimentacao(
            pyxel.KEY_UP,
            pyxel.KEY_DOWN,
            pyxel.KEY_LEFT,
            pyxel.KEY_RIGHT,
            self.personagem1,
            self.inimigo
        )
       
        self.inimigo.perseguir(
            self.personagem2,
            self.personagem1
        )

        self.personagem1.combate(
            pyxel.KEY_J,
            pyxel.KEY_K,
            self.inimigo
        )

        self.personagem2.combate(
            pyxel.KEY_KP_1,
            pyxel.KEY_KP_2,
            self.inimigo
        )
       
    def draw(self):

        pyxel.cls(0)

        self.personagem1.desenhar()
        self.personagem2.desenhar()
        self.inimigo.desenhar()
        s = f" {self.inimigo.vida:>4}"#int para string
        pyxel.text(50, 60, s, 7)#texto na tela, s tem que ser string
       

Jogo()
