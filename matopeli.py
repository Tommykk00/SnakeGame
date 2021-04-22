# importataan pygame, jotta voidaan käyttää pygame kirjaston sisältöä hyväksi
import pygame
#importataan time, jotta voidaan säätää pelin fps:ää (kuva per sekunti)
import time
#importataan random, jotta voidaan randomisti generoida ruoan paikka
import sys, random
from pygame import mixer
pygame.mixer.init()

#Alustaa kaikki tuodut Pygame-moduulit (palauttaa dupleksin, joka osoittaa alustamisen onnistumisen ja epäonnistumisen)
pygame.init()

#luodaan fontti muuttuja, jossa määritellään fontti ja sen koko
font = pygame.font.SysFont('comicsans',40)

#luodaan väri muuttujia (R, G, B)
keltainen = (255, 255, 0)
musta = (0, 0, 0)
valkoinen = (255, 255, 255)

#luodaan piste_sound muuttuja, jossa on määritelty ääni, joka kuuluu aina kun saa pisteen eli aina kun mato syö ruoan
piste_sound = pygame.mixer.Sound("piste-sound.wav")
#luodaan gameover_sound muuttuja, jossa määritellään ääni, joka kuuluu aina kun peli päättyy eli esim. kun mato osuu seinään
gameover_sound = pygame.mixer.Sound("game-over-sound.wav")
#luodaan background_music muuttuja, jossa määritellään ääni, joka kuuluu kokoajan kun peliä pelataan
background_music = pygame.mixer.Sound("background-music.wav")

#määritellään muuttujat ruudun leveydelle ja pituudelle ja asetetaan ne 400. Ruutu on siis 400x400 pikseliä
ruutu_leveys = 400
ruutu_pituus = 400

#luodaan muuttuja koko, jossa on yhdistetty muuttujat ruutu_leveys ja ruutu_pituus
koko = (ruutu_leveys, ruutu_pituus)
#luodaan muuttuja ruutu, joka alustaa ruudun näkyviin
ruutu = pygame.display.set_mode(koko)
#luodaan muuttuja tausta, jossa määritellään pelin taustakuva
tausta = pygame.image.load("ruoho.png").convert()
#luodaan muuttuja peli_paattyy_tausta, jossa määritellään tausta, joka näkyy pelin päättyessä
peli_paattyy_tausta = pygame.image.load("peli-paattyy.png").convert()
#luodaan muuttuja main_menu_tausta, jossa määritellään tausta, joka näkyy ennen kuin peli alkaa
main_menu_tausta = pygame.image.load("main-menu.png").convert()

#asetetaan peliruudun yläpalkkiin "Matopeli"
pygame.display.set_caption("Matopeli")

