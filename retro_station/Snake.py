''' Snake Game '''


import pygame
import random
import pyxel
import sys
from collections import namedtuple

# Global Variables
RIGHT = 1
LEFT = 2
UP = 3
DOWN = 4

BLOCK_SIZE = 20
SPEED = 10

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREEN2 = (0, 100, 0)


Point = namedtuple('Point', 'x, y')


try:
    pygame.init()
    font = pygame.font.SysFont('arial', 25)
except Exception as e:
    print(e)
    sys.exit()


class Snake:
    def __init__(self, height=640, width=480):
        self.height = height
        self.width = width

        self.display_screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.direction = RIGHT
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y), Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food1 = Point(0, 0)
        self.food2 = False
        self.game_over = False


    def place_food(self):
        if self.score < 5:
            x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.food1 = Point(x, y)
        else:
            x = random.randint(0, abs(self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, abs(self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.food1 = Point(x, y)

            x = random.randint(0, abs(self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, abs(self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.food2 = Point(x, y)

        # Se periptosi opou to food topothetithei se kapoia thesi tou snake kaloume pali tin sunartisi oste na allaksei to simio tou food
        if (self.food1 in self.snake) or (self.food2 in self.snake):
            self.place_food()




    def play(self):
        global SPEED

        # Epilogi tou xristi
        for user_input in pygame.event.get():
            if user_input.type == pygame.KEYDOWN:
                if user_input.key == pygame.K_LEFT:
                    self.direction = LEFT
                elif user_input.key == pygame.K_RIGHT:
                    self.direction = RIGHT
                elif user_input.key == pygame.K_UP:
                    self.direction = UP
                elif user_input.key == pygame.K_DOWN:
                    self.direction = DOWN
            elif user_input.type == pygame.QUIT:
                pygame.quit()

        self.move(self.direction)
        self.snake.insert(0, self.head)


        if self.collision():
            self.game_over = True
            return self.game_over, self.score


        if (self.head == self.food1) or (self.head == self.food2):
            # Kathe fora pou troei to fadaki auksanouume kata 1 to SPEED efoson to score einai artios
            if self.score % 2 == 0:
                SPEED += 1
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()


        self.update_game()
        self.clock.tick(SPEED)

        return self.game_over, self.score




    def update_game(self):
        # BACKGROUND_
        self.display_screen.fill(BLACK)

        # Emfanisi tou fidiou
        for point in self.snake:
            pygame.draw.rect(self.display_screen, GREEN, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display_screen, GREEN2, pygame.Rect(point.x + 2, point.y + 4, 10, 10))

        # Emfanisi tou food
        pygame.draw.rect(self.display_screen, RED, pygame.Rect(self.food1.x, self.food1.y, BLOCK_SIZE, BLOCK_SIZE))

        if self.score >= 5:
            pygame.draw.rect(self.display_screen, RED, pygame.Rect(self.food2.x, self.food2.y, BLOCK_SIZE, BLOCK_SIZE))


        text = font.render("Points: " + str(self.score), True, WHITE)
        self.display_screen.blit(text, [0, 0])

        pygame.display.flip()


    # Elexnoume poio pliktro edose o xristis
    def move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == RIGHT:
            x += BLOCK_SIZE
        elif direction == LEFT:
            x -= BLOCK_SIZE
        elif direction == DOWN:
            y += BLOCK_SIZE
        elif direction == UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


    def collision(self):
        # Elexnos gia to an to fidaki xtypise sta akra h ston eauto tou
        # An xtypise termatizetai to paixnidi allios senexizei
        if (self.head.x > self.width - BLOCK_SIZE) or (self.head.x < 0) or (self.head.y > self.height - BLOCK_SIZE) or (self.head.y < 0):
            return True
        elif self.head in self.snake[1:]:
            return True

        return False



class Print:
    def __init__(self, score):
        self.score = score
        pyxel.init(160, 120, caption="Snake Game")

    # Me to pliktro Q termatizei
    def quit(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def print(self):
        pyxel.cls(0)
        pyxel.text(60, 0, "GAME OVER", pyxel.frame_count % 16)
        pyxel.text(50, 40, f"Total Points: {self.score}", pyxel.frame_count % 16)
        pyxel.blt(70, 65, 0, 0, 0, 40, 20)


    def run(self):
        pyxel.run(self.quit, self.print)





def Snake_Game():
    snake = Snake()

    while True:
        game_over, score = snake.play()

        if game_over:
            break

    try:
        pygame.quit()
    except Exception as e:
        print(e)
        sys.exit()

    # Emfanizoume to teliko scor
    pnt = Print(score)
    pnt.run()



# Arxi tou programmatos
if __name__ == '__main__':
    Snake_Game()

