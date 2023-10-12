import pygame
import random

# Alustetaan Pygame
pygame.init()
pygame.mixer.init()  # Alusta äänentoisto
pygame.mixer.music.load('sounds/level1.ogg')  # Lataa musiikkitiedosto
pygame.mixer.music.play(-1)  # Soita musiikkia jatkuvasti

# Näytön leveys ja korkeus
leveys = 800
korkeus = 600

# Pelin päivitysnopeus (FPS)
pelin_nopeus = 144
kello = pygame.time.Clock()

# Luo pelinäyttö
naytto = pygame.display.set_mode((leveys, korkeus))
pygame.display.set_caption("Väistelypeli")

# Taustakuvan lataus ja skaalaus
taustakuva = pygame.image.load('images/taustakuva.png')
taustakuva = pygame.transform.scale(taustakuva, (leveys, korkeus))

# Taustakuvan alkuperäinen sijainti
taustakuva_x = 0
taustakuva_y = 0

# Taustakuvan liikkumisen nopeus
taustakuva_nopeus = 1

# Taustakuvien määrä
taustakuva_maara = 3

# Luo lista taustakuvista
taustakuvat = [taustakuva.copy() for _ in range(taustakuva_maara)]

# Alkuperäiset taustakuvien y-koordinaatit
taustakuvien_y = [-korkeus * i for i in range(taustakuva_maara)]

# Pelaajan hahmo
alkuperainen_pelaaja_kuva = pygame.image.load('images/ship.xcf')  # Lataa alkuperäinen pelaajan kuva
pelaaja_leveys = 100  # Haluttu pelaajan kuvan leveys
pelaaja_korkeus = 100  # Haluttu pelaajan kuvan korkeus

# Leikkaa pelaajan kuva haluttuun kokoiseksi
pelaaja_kuva = pygame.transform.scale(alkuperainen_pelaaja_kuva, (pelaaja_leveys, pelaaja_korkeus))

pelaaja_x = leveys // 2 - pelaaja_leveys // 2  # Määritä pelaajan x-koordinaatti ja koko
pelaaja_y = korkeus - pelaaja_korkeus
pelaaja_nopeus = 5  # Pelaajan nopeus

# Määritä pelaajan osumatunniste (collider)
pelaaja_collider = pygame.Rect(pelaaja_x, pelaaja_y, pelaaja_leveys - 50, pelaaja_korkeus - 50)

# Lisää kaksi estekuvaa
este_kuva1 = pygame.image.load('images/asteroid.png')
este_kuva2 = pygame.image.load('images/asteroid2.png')

# Määritä estetyypit
ESTE1 = 1
ESTE2 = 2

# Esteiden määrä
este_maara = 10

# Luo lista esteistä, joka sisältää estetyypin ja sijainnin
esteet = []

for _ in range(este_maara):
    este_leveys = random.randint(20, 150)
    este_korkeus = random.randint(20, 150)
    este_x = random.randint(0, leveys - este_leveys)
    este_y = random.randint(-korkeus, 0)
    este_nopeus = random.uniform(1, 3)
    este_tyyppi = random.choice([ESTE1, ESTE2])  # Arvotaan esteen tyyppi
    esteet.append((este_x, este_y, este_leveys, este_korkeus, este_nopeus, este_tyyppi))

# Pelin lopetus
lopetus = False
peli_kaynnissa = False  # Alustetaan peli_käynnissä muuttuja

# Pelaajan pisteet
pisteet = 0
# Ohitetut esteet
ohitetut_esteet = 0
# Pelin päivitysnopeus (FPS)
pelin_nopeus = 60
fontti = pygame.font.Font(pygame.font.get_default_font(), 36)

# Alkuvalikon fontti
alkuvalikon_fontti = pygame.font.Font(pygame.font.get_default_font(), 64)
alkuvalikon_teksti = alkuvalikon_fontti.render("Paina SPACE aloittaaksesi", True, (255, 255, 255))
alkuvalikon_x = leveys // 2 - alkuvalikon_teksti.get_width() // 2
alkuvalikon_y = korkeus // 2 - alkuvalikon_teksti.get_height() // 2







