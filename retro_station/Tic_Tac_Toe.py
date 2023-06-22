''' TIC TAC TOE GAME '''

import pygame
import numpy as np
import sys
import time




# Global Variables

WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLUMNS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 50


# COLORS
CIRCLE_COLOR = (0, 0, 0)
CROSS_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (30, 144, 255)
LINE_COLOR = (173, 216, 230)



try:
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('TIC TAC TOE GAME')
	screen.fill(BACKGROUND_COLOR)
except Exception as e:
	print(e)
	sys.exit()


# Pinakas
board = np.zeros((BOARD_ROWS, BOARD_COLUMNS))



# Sximatizoume tis grammes kai tis stiles tou pinaka
def draw_lines():
	pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)

	pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)

	pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)

	pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


# Sximatizoume ta X kai O
def draw_table():
	for row in range(BOARD_ROWS):
		for column in range(BOARD_COLUMNS):
			if board[row][column] == 1:
				pygame.draw.circle(screen, CIRCLE_COLOR, (int(column * SQUARE_SIZE + SQUARE_SIZE//2), int(row * SQUARE_SIZE + SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
			elif board[row][column] == 2:
				pygame.draw.line(screen, CROSS_COLOR, (column * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (column * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
				pygame.draw.line(screen, CROSS_COLOR, (column * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (column * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)



def mark_square(row, column, player):
	board[row][column] = player


def available_square(row, column):
	return board[row][column] == 0


# Elexoume an gemise o pinakas dixos na exei nikisei kapoios
def board_full():
	for row in range(BOARD_ROWS):
		for column in range(BOARD_COLUMNS):
			if board[row][column] == 0:
				return False

	return True


# Elenxoume gia nikiti
def check_for_winner(player):

	# Elexnoume tis 2 diagonious
	if board[0][0] == board[1][1] == board[2][2] == player:
		draw_main_diagonal(player)
		return True

	if board[2][0] == board[1][1] == board[0][2] == player:
		draw_secondary_diagonal(player)
		return True

	# Elexnoume katheta
	for columns in range(BOARD_COLUMNS):
		if board[0][columns] == board[1][columns] == board[2][columns] == player:
			draw_vertical_line(columns, player)
			return True

	# Elenxoume orizontia
	for row in range(BOARD_ROWS):
		if board[row][0] == board[row][1] == board[row][2] == player:
			draw_horizontal_line(row, player)
			return True


	return False


# Sximatizoume tin grammi se periptosi opou exoume nikiti

def draw_vertical_line(column, player):
	X = column * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		COLOR = CIRCLE_COLOR
	else:
		COLOR = CROSS_COLOR

	pygame.draw.line(screen, COLOR, (X, 15), (X, HEIGHT - 15), LINE_WIDTH)


def draw_horizontal_line(row, player):
	Y = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		COLOR = CIRCLE_COLOR
	else:
		COLOR = CROSS_COLOR

	pygame.draw.line(screen, COLOR, (15, Y), (WIDTH - 15, Y), WIN_LINE_WIDTH)



def draw_main_diagonal(player):
	if player == 1:
		COLOR = CIRCLE_COLOR
	else:
		COLOR = CROSS_COLOR

	pygame.draw.line(screen, COLOR, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH)

def draw_secondary_diagonal(player):
	if player == 1:
		COLOR = CIRCLE_COLOR
	else:
		COLOR = CROSS_COLOR

	pygame.draw.line(screen, COLOR, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH)



def pygame_quit():
	try:
		pygame.quit()
	except Exception as e:
		print(e)
		sys.exit()


def Tic_Tac_Toe_Game():
	draw_lines()

	player = 1
	game_over = False

	while True:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
				X = event.pos[0]
				Y = event.pos[1]

				ROW = int(Y // SQUARE_SIZE)
				COLUMN = int(X // SQUARE_SIZE)

				if available_square(ROW, COLUMN):
					mark_square(ROW, COLUMN, player)

					if check_for_winner(player):
						game_over = True

					if board_full() and not check_for_winner(player):
						game_over = True

					# Enalagei gia to poios paixteis paizei
					if player == 1:
						player = 2
					else:
						player = 1

					draw_table()

			elif event.type == pygame.QUIT:
				pygame_quit()

		try:
			pygame.display.update()
		except Exception as e:
			print(e)
			sys.exit()

		if game_over:
			time.sleep(1.5)
			break

	pygame_quit()



# Arxi tou programmatos
if __name__ == '__main__':
	Tic_Tac_Toe_Game()
