"""
Handles user input and displays the current game state

"""
import pygame as p
import ChessEngine

width = height = 512 #Don't increase more , It looks bad.
dimension = 8 # Chess is 8x8 
square_size = height // dimension # Size of each square
max_fps = 15 # For animations such as moving pieces
images = {} # This is where the pieces will be loaded 

#Global dictionary with the images. This will be executed once to avoid lagging. 
def load_images():
	pieces = ["bR","bN","bB","bQ","bK","bP","wR","wN","wB","wQ","wK","wP"]
	for piece in pieces:
		images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (square_size , square_size))
		#Access image with 'images["wP"]' (This is the white pawn image for example)

def main():
	p.init() 
	screen = p.display.set_mode((width,height)) # Sets the size of the displayed window
	clock = p.time.Clock()  # clock object to manage frames
	screen.fill(p.Color("white")) # Colour of screen
	gs = ChessEngine.GameState() #object for managing the gamestate
	valid_moves = gs.get_valid_moves() #list of all valid moves
	move_made = False # flag variable to let us know when we need to generate a new set of valid moves 
	animate = False # checks if we need to animate a move (fixes bugs with undo)
	load_images() # We do this once to avoid lagging.
	square_selected = () # used to keep track of the last square the mouse clicked on, tuple(row,col)
	player_clicks = [] # used to keep track of the 2 squares clicked that decide where to move a piece
					   # list(tuple(row,col),tuple(row,col)) 
	game_over = False #check if game ended
	running = True
	while running:
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
			elif e.type == p.MOUSEBUTTONDOWN: # if mouse button is clicked 
				if not game_over:
					location = p.mouse.get_pos() # gives us an (x,y) location of the mouse
					col = location[0]//square_size # gets the column mouse is on
					row = location[1]//square_size # gets the row mouse is on 
					if square_selected == (row,col):  #Checks if user clicked the same square twice so that we undo it 
						square_selected = () # clears square selected
						player_clicks = [] # clear player clicks
					else :
						square_selected = (row,col)
						player_clicks.append(square_selected) # append both clicks that decide the move
					if len(player_clicks) == 2: # checks if the move the user wants to do has been decided
						move = ChessEngine.Move(player_clicks[0],player_clicks[1],gs.board)
						print(move.get_chess_notation())
						for i in range(len(valid_moves)): # iterate through the valid moves
							if valid_moves[i] == move:
								gs.make_move(valid_moves[i]) # provide the move generated by the engine and not by our clicks
								move_made = True
								animate = True
								square_selected = () #reset to make another move
								player_clicks = [] # reset to make another move
						if not move_made:
							player_clicks = [square_selected]

			#Undo move when z is pressed
			elif e.type == p.KEYDOWN:
				if e.key == p.K_z:
					gs.undo_move()
					move_made = True # when undo_move is called we  needs to reset the valid moves 
					animate = False
				elif e.key == p.K_r: # reset the board by pressing r
					gs = ChessEngine.GameState()
					valid_moves = gs.get_valid_moves()
					square_selected = ()
					player_clicks = ()
					move_made = False
					animate = False
		if move_made:
			if animate:
				animate_move(gs.move_log[-1], screen, gs.board,clock) 
			valid_moves = gs.get_valid_moves() # generate a new set of valid moves
			move_made = False
			animate = False
		draw_gamestate(screen,gs,valid_moves,square_selected) # draws the current gamestate
		if gs.in_check and valid_moves == [] : # if checkmate ( in check without valid moves)
			game_over = True
			if gs.white_to_move:
				draw_text(screen, "BLACK WINS BY CHECKMATE")
			else:
				draw_text(screen, "WHITE WINS BY CHECKMATE")
		elif not gs.in_check and valid_moves == []: # if stalemate ( not in check without valid moves)
			game_over = True
			draw_text(screen, " STALEMATE")



		clock.tick(max_fps) # keeps the runtime at 15 frames per second 
		p.display.flip() # Updates the full display 


#Highlight square selected and possible moves for piece selected
def highlight_squares(screen,gs,valid_moves,square_selected):
	if square_selected != ():
		r,c = square_selected #seperate row and column
		if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'): # if white /black plays  and piece clicked is allied
			#highlight selected square
			s = p.Surface((square_size, square_size)) #set a surface 
			s.set_alpha(100) #sets transparancy value
			s.fill(p.Color('blue')) #colour of surface
			screen.blit(s,(c*square_size, r*square_size)) # draw on top
			#highlight moves that piece can do
			s.fill(p.Color('yellow'))
			for move in valid_moves:
				if move.start_row == r and move.start_col == c:
					screen.blit(s,(square_size*move.end_col,square_size*move.end_row))




#Draws the basic layout of the chess board (squares with colours and pieces)
def draw_gamestate(screen,gs,valid_moves,square_selected):
	draw_board(screen) #draws squares on the board
	highlight_squares(screen,gs,valid_moves,square_selected) # highlight squares
	draw_pieces(screen,gs.board) #draw the pieces on top of the squares

#Draws the squares
def draw_board(screen):
	colours = [p.Color(235,235,208),p.Color(119,148,85)]
	for rows in range(dimension):
		for col in range(dimension):
			colour = colours[((rows+col)%2)]
			p.draw.rect(screen,colour,p.Rect(col*square_size,rows*square_size,square_size,square_size))



#Draws the pieces based on the current state
def draw_pieces(screen,board):
	for rows in range(dimension):
		for col in range(dimension):
			piece = board[rows][col]
			if piece != "--": # if it isn't empty ( see ChessEngine board to understand )
				screen.blit(images[piece],(col*square_size,rows*square_size))

#Animating a move
def animate_move(move,screen,board,clock):
	colours = [p.Color(235,235,208),p.Color(119,148,85)] # square colours
	r = move.end_row - move.start_row # the difference so we can calculate the cords
	c = move.end_col - move.start_col 
	frames_per_square = 10 # frames to move 1 square ( we can play around with this)
	frame_count = ( abs(r) + abs(c) ) * frames_per_square # total amount of frames a move will take
	for frame in range(frame_count + 1): # +1 so that we can reach frame_count/frame_count below
		row,col = (move.start_row + r*frame/frame_count,move.start_col + c*frame/frame_count) # r*frame/frame_count means that we split the animation into smaller pieces that move little by little
		draw_board(screen)
		draw_pieces(screen,board)
		#erase the piece moved from its ending square
		colour= colours[(move.end_row + move.end_col)%2]
		end_square = p.Rect(move.end_col * square_size, move.end_row * square_size, square_size, square_size)
		p.draw.rect(screen,colour,end_square) 
		#draw captured piece onto the rectangle
		if move.piece_captured != '--':
			screen.blit(images[move.piece_captured],end_square)
		#draw the moving piece
		screen.blit(images[move.piece_moved],p.Rect(col * square_size, row * square_size, square_size, square_size))
		p.display.flip()
		clock.tick(60) # controls the animation at 60 frames per second



def draw_text(screen,text):
	font = p.font.SysFont("Helvicta", 32 , True , False) # set the font 
	text_object = font.render(text, 0, p.Color (139,0,0)) # render the text
	text_location = p.Rect(0,0,width,height).move(width/2 - text_object.get_width()/2, height/2 - text_object.get_height()/2) # set to thecenter the location
	screen.blit(text_object,text_location)

if __name__ == "__main__":

	main()



