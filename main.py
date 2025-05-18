import pygame
import random
import sys

# Initiera Pygame
pygame.init()

# Skärmstorlek
SKÄRM_BREDD = 800
SKÄRM_HÖJD = 600
skärm = pygame.display.set_mode((SKÄRM_BREDD, SKÄRM_HÖJD))
pygame.display.set_caption("Spaceshooter")

# Klocka för FPS
klocka = pygame.time.Clock()
FPS = 60

# Färger
VIT = (255, 255, 255)
SVART = (0, 0, 0)
RÖD = (255, 0, 0)
GRÖN = (0, 255, 0)

# Ladda bilder
spelare_bild = pygame.image.load("assets/spaceship.png")
jet_bild = pygame.image.load("assets/jet.png")
skott_bild = pygame.image.load("assets/bullet.png")
asteroid_bild = pygame.image.load("assets/asteroid.png")
bakgrund_bild = pygame.image.load("assets/background.png")

# Ladda ljud
skott_ljud = pygame.mixer.Sound("assets/sounds/laser.wav")
explosion_ljud = pygame.mixer.Sound("assets/sounds/explosion.wav")
pygame.mixer.music.load("assets/music/theme.mp3")
pygame.mixer.music.play(-1)

# Spelklasser
class Spelare:
    def __init__(self):
        self.bild = spelare_bild
        self.jet = jet_bild
        self.x = 370
        self.y = 500
        self.hastighet = 5
        self.rekt = self.bild.get_rect(topleft=(self.x, self.y))
        self.levande = True
        self.energi = 200

    def hantera_tangenter(self):
        tangenter = pygame.key.get_pressed()
        if tangenter[pygame.K_LEFT] and self.x > 0:
            self.x -= self.hastighet
        if tangenter[pygame.K_RIGHT] and self.x < SKÄRM_BREDD - self.bild.get_width():
            self.x += self.hastighet
        self.rekt.topleft = (self.x, self.y)

    def rita(self):
        skärm.blit(self.jet, (self.x + 15, self.y + 40))
        skärm.blit(self.bild, (self.x, self.y))

class Skott:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hastighet = 10
        self.bild = skott_bild
        self.rekt = self.bild.get_rect(topleft=(x, y))

    def uppdatera(self):
        self.y -= self.hastighet
        self.rekt.topleft = (self.x, self.y)

    def rita(self):
        skärm.blit(self.bild, (self.x, self.y))

class Asteroid:
    def __init__(self):
        self.x = random.randint(0, SKÄRM_BREDD - 64)
        self.y = -64
        self.hastighet = random.randint(2, 6)
        self.bild = asteroid_bild
        self.rekt = self.bild.get_rect(topleft=(self.x, self.y))

    def uppdatera(self):
        self.y += self.hastighet
        self.rekt.topleft = (self.x, self.y)

    def rita(self):
        skärm.blit(self.bild, (self.x, self.y))

# Poäng och text
poäng = 0
font = pygame.font.SysFont("Arial", 28)

def rita_poäng():
    text = font.render(f"Poäng: {poäng}", True, VIT)
    skärm.blit(text, (10, 10))

def rita_energi(spelare):
    pygame.draw.rect(skärm, RÖD, (10, 50, 200, 20))
    pygame.draw.rect(skärm, GRÖN, (10, 50, spelare.energi, 20))

# Spelobjekt
spelare = Spelare()
skott_lista = []
asteroider = []
asteroid_timer = 0
skott_timer = 0

# Huvudloop
kör = True
while kör:
    skärm.blit(bakgrund_bild, (0, 0))

    for händelse in pygame.event.get():
        if händelse.type == pygame.QUIT:
            kör = False

    if spelare.levande:
        spelare.hantera_tangenter()

        # Hantera skott
        skott_timer += 1
        tangenter = pygame.key.get_pressed()
        if tangenter[pygame.K_SPACE] and skott_timer > 10:
            nytt_skott = Skott(spelare.x + 20, spelare.y)
            skott_lista.append(nytt_skott)
            skott_ljud.play()
            skott_timer = 0

        # Hantera asteroider
        asteroid_timer += 1
        if asteroid_timer > 30:
            asteroider.append(Asteroid())
            asteroid_timer = 0

        # Uppdatera och rita skott
        for skott in skott_lista[:]:
            skott.uppdatera()
            skott.rita()
            if skott.y < -10:
                skott_lista.remove(skott)

        # Uppdatera och rita asteroider
        for asteroid in asteroider[:]:
            asteroid.uppdatera()
            asteroid.rita()
            if asteroid.y > SKÄRM_HÖJD:
                asteroider.remove(asteroid)
            elif asteroid.rekt.colliderect(spelare.rekt):
                spelare.energi -= 40
                explosion_ljud.play()
                asteroider.remove(asteroid)
                if spelare.energi <= 0:
                    spelare.levande = False

            for skott in skott_lista[:]:
                if asteroid.rekt.colliderect(skott.rekt):
                    explosion_ljud.play()
                    skott_lista.remove(skott)
                    asteroider.remove(asteroid)
                    poäng += 1
                    break

        # Rita spelare och gränssnitt
        spelare.rita()
        rita_poäng()
        rita_energi(spelare)
    else:
        game_over = font.render("GAME OVER", True, VIT)
        skärm.blit(game_over, (SKÄRM_BREDD//2 - 100, SKÄRM_HÖJD//2 - 20))

    pygame.display.update()
    klocka.tick(FPS)

pygame.quit()
sys.exit()