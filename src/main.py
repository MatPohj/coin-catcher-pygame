import pygame
from random import randint

class Robo:
    def __init__(self, image_path, x, y, speed):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y
        self.speed = speed
        self.moving_left = False
        self.moving_right = False

    def move(self):
        if self.moving_right and self.x + self.image.get_width() < 640:
            self.x += self.speed
        if self.moving_left and self.x > 0:
            self.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Kolikko:
    def __init__(self, image_path, speed):
        self.image = pygame.image.load(image_path)
        self.x = randint(0, 640 - self.image.get_width())
        self.y = randint(-480, 0)
        self.speed = speed

    def update(self):
        self.y += self.speed
        if self.y > 480:
            self.y = randint(-480, 0)
            self.x = randint(0, 640 - self.image.get_width())

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

def main():
    pygame.init()
    naytto = pygame.display.set_mode((640, 480))
    kello = pygame.time.Clock()

    robo = Robo("robo.png", 300, 480 - pygame.image.load("robo.png").get_height(), 5)
                    # kuva, koordinaatit, nopeus
    kolikot = [Kolikko("kolikko.png", 2) for _ in range(3)] #kolikoiden nopeus() ja kuinka monta() 
    #Näppäimistö
    while True:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    robo.moving_left = True
                if tapahtuma.key == pygame.K_RIGHT:
                    robo.moving_right = True

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    robo.moving_left = False
                if tapahtuma.key == pygame.K_RIGHT:
                    robo.moving_right = False

            if tapahtuma.type == pygame.QUIT:
                exit()

        robo.move()

        for kolikko in kolikot:
            kolikko.update()

        naytto.fill((0, 0, 0))
        robo.draw(naytto)
        for kolikko in kolikot:
            kolikko.draw(naytto)
            # pistelaskuri
            
            if not hasattr(main, "score"):
                main.score = 0
            if not hasattr(main, "font"):
                main.font = pygame.font.Font(None, 20)
            if not hasattr(main, "game_over_font"):
                main.game_over_font = pygame.font.Font(None, 40)

            # kolikkojen mekanismi ja pelin lopetus
            for k in kolikot:
                # kolikkojen tiputus+laskuri
                if (k.x + k.image.get_width() > robo.x and
                    k.x < robo.x + robo.image.get_width() and
                    k.y + k.image.get_height() > robo.y and
                    k.y < robo.y + robo.image.get_height()):
                    main.score += 1
                    k.y = randint(-480, 0)
                    k.x = randint(0, 640 - k.image.get_width())
                # pelin lopetus
                elif k.y + k.image.get_height() >= 480:
                    text = main.game_over_font.render(f"Peli loppui sait {main.score} pistettä", True, (255, 0, 0))
                    naytto.blit(text, (40, 150))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    exit()

            # pistelaskuri
            score_surf = main.font.render(str(main.score), True, (255, 255, 255))
            naytto.blit(score_surf, (560, 10))
        pygame.display.flip()

        kello.tick(60)

if __name__ == "__main__":
    main()