# Pelisilmukka
while not lopetus:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lopetus = True

    naytto.fill((0, 0, 0))  # Musta tausta

    if not peli_kaynnissa:
        naytto.blit(alkuvalikon_teksti, (alkuvalikon_x, alkuvalikon_y))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            peli_kaynnissa = True
    else:

        naytto.fill((0, 0, 0))  # Musta tausta

    # Päivitä taustakuvien sijainteja ylhäältä alas liikkumiseen
    for i in range(taustakuva_maara):
        taustakuvien_y[i] += taustakuva_nopeus

        # Jos taustakuva menee pois näytöltä, aseta se takaisin alkuperäiseen sijaintiin
        if taustakuvien_y[i] >= korkeus:
            taustakuvien_y[i] = -korkeus

               # Piirrä taustakuvat
        naytto.blit(taustakuvat[i], (taustakuva_x, taustakuvien_y[i]))

    # Piirrä pelaaja
    naytto.blit(pelaaja_kuva, (pelaaja_x, pelaaja_y))  # Piirrä pelaajan kuva
    
    # Päivitä pistenäyttö
    pisteteksti = fontti.render(f"Evaded asteroids: {pisteet}", True, (255, 255, 255))
    naytto.blit(pisteteksti, (10, 10))
    
    # Liikuta pelaajahahmoa
    näppäimet = pygame.key.get_pressed()

    # Pelaaja liikkuu vasemmalle
    if näppäimet[pygame.K_LEFT] and pelaaja_x > 0:
        pelaaja_x -= pelaaja_nopeus

    # Pelaaja liikkuu oikealle
    if näppäimet[pygame.K_RIGHT] and pelaaja_x < leveys - 20:
        pelaaja_x += pelaaja_nopeus

    # Pelaaja liikkuu ylös
    if näppäimet[pygame.K_UP] and pelaaja_y > 0:
        pelaaja_y -= pelaaja_nopeus

    # Pelaaja liikkuu alas
    if näppäimet[pygame.K_DOWN] and pelaaja_y < korkeus - 20:
        pelaaja_y += pelaaja_nopeus

    # Tarkista törmäykset pelaajan ja esteiden välillä
    pelaaja_rect = pygame.Rect(pelaaja_x, pelaaja_y, pelaaja_leveys -50, pelaaja_korkeus -50)
    for i in range(este_maara):
        este_x, este_y, este_leveys, este_korkeus, este_nopeus, este_tyyppi = esteet[i]
        este_y += este_nopeus

        este_rect = pygame.Rect(este_x, este_y, este_leveys -100, este_korkeus -100)

        if pelaaja_rect.colliderect(este_rect):
            lopetus = True

        # Jos este menee pois näytöltä, asetetaan se uudelleen ylös ja arvotaan x-koordinaatti ja koko
        if este_y > korkeus:
            este_leveys = random.randint(20, 150)
            este_korkeus = random.randint(20, 150)
            este_x = random.randint(0, leveys -50 - este_leveys -50)
            este_y = random.randint(-korkeus, 0)
            pisteet += 1
            este_tyyppi = random.choice([ESTE1, ESTE2])  # Arvotaan uusi esteen tyyppi
        esteet[i] = (este_x, este_y, este_leveys, este_korkeus, este_nopeus, este_tyyppi)

        # Piirrä esteet käyttämällä niiden tyyppiä ja skaalaa ne sopiviksi
        if este_tyyppi == ESTE1:
            naytto.blit(pygame.transform.scale(este_kuva1, (este_leveys, este_korkeus)), (este_x, este_y))
        elif este_tyyppi == ESTE2:
            naytto.blit(pygame.transform.scale(este_kuva2, (este_leveys, este_korkeus)), (este_x, este_y))

    # Tarkista, onko pelaaja ohittanut esteen
    for i in range(este_maara):
        este_x, este_y, este_leveys, este_korkeus, este_nopeus, este_tyyppi = esteet[i]
        if este_y > korkeus and esteet[i] is not None:
            ohitetut_esteet += 1  # Lisää yksi piste ohitetusta esteestä
            esteet[i] = None  # Merkitse este käsitellyksi, jotta sitä ei oteta huomioon uudestaan

    
    pygame.display.update()

    # Rajoita pelin päivitysnopeus
    kello.tick(pelin_nopeus)
# Lopputekstin fontti ja lopputekstin sijainti
lopputekstin_fontti = pygame.font.Font(None, 64)
lopputekstin = lopputekstin_fontti.render(f"Game Over! Pisteet: {pisteet}", True, (255, 255, 255))
lopputekstin_x = leveys // 2 - lopputekstin.get_width() // 2
lopputekstin_y = korkeus // 2 - lopputekstin.get_height() // 2

# Lisäteksti uudelleenaloitusta varten
uudelleenaloitusteksti_fontti = pygame.font.Font(None, 36)
uudelleenaloitusteksti = uudelleenaloitusteksti_fontti.render("Paina SPACE aloittaaksesi uudelleen", True, (255, 255, 255))
uudelleenaloitusteksti_x = leveys // 2 - uudelleenaloitusteksti.get_width() // 2
uudelleenaloitusteksti_y = lopputekstin_y + lopputekstin.get_height() + 20  # Lisää pystysuora väli

# Lopputekstin ja lisätekstin näyttäminen
naytto.blit(lopputekstin, (lopputekstin_x, lopputekstin_y))
naytto.blit(uudelleenaloitusteksti, (uudelleenaloitusteksti_x, uudelleenaloitusteksti_y))
pygame.display.update()

uudelleenaloitus = False
while not uudelleenaloitus:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            uudelleenaloitus = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            uudelleenaloitus = True

# Lopeta Pygame
pygame.quit()

