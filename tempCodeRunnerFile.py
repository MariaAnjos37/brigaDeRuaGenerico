    if self.colisao_alcance_ataque_inimigo(personagemA):
            alvo = personagemA
        elif self.colisao_alcance_ataque_inimigo(personagemB):
            alvo = personagemB

        if alvo is not None:
            self.atacando = True
            self.animacao = "atacando"
            self.frame_atual = 0
            self.contador_animacao = 0
            self.esperar_atacar = self.velocidade_dano
            alvo.vida -= self.dano