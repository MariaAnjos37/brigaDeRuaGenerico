if pyxel.btn(direita):
            self.x += 2

            if self.colisao(personagemB):
                self.x -= 2

            if self.x > 160 - self.largura:
                self.x = 160 - self.largura
