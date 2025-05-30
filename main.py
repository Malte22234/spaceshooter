import pygame
import random
import sys
import math

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
MÖRK_BLÅ = (10, 10, 30)
GRÅ = (120, 120, 120)
ASTEROID_FÄRG = (130, 130, 130)
BLÅ = (70, 130, 180)

# Font
font = pygame.font.SysFont("Arial", 28)

# Spelklass för rymdskeppet
class Spelare:
    def __init__(self):
        self.bredd = 60
        self.höjd = 80
        self.x = 370
        self.y = 500
        self.hastighet = 5
        self.rekt = pygame.Rect(self.x, self.y, self.bredd, self.höjd)
        self.levande = True
        self.energi = 200
        self.jet_anim = 0

    def hantera_tangenter(self):
        tangenter = pygame.key.get_pressed()
        if tangenter[pygame.K_LEFT] and self.x > 0:
            self.x -= self.hastighet
        if tangenter[pygame.K_RIGHT] and self.x < SKÄRM_BREDD - self.bredd:
            self.x += self.hastighet
        self.rekt.topleft = (self.x, self.y)

    def rita(self):
        # Skapa yta för skeppet
        skepp_yta = pygame.Surface((self.bredd, self.höjd), pygame.SRCALPHA)

        # Kropp: triangulär bas (silvergrå)
        kropp_punkter = [
            (self.bredd // 2, 0),
            (0, self.höjd - 20),
            (self.bredd, self.höjd - 20)
        ]
        pygame.draw.polygon(skepp_yta, (180, 180, 200), kropp_punkter)

        # Cockpit
        cockpit_rect = pygame.Rect(self.bredd // 2 - 10, 10, 20, self.höjd - 40)
        pygame.draw.rect(skepp_yta, BLÅ, cockpit_rect, border_radius=8)

        # Vingar
        vänster_vinge = [
            (0, self.höjd - 20),
            (self.bredd // 4, self.höjd - 10),
            (self.bredd // 4, self.höjd)
        ]
        höger_vinge = [
            (self.bredd, self.höjd - 20),
            (self.bredd * 3 // 4, self.höjd - 10),
            (self.bredd * 3 // 4, self.höjd)
        ]
        pygame.draw.polygon(skepp_yta, (140, 140, 160), vänster_vinge)
        pygame.draw.polygon(skepp_yta, (140, 140, 160), höger_vinge)

        # Cockpit detaljer
        pygame.draw.ellipse(skepp_yta, (150, 200, 255, 180), (self.bredd//2 - 8, 15, 16, self.höjd - 50))
        pygame.draw.ellipse(skepp_yta, (220, 240, 255, 100), (self.bredd//2 - 6, 20, 10, self.höjd - 60))

        # Rita skeppet
        skärm.blit(skepp_yta, (self.x, self.y))

        # Jet-flamma animation
        self.jet_anim += 0.15
        puls = (math.sin(self.jet_anim) + 1) / 2
        jet_färg = (255, int(150 + 105 * puls), 0)

        jet_bas_x = self.x + self.bredd // 2
        jet_bas_y = self.y + self.höjd

        flam_punkter = [
            (jet_bas_x - 10, jet_bas_y),
            (jet_bas_x, jet_bas_y + 20 + int(10 * puls)),
            (jet_bas_x + 10, jet_bas_y)
        ]
        pygame.draw.polygon(skärm, jet_färg, flam_punkter)

# Skott klass
class Skott:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hastighet = 10
        self.bredd = 6
        self.höjd = 12
        self.rekt = pygame.Rect(self.x, self.y, self.bredd, self.höjd)

    def uppdatera(self):
        self.y -= self.hastighet
        self.rekt.topleft = (self.x, self.y)

    def rita(self):
        pygame.draw.rect(skärm, (255, 255, 0), self.rekt)

# Asteroid klass
class Asteroid:
    def __init__(self):
        self.storlek = random.randint(30, 50)
        self.x = random.randint(0, SKÄRM_BREDD - self.storlek)
        self.y = -self.storlek
        self.hastighet = random.uniform(2, 5)
        self.rekt = pygame.Rect(self.x, self.y, self.storlek, self.storlek)

    def uppdatera(self):
        self.y += self.hastighet
        self.rekt.topleft = (self.x, self.y)

    def rita(self):
        pygame.draw.circle(skärm, ASTEROID_FÄRG, (self.x + self.storlek//2, self.y + self.storlek//2), self.storlek//2)
        detalj_färger = [(100, 100, 100), (150, 150, 150), (90, 90, 90)]
        for _ in range(6):
            dx = random.randint(-self.storlek//3, self.storlek//3)
            dy = random.randint(-self.storlek//3, self.storlek//3)
            radie = random.randint(3, 7)
            färg = random.choice(detalj_färger)
            cx = self.x + self.storlek//2 + dx
            cy = self.y + self.storlek//2 + dy
            pygame.draw.circle(skärm, färg, (cx, cy), radie)

# Rita poäng på skärmen
def rita_poäng():
    text = font.render(f"Poäng: {poäng}", True, VIT)
    skärm.blit(text, (10, 10))

# Rita energi-stapeln
def rita_energi(spelare):
    pygame.draw.rect(skärm, RÖD, (10, 50, 200, 20))
    pygame.draw.rect(skärm, GRÖN, (10, 50, spelare.energi, 20))

# Rymdbakgrund med stjärnor
def rita_rymdbakgrund():
    skärm.fill(MÖRK_BLÅ)
    for _ in range(50):
        x = random.randint(0, SKÄRM_BREDD)
        y = random.randint(0, SKÄRM_HÖJD)
        pygame.draw.circle(skärm, VIT, (x, y), 1)

# Startskärm
def startskärm():
    skärm.fill(MÖRK_BLÅ)
    titel = font.render("Spaceshooter", True, VIT)
    instruktion = font.render("Tryck på SPACE för att starta", True, VIT)
    skärm.blit(titel, (SKÄRM_BREDD//2 - titel.get_width()//2, SKÄRM_HÖJD//3))
    skärm.blit(instruktion, (SKÄRM_BREDD//2 - instruktion.get_width()//2, SKÄRM_HÖJD//2))
    pygame.display.flip()

# Huvudprogram

# Variabler
spelare = Spelare()
skott_lista = []
asteroider = []
asteroid_timer = 0
skott_timer = 0
poäng = 0
mål_poäng = 20  # Poäng för att vinna

spelar_startat = False
kör = True

while kör:
    if not spelar_startat:
        startskärm()
        for händelse in pygame.event.get():
            if händelse.type == pygame.QUIT:
                kör = False
            elif händelse.type == pygame.KEYDOWN:
                if händelse.key == pygame.K_SPACE:
                    spelar_startat = True
                    # Initiera variabler för nytt spel
                    spelare = Spelare()
                    skott_lista = []
                    asteroider = []
                    asteroid_timer = 0
                    skott_timer = 0
                    poäng = 0
        continue

    klocka.tick(FPS)

    for händelse in pygame.event.get():
        if händelse.type == pygame.QUIT:
            kör = False

    # Hantera tangenttryckningar (vänster/höger)
    spelare.hantera_tangenter()

    # Skott generering med cooldown
    skott_timer += 1
    tangenter = pygame.key.get_pressed()
    if tangenter[pygame.K_SPACE] and skott_timer > 15:
        # Skapa nytt skott i mitten på toppen av skeppet
        nytt_skott = Skott(spelare.x + spelare.bredd//2 - 3, spelare.y)
        skott_lista.append(nytt_skott)
        skott_timer = 0

    # Skapa nya asteroider med viss frekvens
    asteroid_timer += 1
    if asteroid_timer > 30:
        asteroid_timer = 0
        asteroider.append(Asteroid())

    # Uppdatera skott och ta bort de som lämnat skärmen
    for skott in skott_lista[:]:
        skott.uppdatera()
        if skott.y < -skott.höjd:
            skott_lista.remove(skott)

    # Uppdatera asteroider och ta bort de som lämnat skärmen
    for asteroid in asteroider[:]:
        asteroid.uppdatera()
        if asteroid.y > SKÄRM_HÖJD:
            asteroider.remove(asteroid)

    # Kollision: skott mot asteroid
    for asteroid in asteroider[:]:
        for skott in skott_lista[:]:
            if asteroid.rekt.colliderect(skott.rekt):
                asteroider.remove(asteroid)
                skott_lista.remove(skott)
                poäng += 1
                break

    # Kollision: asteroid mot spelare
    for asteroid in asteroider[:]:
        if asteroid.rekt.colliderect(spelare.rekt):
            asteroider.remove(asteroid)
            spelare.energi -= 30
            if spelare.energi <= 0:
                spelare.levande = False

    # Rita bakgrund och spelobjekt
    rita_rymdbakgrund()
    spelare.rita()
    for skott in skott_lista:
        skott.rita()
    for asteroid in asteroider:
        asteroid.rita()
    rita_poäng()
    rita_energi(spelare)

    # Kontrollera Game Over
    if not spelare.levande:
        text = font.render("GAME OVER! Tryck R för att starta om", True, RÖD)
        skärm.blit(text, (SKÄRM_BREDD//2 - text.get_width()//2, SKÄRM_HÖJD//2))
        pygame.display.flip()

        # Vänta på R för restart eller Q för quit
        väntar = True
        while väntar:
            for händelse in pygame.event.get():
                if händelse.type == pygame.QUIT:
                    väntar = False
                    kör = False
                elif händelse.type == pygame.KEYDOWN:
                    if händelse.key == pygame.K_r:
                        # Starta om spelet
                        spelar_startat = False
                        väntar = False
                    elif händelse.key == pygame.K_q:
                        väntar = False
                        kör = False
        continue

    # Kontrollera om spelaren vunnit
    if poäng >= mål_poäng:
        text = font.render("GRATTIS! Du vann! Tryck R för att spela igen", True, GRÖN)
        skärm.blit(text, (SKÄRM_BREDD//2 - text.get_width()//2, SKÄRM_HÖJD//2))
        pygame.display.flip()

        väntar = True
        while väntar:
            for händelse in pygame.event.get():
                if händelse.type == pygame.QUIT:
                    väntar = False
                    kör = False
                elif händelse.type == pygame.KEYDOWN:
                    if händelse.key == pygame.K_r:
                        spelar_startat = False
                        väntar = False
                    elif händelse.key == pygame.K_q:
                        väntar = False
                        kör = False
        continue

    pygame.display.flip()

pygame.quit()
sys.exit()
