import cocos
import cocos.euclid as eu
import cocos.collision_model as cm

class CollidableSprite(cocos.sprite.Sprite):
    def __init__(self, image, center_x, center_y, radius):
        super(CollidableSprite, self).__init__(image)
        self.cshape = cm.CircleShape(eu.Vector2(center_x, center_y), radius)
