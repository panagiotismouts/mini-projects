#Retro Car Game for the subject "Eisagwgh ston Programmatismo me Python"
#Onoma omadas : Games of py
#Creator : Moutsiounas Panagiotis AM P2018007

#O odhgos vrisketai se ena aytokinhtodromo me alla aytokinhta.
#Skopos tou paixnidioy einai na mazepsei oso ginetai pio polles shmaies
#Xwris na trakarei se alla aytokinhta. O odhgos mporei na strivei ,na pataei gkazi
#kai na frenarei to oxhma tou me ta velakia, opws ena klassiko paixnidi me aytokinhta.

#Gia na tre3ei, prepei na einai installed h pygame, pip install pygame.

import pygame
import random

pygame.mixer.pre_init(44100,-16,1,512) #orizoume to channel pou 8a exoume diafora samples mousikhs mesa sto game.
pygame.mixer.init()# pername apo to pre init sto init, na arxisei na paizei h mousikh
pygame.init()# arxizei to game
pygame.font.init()# provolh tou font
clock = pygame.time.Clock()#ka8e game exei tick rate. to orizoume sthn metavlith clock.

#ry8mhsh o8onhs se pixel, alla kai twn fps.
screen_width = 700
screen_height = 800
fps = 120

window = pygame.display
window.set_caption('Retro Car Game')
window.set_icon(pygame.image.load('car.ico')) # non copyrighted at : https://findicons.com/icon/78723/car
screen = pygame.display.set_mode((screen_width,screen_height))


#Background class
class Background:
    def __init__(self):
        self.bg = pygame.image.load('road.png').convert_alpha()#To road.png dhmioyrgh8hke apo emena sth
        # Zwgrafikh twn Windows opote den xreiazetai pnevmatika dikaiwmatal. Orizoume to background kai
        # to kanei aytomata convert me thn entolh convert_alpha.
        self.thesi = -1 #h thesi kai to speed xreiazontai kai gia to background.
        self.speed = 0

    def draw(self):
        self.thesi += self.speed
        if self.thesi >= 0:
            self.thesi = -700
        screen.blit(self.bg, (0,int(self.thesi))) #h entolh kati.blit mas kanei draw
        #to background apo thn arxh, stis syntetagmenes poy 8a orisoume. orizw 0,-700 gia na einai sth
        #swsth 8esh o dromos.

#klash gia ton paikth kai to aytokinhto tou paikth

class Player:
    def __init__(self):
        self.image = pygame.image.load('Audi.png').convert_alpha()#https://opengameart.org/content/free-top-down-car-sprites-by-unlucky-studio   ,dwrean apo copyright, car sprites, gia mh emporikh xrhsh fysika.
        self.sound_rev = pygame.mixer.Sound('0600.ogg') #gia ton hxo ths mhxanhs, https://bigsoundbank.com/detail-0600-acceleration-aston-martin.html
        self.sound_rev.set_volume(0.5)# for the horn :  https://www.freesoundeffects.com/free-sounds/cars-10069/
        self.sound_horn = pygame.mixer.Sound('horn.ogg')
        self.sound_horn.set_volume(0.3)
        #gia th 8esh kai taxythta
        self.trace = (0, 0, 0, 0)
        self.posx = 300
        self.posy = 650

        self.speed = 0
        self.carspeed = -5

        self.moving_left = False
        self.moving_right = False
        self.gas = False
        self.brake = False

