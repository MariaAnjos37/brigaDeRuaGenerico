import pyxel
import math

class Personagem:

    #difinições dos atributos dos personagens
    def __init__(self, x, y, largura, altura, cor,vida, velocidade, massa, x_mapa, y_mapa):
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
        self.x_mapa = x_mapa
        self.y_mapa = y_mapa
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
    
    def colisao_alcance_ataque_personagem(self, inimigo):
            alcance = 5 #não tem como tacar dentro do inimigo, então tem que atacar antes

            return(
                inimigo.vida > 0 #para a colisao sumir apos o inimigo morrer
                and
                self.x  - alcance< inimigo.x + inimigo.largura #o alcance começa antes da coodenada x do personagem, lembrar que a coordena começa no centro dele  < que o quadrado do inimigo
                and self.x + self.largura + alcance> inimigo.x #quadrado do personagem > que coodernada x do inimigo
                and self.y - alcance < inimigo.y + inimigo.altura #o alcance começa antes da coodenada y do personagem, lembrar que a coordena começa no centro dele < que o quadrado do inimigo (y cresce para baixo)
                and self.y + self.altura + alcance> inimigo.y #quadrado do personagem > que coodernada y do inimigo (y cresce para baixo)
        )


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

            if self.x > self.x_mapa - self.largura:#fica dentro do espaço da tela
                self.x = self.x_mapa - self.largura

        if pyxel.btn(esquerda):
            self.x -= self.velocidade #caminha o equivalente a velocidade

            if self.colisao(personagemB, inimigo):# chamei a funcao colisao
                self.x += self.velocidade

            if self.x < 0: #fica dentro do espaço da tela
                self.x = 0

        if pyxel.btn(baixo) and self.chao:
            self.y += self.velocidade

            if self.colisao(personagemB, inimigo):
                self.y -= self.velocidade

            if self.y > self.y_mapa - self.altura:
                self.y = self.y_mapa - self.altura

        if pyxel.btn(cima):
            self.y -= self.velocidade
            self.original_y = self.y

            if self.colisao(personagemB, inimigo):
                self.y += self.velocidade

            if self.y < 0:
                self.y = 0

    def combate(self, ataque,pulo, Inimigo, personagemB):
        if Inimigo.vida > 0:
            if pyxel.btnp(ataque) and self.vida > 0:
                if self.colisao_alcance_ataque_personagem(Inimigo):
                    Inimigo.vida -= self.dano
        if pyxel.btnp(pulo) and self.chao:
            self.chao = False
            self.original_y = self.y

        if not self.chao:
            #colisao tem q ser antes por prioridade
            if self.colisao(personagemB, Inimigo):
                self.y += 1
                self.chao = True
            #se andar para cima ele cai
            if self.original_y - 10 < self.y:
                self.y -= 1
            else:
                self.chao = True
           
        else:
            if self.y < self.original_y:#erro esta aqui
                self.y += 1
               
           
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
        #salvar posições originais
        x_anterior = self.x
        y_anterior = self.y

        if self.vida <= 0:#sem isso tu continua sendo perseguida, mesmo se o inimigo morrer
            return
        
        if personagemB.vida <= 0:
            seguir = personagemA

        elif personagemA.vida <= 0:
            seguir = personagemB
       
        else:
           
        
            # "a" e "b" de pitagoras
            dx1 = personagemA.x - self.x
            dx2 = personagemB.x - self.x
            dy1 = personagemA.y - self.y
            dy2 = personagemB.y - self.y
        
            #pitagoras para indentificamos quem esta mais perto
            pitagoras1 = math.sqrt(dx1**2 + dy1**2)
            pitagoras2 = math.sqrt(dx2**2 + dy2**2)
        
            if (pitagoras2 > pitagoras1) :#True, persegue personagem1
                    seguir = personagemA
            else:
                    seguir = personagemB
            #personagemA.set_cor(15)

        if seguir.x > self.x:#Se personagem1 mais a direita
            self.x += self.velocidade
        else:#Se personagem1 mais a esquerda
            self.x -= self.velocidade
        if seguir.y > self.y:#Se personagem1 mais a baixo
            self.y += self.velocidade
        else:#Se personagem1 mais a cima
            self.y -= self.velocidade


        if self.colisao_i(personagemA, personagemB):
           self.x = x_anterior
           self.y = y_anterior

    def colisao_alcance_ataque_inimigo(self, personagem):
        alcance = 5 #não tem como tacar dentro do inimigo, então tem que atacar antes

        return (
                personagem.vida > 0
                and
                self.x - alcance< personagem.x + personagem.largura
                and
                self.x + self.largura + alcance> personagem.x
                and
                self.y - alcance < personagem.y + personagem.altura
                and
                self.y + self.altura + alcance> personagem.y
            )
    
    def combate(self, personagemA, personagemB):
        if self.vida > 0:
            if self.colisao_alcance_ataque_inimigo(personagemA):
                personagemA.vida -= self.dano 
            if self.colisao_alcance_ataque_inimigo(personagemB):
                personagemB.vida -= self.dano          
                #ele persegui o fantasma do ultimo player, só é um bug se eu não ignorar
