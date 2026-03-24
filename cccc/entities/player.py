"""Player"""
import pygame
from settings import PLAYER_SPEED, PLAYER_MAX_HEALTH


class Player(pygame.sprite.Sprite):
    """Player character"""

    def __init__(self, x, y, sprites):
        super().__init__()

        self.x = x
        self.y = y
        self.sprites = sprites

        self.image = sprites.get("idle")
        if not self.image:
            raise RuntimeError("[ERROR] Player sprites missing!")

        self.rect = self.image.get_rect(topleft=(int(x), int(y)))

        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.speed = PLAYER_SPEED

        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "down"

        self.coins = 0
        self.map_pieces = 0
        self.shards = 0

        self.attacking = False
        self.attack_timer = 0.0
        self.attack_duration = 0.15   # 0.15 seconds

        print(f"[PLAYER] Created at ({int(x)}, {int(y)})")

    def handle_input(self):
        keys = pygame.key.get_pressed()

        self.velocity_x = 0
        self.velocity_y = 0

        # movement should still work while attacking
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y = -self.speed
            self.direction = "up"
            if not self.attacking:
                self.image = self.sprites.get("walk_up", self.sprites["idle"])

        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y = self.speed
            self.direction = "down"
            if not self.attacking:
                self.image = self.sprites.get("walk_down", self.sprites["idle"])

        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.direction = "left"
            if not self.attacking:
                self.image = self.sprites.get("walk_left", self.sprites["idle"])

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.direction = "right"
            if not self.attacking:
                self.image = self.sprites.get("walk_right", self.sprites["idle"])

        else:
            if not self.attacking:
                self.image = self.sprites["idle"]

    def update(self, dt, lw, lh):
        self.handle_input()

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        self.x = max(0, min(self.x, lw - self.rect.width))
        self.y = max(0, min(self.y, lh - self.rect.height))

        self.rect.topleft = (int(self.x), int(self.y))

        if self.attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attacking = False
                self.attack_timer = 0
                self.image = self.sprites.get("idle", self.image)

    def attack(self):
        if self.attacking:
            return

        self.attacking = True
        self.attack_timer = self.attack_duration

        if self.direction == "up":
            self.image = self.sprites.get("attack_up", self.sprites.get("idle"))
        elif self.direction == "down":
            self.image = self.sprites.get("attack_down", self.sprites.get("idle"))
        elif self.direction == "left":
            self.image = self.sprites.get("attack_left", self.sprites.get("idle"))
        elif self.direction == "right":
            self.image = self.sprites.get("attack_right", self.sprites.get("idle"))

    def get_attack_rect(self):
        size = 40

        if self.direction == "up":
            return pygame.Rect(self.rect.centerx - 20, self.rect.top - size, size, size)
        elif self.direction == "down":
            return pygame.Rect(self.rect.centerx - 20, self.rect.bottom, size, size)
        elif self.direction == "left":
            return pygame.Rect(self.rect.left - size, self.rect.centery - 20, size, size)
        else:
            return pygame.Rect(self.rect.right, self.rect.centery - 20, size, size)

    def draw(self, screen, cam):
        dx = int(self.x - cam[0])
        dy = int(self.y - cam[1])

        screen.blit(self.image, (dx, dy))

        pygame.draw.rect(screen, (200, 0, 0), (dx, dy - 10, 64, 5))
        h_w = int(64 * (self.health / self.max_health))
        pygame.draw.rect(screen, (0, 200, 0), (dx, dy - 10, h_w, 5))

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health < 0:
            self.health = 0