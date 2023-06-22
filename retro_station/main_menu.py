#Onoma omadas : Games of py
#Apallaktiko Project : Efarmosmenos Programmatismos me Python

# To arxeio ayto apotelei to Main Menu tou paixnidioy "Retro Station"
import pygame, sys

mainClock = pygame.time.Clock()
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Retro Station')
screen = pygame.display.set_mode((500, 500), 0, 32)

font = pygame.font.Font('images1/Raleway-Regular.ttf', 20) #font einai h grammatoseira poy 8a xrhsimopoih8ei sto game, https://www.1001freefonts.com/raleway.font


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False



def main_menu():
    while True:

        screen.fill((0, 0, 0))#Gemisma o8onhs se mavro xrwma.
        draw_text('Main Menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()   #syntetagmenes tou mouse

        #ta koumpia ekkinhshs twn paixnidiwn
        button_1 = pygame.Rect(50, 70, 200, 50)
        button_2 = pygame.Rect(50, 140, 200, 50)
        button_3 = pygame.Rect(50, 210, 200, 50)
        button_4 = pygame.Rect(50, 280, 200, 50)
        button_5 = pygame.Rect(50, 350, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                import ChessMain
                ChessMain.main()
        if button_2.collidepoint((mx, my)):
            if click:
                import retro_car_game
                retro_car_game.main()
        if button_3.collidepoint((mx, my)):
            if click:
                import Pong
                Pong.main()
        if button_4.collidepoint((mx, my)):
            if click:
                import Snake
                Snake.Snake_Game()
        if button_5.collidepoint((mx, my)):
            if click:
                import Tic_Tac_Toe
                Tic_Tac_Toe.Tic_Tac_Toe_Game()

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        txt1 = draw_text('Play : Chess', font, (0, 0, 0), screen, 50, 70)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        txt2 = draw_text('Play : Retro Car Game', font, (0, 0, 0), screen, 50, 140)
        pygame.draw.rect(screen, (255, 0, 0), button_3)
        txt3 = draw_text('Play : Pong', font, (0, 0, 0), screen, 50, 210)
        pygame.draw.rect(screen, (255, 0, 0), button_4)
        txt4 = draw_text('Play : Snake', font, (0, 0, 0), screen, 50, 280)
        pygame.draw.rect(screen, (255, 0, 0), button_5)
        txt5 = draw_text('Play : Tic Tac Toe', font, (0, 0, 0), screen, 50, 350)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

def main():
    main_menu()

if __name__ == '__main__':
    main()