#gia ta events kinhshs, ta koumpia dld otan einai pathmena kai otan den einai
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.gameover = True
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    elif event.key == pygame.K_UP:
                        self.gas = True
                    elif event.key == pygame.K_DOWN:
                        self.brake = True
            if event.type == pygame.KEYUP: # gia na gyrisoun oles oi metavlhtes sthn arxikh tous timh
                self.moving_right = False
                self.moving_left = False
                self.gas = False
                self.brake = False
                self.sound_rev.stop()
        #gia thn kinhsh, gia na meinei sta oria tou xarth.
        if self.moving_left and not self.posx - 2.5 <= 180:
            self.posx -= 2.5
        if self.moving_right and not self.posx + 2.5 >=427:
            self.posx += 2.5
        #gia thn kinhsh ey8eia
        if self.gas and self.speed < 300:
            self.speed += 1/3 #na ay3anetai dld siga siga oso patame to gkazi mexri ta 299
            bg.speed += 1/6
            flag.speed += 1/60
            self.carspeed += 1/10
            if not pygame.mixer.get_busy():#se periptwsh pou afhsoume to gazi
                    self.sound_rev.play(loops=0, maxtime=0, fade_ms=1)#na kanei kai fade siga siga
        if self.brake and self.speed > 0:#an frenaroume dld, 8a ginetai to e3hs
            self.speed -= 2
            bg.speed -= .05*2
            flag.speed -= .005*2
            self.carspeed -= .03*2
            self.sound_rev.stop()
        if self.speed <= 0 or bg.speed <= 0:#gia na protrepsoume sfalma (moy synevh)
            self.speed = 0
            bg.speed = 0


    def draw(self):
        self.trace = screen.blit(self.image, (int(self.posx), int(self.posy)))
        self.trace = (self.trace[0]+5, self.trace[1]+5, self.trace[2]-10, self.trace[3]-10)

#classh gia ta aytokinhta pou 8a einai "bots". 8a exoyme 3 diaforetika aytokinhta
# kai 8a ginei xrhsh ths vivlio8hkhs random.
class Car:
    def __init__(self, posx):
        self.image0 = pygame.image.load('Car.png').convert_alpha()
        self.image1 = pygame.image.load('Mini_truck.png').convert_alpha()
        self.image2 = pygame.image.load('taxi.png').convert_alpha()
        #ta vazoume se mia lista
        self.image_list = (self.image0, self.image1, self.image2)
        self.image = self.image_list[2]#pairnw ena akyro ap ta 3, den exei shmasia poio 8a parw
        #orizw thn katastash pou 8a einai otan 8a 3ekinane
        self.trace = (0, 0, 0, 0)
        self.posx = posx
        self.posy = -500
        self.speed = 0
        self.is_moving = False
    # ksana tha orisoume thn kinhsh twn aytokinhtwn
    def move(self):
        if not self.is_moving:
            rnd = random.randint(1, game.difficulty) #orizoume game difficulty
            if rnd == 50:
                self.is_moving = True
                self.image = self.image_list[random.randint(0,2)]
            #sthn ousia, exoume to rand kai otan einai 50, ena ama3i 8a 3ekinaei, ena random ama3i apo ta 3.
                self.speed = random.randint(0,3)
                if self.speed == 3 and player.speed > 200:
                    player.sound_horn.play(loops=0, maxtime=0, fade_ms=0)#8a kornaroun ta botakia
                    #an trexoyn ayta poly kai trexei kai o paixths.
        else:
            self.posy += player.carspeed + self.speed
            if self.posy >= screen_height or self.posy <= -999:
                self.is_moving = False
                self.posy = -150

    def draw(self):
        self.trace = screen.blit(self.image, (int(self.posx), int(self.posy)))
        self.trace = (self.trace[0]+5, self.trace[1]+5, self.trace[2]-10, self.trace[3]-10)

#klash gia  to flag. Oses pio polles shmaies mazevei toso anevainei to score.

class Flag:
    def __init__(self):
        self.image = pygame.image.load('racing flag.png').convert_alpha() #https://www.transparentpng.com/download/checkered-flag-clipart-at-pic_1735.html  dwrean gia mh emporikh xrhsh.
        self.trace = (0, 0, 0, 0)
        self.posx = 210
        self.posy = -999
        self.speed = 0
        self.is_moving = False

    def move(self):
        if not self.is_moving:
            self.is_moving = True
            self.posx = random.randint(205, 450)# an den kineitai dhladh, na topo8eth8ei se ena random shmeio.
        else:
            self.posy += self.speed
            if self.posy >= screen_height: #gia na mhn mas bgei e3w ap thn o8onh
                self.is_moving = False
                self.posy = -50
                game.difficulty -= 100
                if game.difficulty <= 100:
                    game.difficulty = 100

    def draw(self):
        self.trace = screen.blit(self.image, (int(self.posx), int(self.posy)))

