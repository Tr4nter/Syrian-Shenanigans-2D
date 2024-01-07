
from Beings.Instances import Instance

class Projectile(Instance):
    def __init__(self, image: str, x, y, screen, dx, dy, maxDistance):
        super().__init__(image, x, y, screen)
        self.dx = dx
        self.dy = dy
        self.maxDistance = maxDistance