#luodaan menu metodi
def menu():
    #luodaan loputon silmukka
    while 1:
        #tarkistetaan tapahtumia esim. näppäimen painallus
        for event in pygame.event.get():
            #jos käyttäjä painaa exit nappia (ruksi ohjelman oikeassa tai vasemmassa yläreunassa), ohjelma sulkeutuu
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #jos käyttäjä painaa hiirellä mistä tahansa ohjelmaa, peli alkaa (kutsutaan pelaa metodia)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pelaa()

        #asetetaan main_menu_tausta peliin
        ruutu.blit(main_menu_tausta, [0, 0])
        
        #luodaan menu_viesti muuttuja, joka luo menu ruudulle viestin "Klikkaa pelataksesi" valkoisella värillä
        menu_viesti = font.render('Klikkaa pelataksesi' , True , (255,255,255))
        
        #luodaan muuttuja menu_viesti_paikka, joka asettaa menu_viestin oikeaan kohtaan (keskelle ruutua)
        menu_viesti_paikka = menu_viesti.get_rect(center=(ruutu_leveys // 2, ruutu_pituus // 2))

        #asetetaan luodut muuttujat peliin
        ruutu.blit(menu_viesti, menu_viesti_paikka)
        #päivitettään ruutu
        pygame.display.update()


#luodaan pelaa metodi
def pelaa():
    #pelin fps (ruudun päivitys per sekuntti)
    fps = pygame.time.Clock() 

    #paikka mistä mato aloittaa pelin (x ja y-akseli)
    madon_paikka = [200, 70]
    #madon vartalo alussa kahden peräkkäisen neliön kokoinen
    madon_vartalo = [[200,70], [200-10,70]]
    #mato lähtee pelin alussa oikeaan suuntaan
    suunta = "oikea"

    #laitetaan taustamusiikki soimaan
    mixer.music.load('background-music.wav')
    #asetetaan taustamusiikin voimakkuus
    mixer.music.set_volume(0.2)
    #laitetaan musiikki looppaamaan
    mixer.music.play(-1)

    #asetetaan pisteet aluksi nollaan
    pisteet = 0

    #ruoan sijainti aluksi
    ruoka_sijainti=[0,0]
    ruoka = True

    #luodaan loputon silmukka
    while 1:
        #tarkistetaan tapahtumia esim. näppäimen painallus
        for event in pygame.event.get():
            #jos käyttäjä painaa exit nappia (ruksi ohjelman oikeassa tai vasemmassa yläreunassa), ohjelma sulkeutuu
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #tallennetaan näppäimen painallus muuttujaan keys
            keys = pygame.key.get_pressed()
            #seuraava osio vaihtaa muuttujan 'suunta' näppäimen painalluksen perusteella
            #jos painaa 'w' tai nuolta ylös, mato menee ylös
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and suunta != 'alas':
                suunta = 'ylos'
            #jos painaa 's' tai nuolta alas, mato menee alas
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and suunta != 'ylos':
                suunta = 'alas'
            #jos painaa 'd' tai nuolta oikealle, mato menee oikealle
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and suunta != 'vasen':
                suunta = 'oikea'
            #jos painaa 'a' tai nuolta vasemmalle, mato menee vasemmalle
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and suunta != 'oikea':
                suunta = 'vasen'

        #asetetaan tausta peliin
        ruutu.blit(tausta, [0, 0])

        """
        Piirretään mato
        Ensimmäinen argumentti määrää, mihin mato piirretään. Tässä tapauksessa ruudulle.
        Toinen argumentti määrää madon värin. Tässä tapauksessa se on keltainen.
        Kolman argumentti määrää mihin mato piirretään ensimmäisenä x-akseli, toisena y-akseli, kolmantena leveys ja neljäntenä pituus.
        """
        for neliö in madon_vartalo:
            pygame.draw.rect(ruutu ,(255, 255, 0), (neliö[0], neliö[1], 10, 10))
        
        #määritellään suunnan perusteella. mihin mato liikkuu
        #jos suunta on oikea, mato liikkuu oikealle
        if (suunta == 'oikea'):
            madon_paikka[0] += 10
        #jos suunta on vasen, mato liikkuu vasemmalle
        elif (suunta == 'vasen'):
            madon_paikka[0] -= 10
        #jos suunta on ylös, mato liikkuu ylös
        elif (suunta == 'ylos'):
            madon_paikka[1] -=10
        #jos suunta oon alas, mato liikkuu alas
        elif (suunta == 'alas'):
            madon_paikka[1] += 10

        madon_vartalo.append(list(madon_paikka))
        
        #random sijainti omenalle
        if ruoka:
            ruoka_sijainti=[random.randint(20,380), random.randint(20,380)]
            ruoka = False

        #piirretään omena ja asetetaan sen väriksi punainen
        pygame.draw.circle(ruutu,(255,0,0),(ruoka_sijainti[0],ruoka_sijainti[1]),5)
        
        #Näytetään pisteet ja asetetaan fontin väriksi valkoinen
        pisteet_fontti = font.render(f'{pisteet}', True, (valkoinen))
        #asetetaan fontin paikka ruudun yläreunaan 
        fontin_paikka = pisteet_fontti.get_rect(center = (ruutu_leveys // 2 , 30))
        #asetetaan pisteet näkyviin peliin
        ruutu.blit(pisteet_fontti, fontin_paikka)
        
        #Mato saa pisteen kun syö omenan
        #madon täytyy osua omenan keskelle, jotta se syö sen
        if pygame.Rect(madon_paikka[0],madon_paikka[1],10,10).collidepoint(ruoka_sijainti[0], ruoka_sijainti[1]):
            ruoka = True
            pisteet +=1
            #kuuluu piste_sound kun saa pisteen
            piste_sound.play()
        
        #jos ei, mato ei kasva ja poistetaan viimeinen osa matoa
        else:
            madon_vartalo.pop(0)
        
        #peli päättyy, jos mato osuu itseensä
        for neliö in madon_vartalo[:-1]:
            if pygame.Rect(neliö[0], neliö[1], 10 ,10).colliderect(pygame.Rect(madon_paikka[0], madon_paikka[1], 10, 10)):
                #soitetaan gameover_sound
                gameover_sound.play()
                #kutsutaan peli_paattyy metodia 
                peli_paattyy(pisteet)

        # Jos mato osuu seinää, peli päättyy x akseli
        if madon_paikka[0] + 20 <= 0 or madon_paikka[0] >= ruutu_leveys:
            #soitetaan gameover_sound
            gameover_sound.play()
            #kutsutaan peli_paattyy metodia 
            peli_paattyy(pisteet)
        # Jos mato osuu seinää, peli päättyy y akseli
        if madon_paikka[1] + 20 <= 0 or madon_paikka[1] >= ruutu_pituus:
            #soitetaan gameover_sound
            gameover_sound.play()
            #kutsutaan peli_paattyy metodia 
            peli_paattyy(pisteet)

        #päivitetään ruutu
        pygame.display.update()

        #luodaan peliin vaikeutta
        #jos pisteet ovat alle 5, peli kulkee nopeudella 10 fps
        if pisteet < 5:
            #ruutu päivittyy 10 kertaa sekunnissa
            fps.tick(10) 
        #jos pisteet ovat 5-9, peli kulkee nopeudella 15 fps
        if pisteet >= 5 and pisteet < 10:
            #ruutu päivittyy 15 kertaa sekunnissa
            fps.tick(15) 
        #jos pisteet 10-14 peli kulkee nopeudella 20 fps
        if pisteet >= 10 and pisteet < 15:
            #ruutu päivittyy 20 kertaa sekunnissa
            fps.tick(20)
        #jos pisteet 15-19 peli kulkee nopeudella 25 fps
        if pisteet >= 15 and pisteet < 20:
            #ruutu päivittyy 25 kertaa sekunnissa
            fps.tick(25)
        #jos pisteitä on enemmän kuin 20 peli kulkee nopeudella 30 fps
        if pisteet >= 20:
            #ruutu päivittyy 30 kertaa sekunnissa
            fps.tick(30)

#luodaan metodi peli_paattyy, joka saa yhden argumentin (pisteet)
def peli_paattyy(pisteet):
        #luodaan loputon silmukka
        while 1:
            #tarkistetaan tapahtumia esim. näppäimen painallus
            for event in pygame.event.get():
                #jos käyttäjä painaa exit nappia (ruksi ohjelman oikeassa tai vasemmassa yläreunassa), ohjelma sulkeutuu
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #peli päättyy tausta
            #ruutu.fill((0, 0, 0))
            ruutu.blit(peli_paattyy_tausta, [0, 0])

            #peli päättyy viesti punaisella värillä
            peli_paattyy_viesti = font.render("Sinä hävisit", True, (255, 0, 0))
            #peli päättyy pisteet valkoisella värillä
            #kun peli päättyy tulee näkyviin teksti 'Sinä sait x pistettä'
            peli_paattyy_pisteet = font.render(f"Sinä sait {pisteet} pistettä", True, (255, 255, 255))
            #viestin sijainti ruudulla keskelle
            peli_paattyy_viesti_paikka = peli_paattyy_viesti.get_rect(center=(ruutu_leveys // 2, ruutu_pituus // 2))
            #pisteiden sijainti ruudulla
            peli_paattyy_pisteet_paikka = peli_paattyy_pisteet.get_rect(center=(ruutu_leveys // 2, ruutu_pituus // 2+40))

            #asetetaan luodut muuttujat peliin
            ruutu.blit(peli_paattyy_viesti, peli_paattyy_viesti_paikka)
            ruutu.blit(peli_paattyy_pisteet, peli_paattyy_pisteet_paikka)
            #päivitetään ruutu
            pygame.display.update()

            #näytetään gameover ruutua 4 sekuntia ja sen jälkeen siirrytään takaisin menuun
            time.sleep(4)
            menu()

#kustutaan menu metodia
menu()