#klash gia to paixnidi. edw 8a oristoun : to score, ta xiliometra kai to collsion.

class Game:
    def __init__(self):# ksana orizoume metavlhtes gia thn klassh game. (to antikeimeno dhladh game).
        self.score = 0
        self.gameover = False
        self.difficulty = 500
        self.FONT = pygame.font.Font('Raleway-Regular.ttf', 20) #font einai h grammatoseira poy 8a xrhsimopoih8ei sto game, https://www.1001freefonts.com/raleway.font
        pygame.mixer.music.load('Sports-Car-Idle-www.fesliyanstudios.com.ogg') #https://www.fesliyanstudios.com/royalty-free-sound-effects-download/car-driving-207
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)# -1 shmainei na paizei se loupa synexeia.
        self.image = pygame.image.load('crashed-car-transparent-3 (1).png').convert_alpha()#http://clipart-library.com/clip-art/crashed-car-transparent-3.htm, free for commercial use
        self.sound_crash = pygame.mixer.Sound('WoodCrashesDistant FS022705.ogg')#https://www.videvo.net/sound-effect/wood-crashes-distant-fs022705/262147/ gia ton hxo otan 8a trakarei.
        self.sound_crash.set_volume(0.5)
        self.sound_point = pygame.mixer.Sound('mixkit-arcade-retro-changing-tab-206.ogg')# gia tous pontous. https://mixkit.co/free-sound-effects/game/
        self.sound_point.set_volume(0.5)

    def draw_score(self):#emfanhsh score sthn o8onh
        txt_speed = self.FONT.render('Speed:' + str(int(player.speed)) + ' km/h', True, (255, 255, 255)) # edw orizoume to keimeno me th xrhsh tou font poy
        #katevasame. 8a einai se aspro xrwma giayto kai h lista me tis times twn 255, 255, 255 se rgb.
        txt_score = self.FONT.render('Score: ' + str(self.score), True, (255,255,255))

        screen.blit(txt_speed, (10,610))
        screen.blit(txt_score, (10, 640))

    def collission(self):
        pl = pygame.Rect(player.trace)#kanei ton paixth collisionable. dhladh gia th sygroush
        fl = pygame.Rect(flag.trace)#to idio gia tis shmaies

        cars = [pygame.Rect(car1.trace), pygame.Rect(car2.trace), pygame.Rect(car3.trace), pygame.Rect(car4.trace)]

        if pl.colliderect(fl):
            flag.posx = -50
            game.score += 1
            self.sound_point.play(loops=0,maxtime=0,fade_ms=0)

        for car in cars:
            if pl.colliderect(car):#an trakarei dhladh o player me kapoio bot car
                screen.blit(self.image, (int(player.posx - 80), int(player.posy + 10)))
                window.update()
                pygame.mixer.music.stop()
                player.sound_rev.stop()
                self.sound_crash.play(loops=0,maxtime=0,fade_ms=1)
                pygame.time.delay(5000)#se miliseconds
                self.gameover = True


    #h ka8oristikh synarthsh, h loopa pou ola 8a symvainoun synexws.
    def mainloop(self):
        while not self.gameover:
            print(player.posx)
            clock.tick(fps)#orizoume ta fps.
            print(clock.tick(fps))
            bg.draw()
            flag.move()
            flag.draw()
            player.move()
            player.draw()
            car1.move()
            car1.draw()
            car2.move()
            car2.draw()
            car3.move()
            car3.draw()
            car4.move()
            car4.draw()
            game.draw_score()
            game.collission()
            window.update()


#kai telos na orisoume tis metavlhtes mas, ta antikeimena dld twn klasewn.

bg = Background()
player = Player()
car1 = Car(posx=205)
car2 = Car(posx=280)
car3 = Car(posx=360)
car4 = Car(posx=435)
flag = Flag()
game = Game()

game.mainloop()
pygame.quit()#gia otan teleiwnei to paixnidi
quit()



