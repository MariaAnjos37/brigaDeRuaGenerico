import pyxel
import math

class Personagem:

    #difinições dos atributos dos personagens
    def __init__(self, x, y, largura, altura, cor,vida, velocidade, massa, x_mapa, y_mapa, frame_parado=None, frame_movendo=None, frame_atacando=None, frame_pulando=None, frame_ataque_movendo=None, frame_ataque_pulando=None):
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
        self.velocidade_dano = 5
        self.esperar_atacar = 0
        self.frame_parado = frame_parado or []
        self.frame_movendo = frame_movendo or []
        self.frame_atacando = frame_atacando or []
        self.frame_pulando = frame_pulando or []
        self.frame_ataque_movendo = frame_ataque_movendo or []
        self.frame_ataque_pulando = frame_ataque_pulando or []
        if not self.frame_parado and self.frame_movendo:
            self.frame_parado = [self.frame_movendo[0]]
        self.animacao_anterior = None
        self.frame_atual = 0
        self.contador_animacao = 0
        self.intevalo_animacao = 6
        self.andando = False
        self.sentido = 1
        self.atacando = False
        self.contador_ataque_animacao = 0
        self.intervalo_ataque_animacao = 4
        
    #desenhar o personagem
    def desenhar(self):
        if self.vida <= 0:
            return
        nome, frames = self.obter_animacao()
        if not frames:
            return
        indice = self.frame_atual
        if indice >= len(frames):
            indice = len(frames) -1 
        x2, y2, largura_desenho, altura_desenho, dx, dy = frames[indice]
        if self.sentido == -1:
            largura_desenho = -largura_desenho
            x_desenho = self.x + dx + self.largura
        else:
            x_desenho= self.x + dx
        pyxel.blt(
            x_desenho,
            self.y + dy,
            1,#banco de imagens
            x2,#x banco de imagens
            y2,#y
            largura_desenho,
            altura_desenho,
            14
        )

    def obter_animacao(self):
        if self.atacando and not self.chao and self.frame_ataque_pulando:
                return "ataque_pulando", self.frame_ataque_pulando
        if self.atacando and self.andando and self.frame_ataque_movendo:
                return "atacando", self.frame_atacando
        if self.atacando and self.frame_atacando:
            return "atacando", self.frame_atacando
        if not self.chao and self.frame_pulando:
            return "pulando", self.frame_pulando
        if self.andando and self.frame_movendo:
            return "movendo", self.frame_movendo
        return "parado", self.frame_parado

    def animar(self):
        none,frames = self.obter_animacao()
        if not frames:
            self.frame_atual = 0
            self.contador_animacao = 0
            return
        if none != self.animacao_anterior:
            self.frame_atual = 0
            self.contador_animacao = 0
            self.contador_ataque_animacao = 0
            self.animacao_anterior = none
        if none in(
            "atacando",
            "ataque_movendo",
            "ataque_pulando"
        ):
            self.contador_ataque_animacao += 1
            if self.contador_ataque_animacao >= self.intervalo_ataque_animacao:
                self.contador_ataque_animacao = 0
                if self.frame_atual < len(frames) - 1:
                    self.frame_atual += 1
            else:
                self.atacando = False
                self.frame_atual = 0
                self.contador_animacao = 0
                self.animacao_anterior = None

            return

        if len(frames) > 1:
            self.contador_animacao += 1
            if self.contador_animacao >= self.intevalo_animacao:
                self.contador_animacao = 0
                self.frame_atual = (
                    self.frame_atual +1
                ) % len(frames)
            else:
                self.frame_atual = 0
                self.contador_animacao = 0

    def colisao(self, personagemB, inimigos):
       
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
        if colisao_B:
            return True
        
        for inimigo in inimigos:
            if inimigo.vida > 0:
                colisao_inimigo = (
                    self.x < inimigo.x + inimigo.largura #coodenada x do personagem < que o quadrado do outro
                    and
                    self.x + self.largura > inimigo.x #quadrado do personagem > que coodernada x do outro personagem
                    and
                    self.y < inimigo.y + inimigo.altura #coodenada y do personagem < que o quadrado do outro (y cresce para baixo)
                    and
                    self.y + self.altura > inimigo.y #quadrado do personagem > que coodernada y do outro personagem (y cresce para baixo)
            )
                if colisao_inimigo:
                    return True
        return False
    
    def colisao_alcance_ataque_personagem(self, inimigo):
            alcance = 5 #não tem como tacar dentro do inimigo, então tem que atacar antes

            return(
                inimigo.vida > 0 #para a colisao sumir apos o inimigo morrer
                and
                self.x  - alcance< inimigo.x + inimigo.largura #o alcance começa antes da coodenada x do personagem, lembrar que a coordena começa no centro dele  < que o quadrado do inimigo
                and 
                self.x + self.largura + alcance> inimigo.x #quadrado do personagem > que coodernada x do inimigo
                and 
                self.y - alcance < inimigo.y + inimigo.altura #o alcance começa antes da coodenada y do personagem, lembrar que a coordena começa no centro dele < que o quadrado do inimigo (y cresce para baixo)
                and 
                self.y + self.altura + alcance> inimigo.y #quadrado do personagem > que coodernada y do inimigo (y cresce para baixo)
        )


    def movimentacao(
        self,
        cima,
        baixo,
        esquerda,
        direita,
        personagemB,
        inimigo,
        camera_para_colisao   
    ):
        x_inicial = self.x
        y_inicial = self.y

        segundo_terceiro_y_original = self.y
        if pyxel.btn(direita):
            self.x += self.velocidade #caminha o equivalente a velocidade
            self.sentido = 1

            if self.colisao(personagemB, inimigo):# chamei a funcao colisao
                self.x -= self.velocidade #se a colisao for True, personagens não ocupam o mesmo espaço

            if self.x > self.x_mapa - self.largura:#fica dentro do espaço da tela
                self.x = self.x_mapa - self.largura

        if pyxel.btn(esquerda):
            self.x -= self.velocidade #caminha o equivalente a velocidade
            self.sentido = -1

            if self.colisao(personagemB, inimigo):# chamei a funcao colisao
                self.x += self.velocidade

            if self.x < 0: #fica dentro do espaço da tela
                self.x = 0

        if pyxel.btn(baixo) and self.chao:
            self.y += self.velocidade

            if self.colisao(personagemB, inimigo):
                self.y -= self.velocidade

            # quase certeza q dar de limitar y aqui, mas ta bugando
            if self.y > self.y_mapa - self.altura:
                self.y = self.y_mapa - self.altura

        if pyxel.btn(cima):
            self.y -= self.velocidade
            self.original_y = self.y

            if self.colisao(personagemB, inimigo):
                self.y += self.velocidade

            if self.y < 45:
                self.y = 45

            #colisao
        if self.x < camera_para_colisao:
            self.x = camera_para_colisao
        if self.x + self.largura > camera_para_colisao + 360:
            self.x = camera_para_colisao + 360 - self.largura

        self.andando = (
            self.x != x_inicial
            or
            self.y != y_inicial
        )
        if self.andando != getattr(self, "_andando_anterior", False):
            self.frame_atual = 0
            self.contador_animacao = 0
        self._andando_anterior = self.andando

    def combate(self, ataque,pulo, inimigos, personagemB, chefe):
        if self.esperar_atacar > 0:
            self.esperar_atacar -= 1
        if pyxel.btnp(ataque) and self.vida > 0 and self.esperar_atacar == 0:
            if self.frame_atacando:
                self.atacando = True
                self.frame_atual = 0
                self.contador_ataque_animacao = 0
                self.contador_animacao = 0
            for inimigo in inimigos:
                if inimigo.vida > 0 and self.colisao_alcance_ataque_personagem(inimigo):
                    inimigo.vida -= self.dano
                    self.esperar_atacar = self.velocidade_dano
            if chefe.vida > 0 and self.colisao_alcance_ataque_personagem(chefe):
                chefe.vida -= self.dano
                self.esperar_atacar = self.velocidade_dano
        if pyxel.btnp(pulo) and self.chao:
            self.chao = False
            self.original_y = self.y

        if not self.chao:
            #colisao tem q ser antes por prioridade
            if self.colisao(personagemB, inimigos):
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

    def __init__(self, x, y, largura, altura, cor, vida, velocidade, massa, desenho_x = 0, desenho_y = 0, frames_parado=None, frames_movendo=None, frames_atacando=None):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.vida = vida
        self.velocidade = velocidade
        self.massa = massa
        self.dano = massa*velocidade
        self.velocidade_dano = 17
        self.esperar_atacar = 0
        self.desenho_x = desenho_x
        self.desenho_y = desenho_y
        self.frames_parado = frames_parado or [
            (desenho_x, desenho_y, largura, altura)
        ]
        self.frames_movendo = frames_movendo or self.frames_parado
        self.frames_atacando = frames_atacando or self.frames_parado
        self.animacao = "parado"
        self.frame_atual = 0
        self.contador_animacao = 0
        self.intervalo_animacao = 6
        self.sentido = 1
        self.atacando = False

    def obter_frames(self):
        if self.atacando:
            return self.frames_atacando
        if self.animacao == "movendo":
            return self.frames_movendo
        return self.frames_parado
    
    def animar(self):
        frames = self.obter_frames()
        if not frames:
            return
        self.contador_animacao += 1
        if self.contador_animacao < self.intervalo_animacao:
            return
        self.contador_animacao = 0
        if self.atacando:
            if self.frame_atual < len(frames) - 1:
                self.frame_atual += 1
            else:
                self.atacando = False
                self.frame_atual = 0
        else:
            self.frame_atual = (
                self.frame_atual + 1
            ) % len(frames)
        

    def desenhar(self):
        if self.vida <= 0:
            return

        frames = self.obter_frames()
        if not frames:
            return

        indice = self.frame_atual
        if indice >= len(frames):
            indice = len(frames) - 1
        sx, sy, largura, altura = frames[indice]

        if self.sentido == -1:
            largura = -largura
            x_desenho = self.x + self.largura
        else:
            x_desenho = self.x

        pyxel.blt(
            x_desenho,
            self.y,
            1,#banco de imagens
            sx,#x banco de imagens
            sy,#y
            largura,
            altura,
            14
        )

    def colisao_i(self, personagemB, personagemA, inimigos):

        for personagem in (personagemA, personagemB):
            if personagem.vida > 0:
                if (
                    self.x < personagem.x + personagem.largura
                    and self.x + self.largura > personagem.x
                    and self.y < personagem.y + personagem.altura
                    and self.y + self.altura > personagem.y
                ):
                    return True

        for inimigo in inimigos:
            if inimigo is self or inimigo.vida <= 0:
                continue

            if (
                self.x < inimigo.x + inimigo.largura
                and self.x + self.largura > inimigo.x
                and self.y < inimigo.y + inimigo.altura
                and self.y + self.altura > inimigo.y
            ):
                return True

        return False
   
    def perseguir(self, personagemA, personagemB, inimigos):
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
        self.animacao = "movendo"
        if seguir.x > self.x:#Se personagem1 mais a direita
            self.x += self.velocidade
            self.sentido = 1
        else:#Se personagem1 mais a esquerda
            self.x -= self.velocidade
            self.sentido = -1

        if self.colisao_i(personagemA, personagemB, inimigos):
           self.x = x_anterior
        if seguir.y >self.y:
           self.y+= self.velocidade
        else:
           self.y -= self.velocidade
        if self.colisao_i(personagemA, personagemB, inimigos):
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
        if self.vida <= 0:
            return
        if self.esperar_atacar > 0:
            self.esperar_atacar -= 1
            return
        if(
            self.colisao_alcance_ataque_inimigo(personagemA)
            or
            self.colisao_alcance_ataque_inimigo(personagemB)
        ):
            self.atacando = True
            self.animacao = "atacando"
            self.frame_atual = 0
            self.contador_animacao = 0
            self.esperar_atacar = self.velocidade_dano
            if self.colisao_alcance_ataque_inimigo(personagemA):
                personagemA.vida -= self.dano

            if self.colisao_alcance_ataque_inimigo(personagemB):
                personagemB.vida -= self.dano
                #ele persegui o fantasma do ultimo player, só é um bug se eu não ignorar
