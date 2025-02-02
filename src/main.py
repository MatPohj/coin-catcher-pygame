import pygame, sys
from random import randint

pygame.init()

WIDTH, HEIGHT = 640, 480
naytto = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Catcher Game")
kello = pygame.time.Clock()

score = 0
font = pygame.font.Font(None, 20)
game_over_font = pygame.font.Font(None, 40)

# Load images. If not working try putting src\\ in front of the imagepath   robo_image = pygame.image.load("src\\robo.png")
robo_image = pygame.image.load("robo.png")
coin_image = pygame.image.load("kolikko.png")
monster_image = pygame.image.load("hirvio.png")

class Robo:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

class Coin:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

class Monster:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)

monster_spawn_delay = 3000  # milliseconds
last_monster_spawn_time = pygame.time.get_ticks()

def game_over_screen(score, cause):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        naytto.fill((255, 255, 255))
        
        if cause == "monster":
            game_over_text = game_over_font.render("Game Over! You caught a monster.", True, (255, 0, 0))
        elif cause == "coin":
            game_over_text = game_over_font.render("Game Over! You missed a coin.", True, (255, 0, 0))
        score_text = game_over_font.render(f"You got {score} coins", True, (255, 0, 0))
        restart_text = font.render("Press R to restart", True, (0, 0, 0))
        quit_text = font.render("Press Q to quit", True, (0, 0, 0))
        
        naytto.blit(game_over_text, (40, 100))
        naytto.blit(score_text, (40, 150))
        naytto.blit(restart_text, (40, 200))
        naytto.blit(quit_text, (40, 250))
        pygame.display.flip()
        kello.tick(60)

def main():
    global score, last_monster_spawn_time
    score = 29
    # Initialize game objects.
    robo = Robo(WIDTH // 2, HEIGHT - robo_image.get_height() - 10, robo_image)
    kolikot = [Coin(randint(0, WIDTH - coin_image.get_width()), randint(-480, 0), coin_image) for _ in range(2)]
    hirviot = [Monster(randint(0, WIDTH - monster_image.get_width()), randint(-480, 0), monster_image)]
    last_monster_spawn_time = pygame.time.get_ticks() 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the robot with arrow keys.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            robo.x -= 6
        if keys[pygame.K_RIGHT]:
            robo.x += 6
        robo.update_rect()
        
        #code for out of bound (OB) logic
        outofob=0
        #Cannot go OB
        if outofob==0:
            if robo.x>WIDTH-robo.image.get_width():
                robo.x=WIDTH-robo.image.get_width()
            if robo.x<0:
                robo.x=0
        ##this makes the robot switch sides when fully OB
        if outofob==1:
            if robo.x>WIDTH: 
                robo.x=0
            if robo.x<-40: 
                robo.x=WIDTH-robo_image.get_width()
        
        #this makes the robot switch sides when going even a little bit OB
        if outofob==2:
            if robo.x>WIDTH-robo_image.get_width():
                robo.x=1
            if robo.x<0:
                robo.x=WIDTH-robo_image.get_width()
        
        #backround color
        naytto.fill((255, 255, 255))
        
        ##makes game harder when above x score
        if score>30:
            naytto.fill((0,0,0))
        score_surface = font.render(f"Score {str(score)}", True, (255, 0, 0))
        naytto.blit(score_surface, (560, 30))
    
        # Process coins.
        for coin in kolikot:
            coin.y += 2  # Coin fall speed.
            coin.update_rect()
            # End game if coin falls past the bottom.
            if coin.y + coin.image.get_height() >= HEIGHT:
                if game_over_screen(score, "coin"):
                    main()
                return
            # Collision with the robot collects coin.
            if robo.rect.colliderect(coin.rect):
                score += 1
                coin.y = randint(-480, 0)
                coin.x = randint(0, WIDTH - coin_image.get_width())
                coin.update_rect()
            coin.draw(naytto)

        # Process monsters.
        current_time = pygame.time.get_ticks()
        if hirviot:
            for monster in hirviot[:]:
                monster.y += 4  # Monster fall speed.
                monster.update_rect()
                monster.draw(naytto)
                if robo.rect.colliderect(monster.rect):
                    if game_over_screen(score, "monster"):
                        main()  # Restart the game.
                    return
                if monster.y > HEIGHT:
                    hirviot.remove(monster)
                    last_monster_spawn_time = current_time
        else:
            if current_time - last_monster_spawn_time >= monster_spawn_delay:
                x = randint(0, WIDTH - monster_image.get_width())
                y = randint(-480, 0)
                hirviot.append(Monster(x, y, monster_image))

        robo.draw(naytto)
        pygame.display.flip()
        kello.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
