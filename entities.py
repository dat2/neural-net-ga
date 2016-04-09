from collision import CollidableSprite
import numpy as np

class Tank:
    def __init__(self, x, y, r, smart):
        self.smart_sprite = CollidableSprite('images/tank_smart.png', 16, 16, 32)
        self.stupid_sprite = CollidableSprite('images/tank_stupid.png', 16, 16, 32)

        self.set_sprites(x,y,r)
        self.set_smart(smart)

        self.x = x
        self.y = y
        self.r = r
        self.speed = 0

    def rotate(self, r):
        self.set_sprites(self.x, self.y, self.r + r)

    def set_sprites(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r

        self.smart_sprite.position = x,y
        self.smart_sprite.rotation = r

        self.stupid_sprite.position = x,y
        self.stupid_sprite.rotation = r

    def set_smart(self, smart):
        self.smart = smart

        self.smart_sprite.opacity = 255 if self.smart else 0
        self.stupid_sprite.opacity = 0 if self.smart else 255

    def add_to_layer(self, layer):
        layer.add(self.stupid_sprite, z=2)
        layer.add(self.smart_sprite, z=2)

    def do(self, command):
        self.smart_sprite.do(command)
        self.stupid_sprite.do(command)

    def get_forward_vector(self):
        x = np.sin(np.radians(self.r))
        y = np.cos(np.radians(self.r))

        return x,y

class Mine:
    def __init__(self, x, y):
        self.sprite = CollidableSprite('images/mine.png', 16, 16, 32)
        self.sprite.position = x,y
        self.x = x
        self.y = y

    def add_to_layer(self, layer):
        layer.add(self.sprite, z=1)