class Jogo:

    def __init__(self):
        x_mapa = 1000
        y_mapa = 200
        pyxel.init(360, y_mapa)#tamanho da tela
        pyxel.load("my_resource.pyxres")#chamando a imagem
        self.camera_x = 0

        self.personagem1 = Personagem(
            20, 20, 10, 10, 5, 100, 5, 10, x_mapa, y_mapa)
            #x, y, largura, altura, cor,vida, velocidade, massa

        self.personagem2 = Personagem(
            20,#x,
            80, #y,
            10, #largura,
            10, #altura,
            6, #cor,
            100, #vida, 
            5, #velocidade,
            10,#massa
            x_mapa,
            y_mapa )
                 

        self.inimigo = Inimigo(
            80, 40, 10, 10, 8,100, 2, 2, self.personagem1, self.personagem2)
            #x, y, largura, altura, cor, vida, velocidade, massa, personagemA, personagemB

        pyxel.run(self.update, self.draw)#dejeito nenhum ponha algo depois disso

    def update(self):
        # Personagem 1 - WASD
        self.personagem1.movimentacao(
            pyxel.KEY_W,
            pyxel.KEY_S,
            pyxel.KEY_A,
            pyxel.KEY_D,
            self.personagem2,
            self.inimigo,
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

        self.personagem1.combate (
            pyxel.KEY_J,
            pyxel.KEY_K,
            self.inimigo,
            self.personagem2
        )

        self.personagem2.combate(
            pyxel.KEY_KP_1,
            pyxel.KEY_KP_2,
            self.inimigo,
            self.personagem1
        )

        self.inimigo.combate(
            self.personagem1,
            self.personagem2
        )
       
    def draw(self):
        inimigo_na_tela = (
            self.inimigo.x + self.inimigo.largura > self.camera_x
            and
            self.inimigo.x < self.camera_x+360
        )
        if inimigo_na_tela:
            pass
        else:
            if self.personagem1.vida > 0 and self.personagem2.vida > 0:
                lado_esquerdo_tela = self.personagem1.x
                lado_direito_tela = self.personagem1.x + self.personagem1.largura
                if self.personagem2.x < self.personagem1.x:
                    lado_esquerdo_tela = self.personagem2.x
                else:
                    lado_direito_tela = self.personagem2.x + self.personagem2.largura
                centro_tela_ambos_vivos = (lado_esquerdo_tela + lado_direito_tela) / 2 #media aritmetica
                self.camera_x = centro_tela_ambos_vivos - 180
            elif self.personagem1.vida > 0 :
                self.camera_x = self.personagem1.x - 180
            elif self.personagem2.vida > 0 :
                self.camera_x = self.personagem2.x - 180
        if self.camera_x < 0:
            self.camera_x = 0
        if self.camera_x > 640:
            self.camera_x = 640
        pyxel.camera(self.camera_x, 0)
        pyxel.cls(0)
        pyxel.bltm(
        0, #eixo x
        0, #eixo y
        0, #qual timelap
        0, #posiçao x no timelap
        0, #posiçao y no timelap
        1000, #largura que sera desenha 
        200, #largura que sera desenha 
        200 #altura que sera desenhada
    )
        self.personagem1.desenhar()
        self.personagem2.desenhar()
        self.inimigo.desenhar()
        s = f" {self.inimigo.vida:>4}"#int para string
        pyxel.text(50, 60, s, 7)#texto na tela, s tem que ser string

        b = f" {self.personagem1.vida:>4}"#int para string
        pyxel.text(50, 30, b, 7)#texto na tela, s tem que ser string

        a = f" {self.personagem2.vida:>4}"#int para string
        pyxel.text(10, 60, a, 7)#texto na tela, s tem que ser string
       

Jogo()
