import pyxel
import math

class Personagem:

    def __init__(self, x, y, largura, altura, cor,vida, velocidade, massa):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.vida = vida
        self.velocidade = velocidade
        self.massa = massa
        dano = massa*velocidade
        #velocidade é usada no lugar da aceleração
   
    def set_cor(self, cor):
        self.cor = cor

    def desenhar(self):
        pyxel.rect(
            self.x,
            self.y,
            self.largura,
            self.altura,
            self.cor
        )

    def colisao(self, personagemB, inimigo):

        colisao_B = (
            self.x < personagemB.x + personagemB.largura
            and
            self.x + self.largura > personagemB.x
            and
            self.y < personagemB.y + personagemB.altura
            and
            self.y + self.altura > personagemB.y
        )

        colisao_inimigo = (
            self.x < inimigo.x + inimigo.largura
            and self.x + self.largura > inimigo.x
            and self.y < inimigo.y + inimigo.altura
            and self.y + self.altura > inimigo.y
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

        if pyxel.btn(direita):
            self.x += self.velocidade

            if self.colisao(personagemB, inimigo):
                self.x -= self.velocidade

            if self.x > 160 - self.largura:
                self.x = 160 - self.largura

        if pyxel.btn(esquerda):
            self.x -= self.velocidade

            if self.colisao(personagemB, inimigo):
                self.x += self.velocidade

            if self.x < 0:
                self.x = 0

        if pyxel.btn(baixo):
            self.y += self.velocidade

            if self.colisao(personagemB, inimigo):
                self.y -= self.velocidade

            if self.y > 120 - self.altura:
                self.y = 120 - self.altura

        if pyxel.btn(cima):
            self.y -= self.velocidade

            if self.colisao(personagemB, inimigo):
                self.y += self.velocidade

            if self.y < 0:
                self.y = 0


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
        dano = massa*velocidade
        self.personagemA_x = personagemA.x
        self.personagemB_x = personagemB.x
        self.personagemA_y = personagemA.y
        self.personagemB_y = personagemB.y


    def desenhar(self):
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
        x_anterior = self.x
        y_anterior = self.y
        
        dx1 = personagemA.x - self.x
        dx2 = personagemB.x - self.x
        dy1 = personagemA.y - self.y
        dy2 = personagemB.y - self.y
       
        pitagoras1 = math.sqrt(dx1**2 + dy1**2)
        pitagoras2 = math.sqrt(dx2**2 + dy2**2)
       
        if pitagoras2 > pitagoras1:
           
           personagemA.set_cor(15)

           if personagemA.x > self.x:
                self.x += self.velocidade
           else:
                self.x -= self.velocidade
           if personagemA.y > self.y:
                self.y += self.velocidade
           else:
                self.y -= self.velocidade

        else:
           
           personagemB.set_cor(8)

           if personagemB.x > self.x:
                self.x += self.velocidade
           else:
                self.x -= self.velocidade
           if personagemB.y > self.y:
                self.y += self.velocidade
           else:
                self.y -= self.velocidade

        if self.colisao_i(
           personagemA,
           personagemB
        ):
            self.x = x_anterior
            self.y = y_anterior
            
class Jogo:

    def __init__(self):

        pyxel.init(160, 120)

        self.personagem1 = Personagem(
            20, 20, 10, 10, 5, 100, 5, 10)

        self.personagem2 = Personagem(
            20, 80, 10, 10, 6, 100, 5, 10)

        self.inimigo = Inimigo(
            80, 40, 10, 10, 8,30, 2, 5, self.personagem1, self.personagem2)

        pyxel.run(self.update, self.draw)

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

        
    def draw(self):

        pyxel.cls(0)

        self.personagem1.desenhar()
        self.personagem2.desenhar()
        self.inimigo.desenhar()


Jogo()