class DoCao(Inimigo):
    def perseguir(self, personagemA, personagemB, inimigos, camera_x):
        if(
            self.vida > 0
            and
            self.x + self.largura > camera_x
            and
            self.x < camera_x + 360
        ):
            super().perseguir(
                personagemA,
                personagemB,
                inimigos
            )
class Jogo:

    def __init__(self):
        x_mapa = 1000
        y_mapa = 200
        pyxel.init(360, y_mapa)#tamanho da tela
        pyxel.load("my_resource.pyxres")#chamando a imagem
        pyxel.playm(0, loop=True) #musica
        self.camera_x = 0
        self.incremento_camera = 5
        self.continues = 13

        self.personagem1 = Personagem(
            20,#x,
            90, #y
            21, #largura
            26, #altura
            5, #cor
            100, #vida
            5, #velocidade
            10, #massa
            x_mapa, 
            y_mapa,
            
            frame_parado=[
                (0,0,21,26,0,0),
            ],
            frame_movendo=[
                (24, 0, 24, 26, 0, 0),
                (48, 0, 18, 27, 0, 0),
                (64, 0, 24, 26, 0, 0),
            ],
            
            frame_atacando=[
                (120,1,30,26,0,0),
                (152,2,21,26,0,0),
                (184,0,21,26,0,0),
            ],
            frame_pulando=[
                (95, 1, 25, 32, 0, 0),
            ],

            frame_ataque_movendo=[
                (152, 2, 21, 26, 0, 0),
                (184, 0, 21, 26, 0, 0),
                (184, 0, 21, 26, 0, 0),
            ],

            frame_ataque_pulando=[
                (0, 33, 30, 26, 0, 0),
            ])


        self.personagem2 = Personagem(
            20,#x,
            150, #y,
            21, #largura,
            35, #altura,
            6, #cor,
            100, #vida, 
            5, #velocidade,
            10,#massa
            x_mapa,
            y_mapa,
            
            frame_parado=[
                (32, 26, 21, 35, 0, 0),
            ],
            frame_movendo=[
                (56, 29, 24, 34, 0, 0),
                (80, 27, 17, 36, 0, 0),
                (96, 37, 24, 35, 0, 0),
            ],
            
            frame_atacando=[
                (152, 34, 30, 35, 0, 0),
                (184, 37, 21, 35, 0, 0),
                (216, 35, 21, 35, 0, 0),
            ],
            frame_pulando=[
                (120, 27, 26, 39, 0, 0),
            ],

            frame_ataque_movendo=[
                (120, 1, 30, 26, 0, 0),
                (152, 2, 21, 26, 0, 0),
                (184, 0, 21, 26, 0, 0),
            ],

            frame_ataque_pulando=[
                (32, 67, 25, 26, 0, 0),
            ])
                 
        posicoes_inimigos = [
            (70, 50),  (120, 50), (220, 50), (320, 50), (420, 50),
            (520, 50), (620, 50), (720, 50), (820, 50), (760, 50),

            (70, 200), (120, 200), (220, 200), (320, 200), (420, 200),
            (520, 200), (620, 200), (720, 200), (820, 200), (762, 200),
            ]

        self.inimigo = []
        for x,y in posicoes_inimigos:
            self.inimigo.append(
                Inimigo(
                x,
                y,
                30, #largura,
                21, #altura,
                8,#cor,
                100, #vida,
                2, #velocidade,
                2,#massa 
                frames_parado=[
                    (64,77,30,21),
                ],  
                frames_movendo=[
                    (64, 77, 30, 21),
                    (96, 77, 32, 21),
                ],
                frames_atacando=[
                    (167, 77, 50, 21),
                ]
                ))
 

        self.chefe = DoCao(
            950, #x,
            100, #y,
            20, #largura,
            27, #altura,
            15,#cor,
            2500, #vida,
            4, #velocidade,
            4, #massa
            frames_parado=[
                (0, 112, 40, 35),
            ],

            frames_movendo=[
                (24, 113, 22, 30),
                (0, 112, 21, 30),
                (48, 113, 22, 30),
            ],
            frames_atacando=[
                (104, 113, 28, 35),
                (73, 113, 27, 35),
                (136, 113, 28, 35),
            ]
            )


        self.chefe.velocidade_dano = 4   

        self.game_over = False
        self.tempo_game_over = 0
        self.reiniciar()
        pyxel.run(self.update, self.draw)#dejeito nenhum ponha algo depois disso

    #não funciona como devia, mas se tirar nao abre o jogo, então a
    def reiniciar(self):
        """self.game_over = False
        self.tempo_game_over = 0"""""
        pass

    def camera_colisao(self):
        inimigo_tela = False
        for inimigo in self.inimigo:
            if inimigo.vida > 0:
                if (
                    inimigo.x + inimigo.largura > self.camera_x
                    and
                    inimigo.x < self.camera_x + 360
                ):
                    inimigo_tela = True
                    break
            if (
                self.chefe.vida > 0
                and self.chefe.x + self.chefe.largura > self.camera_x
                and self.chefe.x < self.camera_x + 360
            ):
                    inimigo_tela = True
        if inimigo_tela:
            pass
        else:
            if self.personagem1.vida > 0 and self.personagem2.vida > 0:
                lado_esquerdo_tela = self.personagem1.x
                lado_direito_tela = self.personagem1.x + self.personagem1.largura
                if self.personagem2.x < self.personagem1.x:
                    lado_esquerdo_tela = self.personagem2.x
                else:
                    lado_direito_tela = self.personagem2.x + self.personagem2.largura
                centro_tela_ambos_vivos = (
                    lado_esquerdo_tela + lado_direito_tela
                ) / 2
                centro_tela_ambos_vivos2 = centro_tela_ambos_vivos - 180
                if self.camera_x < centro_tela_ambos_vivos2:
                    self.camera_x += self.incremento_camera
                    if self.camera_x > centro_tela_ambos_vivos2:
                        self.camera_x = centro_tela_ambos_vivos2
                if self.camera_x > centro_tela_ambos_vivos2:
                    self.camera_x -= self.incremento_camera
                    if self.camera_x < centro_tela_ambos_vivos2:
                        self.camera_x = centro_tela_ambos_vivos2
            elif self.personagem1.vida > 0:
                centro_tela_personagem1 = self.personagem1.x - 180
                if self.camera_x < centro_tela_personagem1:
                    self.camera_x += self.incremento_camera
                    if self.camera_x > centro_tela_personagem1:
                        self.camera_x = centro_tela_personagem1
                if self.camera_x > centro_tela_personagem1:
                    self.camera_x -= self.incremento_camera
                    if self.camera_x < centro_tela_personagem1:
                        self.camera_x = centro_tela_personagem1
            elif self.personagem2.vida > 0:
                centro_tela_personagem2 = self.personagem2.x - 180
                if self.camera_x < centro_tela_personagem2:
                    self.camera_x += self.incremento_camera
                    if self.camera_x > centro_tela_personagem2:
                        self.camera_x = centro_tela_personagem2
                if self.camera_x > centro_tela_personagem2:
                    self.camera_x -= self.incremento_camera
                    if self.camera_x < centro_tela_personagem2:
                        self.camera_x = centro_tela_personagem2
        if self.camera_x < 0:
            self.camera_x = 0
        if self.camera_x > 640:
            self.camera_x = 640
    def reviver(self):
            if self.personagem1.vida <=0:
                if self.continues > 0:
                    self.continues -= 1
                    self.personagem1.vida = 100
                    self.personagem1.x = self.camera_x+50
                    self.personagem1.y = 60
                    self.personagem1.chao = True
                    self.personagem1.original_y = self.personagem1.y
                    self.personagem1.esperar_atacar = 0
            if self.personagem2.vida <=0:
                if self.continues > 0:
                    self.continues -= 1
                    self.personagem2.vida = 100
                    self.personagem2.x = self.camera_x+70
                    self.personagem2.y = 100
                    self.personagem2.chao = True
                    self.personagem2.original_y = self.personagem2.y
                    self.personagem2.esperar_atacar = 0

    def update(self):
        if self.personagem1.vida <= 0 and self.personagem2.vida <= 0:
            if not self.game_over:
                self.game_over = True
                self.tempo_game_over = pyxel.frame_count

            if pyxel.frame_count - self.tempo_game_over >= 300:
                self.reiniciar()

            return


        self.camera_colisao()#tem q ser antes da movimentação se n a camera n anda
        # Personagem 1 - WASD
        self.personagem1.movimentacao(
            pyxel.KEY_W,
            pyxel.KEY_S,
            pyxel.KEY_A,
            pyxel.KEY_D,
            self.personagem2,
            self.inimigo,
            self.camera_x
        )

        # Personagem 2 - Setas
        self.personagem2.movimentacao(
            pyxel.KEY_UP,
            pyxel.KEY_DOWN,
            pyxel.KEY_LEFT,
            pyxel.KEY_RIGHT,
            self.personagem1,
            self.inimigo,
            self.camera_x
        )

        self.personagem1.animar()
        self.personagem2.animar()

        for inimigo in self.inimigo:
            if (
                inimigo.vida > 0
                and
                inimigo.x + inimigo.largura > self.camera_x
                and
                inimigo.x < self.camera_x + 420# 360 da tela and 60 fora dela
            ):
                inimigo.perseguir(
                    self.personagem1,
                    self.personagem2,
                    self.inimigo
                )
                inimigo.animar()
        self.chefe.perseguir(
            self.personagem1,
            self.personagem2,
            self.inimigo,
            self.camera_x
        )
        self.chefe.animar()

        self.personagem1.combate (
            pyxel.KEY_J,
            pyxel.KEY_K,
            self.inimigo,
            self.personagem2,
            self.chefe
        )

        self.personagem2.combate(
            pyxel.KEY_KP_1,
            pyxel.KEY_KP_2,
            self.inimigo,
            self.personagem1,
            self.chefe
        )

        for inimigo in self.inimigo:
            inimigo.combate(
                self.personagem1,
                self.personagem2
            )
        self.chefe.combate(
            self.personagem1,
            self.personagem2
        )

        self.reviver()        
    
       
    def draw(self):
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
        100 #altura que sera desenhada
    )
    
        self.personagem1.desenhar()
        self.personagem2.desenhar()
        for inimigo in self.inimigo:
            inimigo.desenhar()
        
        self.chefe.desenhar()
        pyxel.camera()

        pyxel.rect(0, 0, 360, 30, 0)

        b = f"VIDA P1: {self.personagem1.vida}"
        pyxel.text(20, 10, b, 15)

        a = f"VIDA P2: {self.personagem2.vida}"
        pyxel.text(140, 10, a, 15)

        pyxel.text(260, 10, f"CONTINUES: {self.continues}", 10)

        if self.chefe.vida <= 0:
            mensagem = "VOCE VENCEU!"

            imagem = pyxel.Image(64, 8)
            imagem.cls(0)
            imagem.text(0, 0, mensagem, 10)

            x_texto = (360 - 64 * 3) // 2
            y_texto = 85

            for px in range(64):
                for py in range(8):
                    if imagem.pget(px, py) == 10:
                        pyxel.rect(
                            x_texto + px * 3,
                            y_texto + py * 5,
                            3,
                            5,
                            10
                        )

        if self.game_over:
            mensagem = "GAME OVER"
            imagem = pyxel.Image(64, 8)
            imagem.cls(0)
            imagem.text(0, 0, mensagem, 10)

            x_texto = (360 - 64 * 3) // 2
            y_texto = 85

            for px in range(64):
                for py in range(8):
                    if imagem.pget(px, py) == 10:
                        pyxel.rect(
                            x_texto + px * 3,
                            y_texto + py * 5,
                            3,
                            5,
                            10)

Jogo()
