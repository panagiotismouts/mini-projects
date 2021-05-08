"""
This Class will be resonsible for handling information about the game state, valid moves, move log 
and other game specific tasks.

"""
import copy

class GameState():
	def __init__(self): 
		
		#Representation of the board 
		#First letter represents colour b for black and w for white
		#The second letter represents the piece. 
		#"--" represents the spaces between the two sides of the board.
		self.board= [
		
			["bR","bN","bB","bQ","bK","bB","bN","bR"],
			["bP","bP","bP","bP","bP","bP","bP","bP"],
			["--","--","--","--","--","--","--","--"],
			["--","--","--","--","--","--","--","--"],
			["--","--","--","--","--","--","--","--"],
			["--","--","--","--","--","--","--","--"],
			["wP","wP","wP","wP","wP","wP","wP","wP"],
			["wR","wN","wB","wQ","wK","wB","wN","wR"]

			]
		#This dictionary will be used to get all the valid moves from the functions
		self.move_functions = {'P':self.get_pawn_moves,'R':self.get_rook_moves,'B':self.get_bishop_moves,
							'N':self.get_knight_moves,'Q':self.get_queen_moves,'K':self.get_king_moves}
		self.white_to_move = True # white always moves first
		self.move_log = [] # this is where we'll keep log of the moves
		self.white_king_location = (7,4) # starting square of the white king
		self.black_king_location = (0,4) # starting square of the black king
		self.in_check = False # will check if the king is in check
		self.pins = [] # checks fo potential pins (will explain more in the functions)
		self.checks = []# checks for potential checks 
		self.en_passant_possible = () # coordinates for squares where en passant is possible
		self.current_castling_right = CastlingRights(True,True,True,True) # castling is always available at the start of the game
		#Creating a new object instead of adding the current_castling_right because it messes up with undoing later on
		self.castle_right_log = [CastlingRights(self.current_castling_right.wks,self.current_castling_right.wqs, # log of castling rights
												self.current_castling_right.bks,self.current_castling_right.bqs)] 




	#Executes a move
	def make_move(self,move):
		self.board[move.start_row][move.start_col] = '--' #Sets the square that was first clicked to empty
		self.board[move.end_row][move.end_col] = move.piece_moved #Sets the piece to the last square clicked
		self.move_log.append(move)  # we log the moves so that we can undo it later if we have to
		self.white_to_move = not self.white_to_move # switch turns so that black and white play in rotation	

		#update king's location when moved
		if move.piece_moved == 'wK':
			self.white_king_location = (move.end_row,move.end_col) # keep track of white king's location
		elif move.piece_moved == 'bK':
			self.black_king_location = (move.end_row,move.end_col) # keep track of black king's location

		#pawn promotion 
		if move.pawn_promotion:
			self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'
		
		#en passant 
		if move.en_passant_move:
			self.board[move.start_row][move.end_col] = '--' # capturing the pawn

		#update en_passant_possible whenever a 2 pawn advance is being done
		if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2: # if pawn and 2 square pawn advance
			#coordinates of the blank square where the en passant happens
			self.en_passant_possible = ((move.start_row + move.end_row)//2,move.start_col) 
		else: # if any other move than en passant happens after a pawn moves 2 squares , reset the variable
			self.en_passant_possible = ()

		#updating castling rights (if a rook or king moves)
		self.update_castling_rights(move)
		#appending to the log the changed castling rights
		self.castle_right_log.append(CastlingRights(self.current_castling_right.wks,self.current_castling_right.wqs, 
												self.current_castling_right.bks,self.current_castling_right.bqs))

		#castle move
		if move.Castling:
			if move.end_col - move.start_col == 2: #means it's king side castling
				self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1] #move the rook to the left of the knig
				self.board[move.end_row][move.end_col+1] = '--' #square with old rook is now blank				
			else: #queen side castling
				self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2]#same as before but the other side
				self.board[move.end_row][move.end_col-2] = '--'



	#Undo the last move
	def undo_move(self):
		if len(self.move_log) != 0 : # check if there's a move to undo
			move = self.move_log.pop()
			self.board[move.start_row][move.start_col] = move.piece_moved
			self.board[move.end_row][move.end_col] = move.piece_captured
			self.white_to_move = not self.white_to_move # same side plays again
			if move.piece_moved == 'wK':
				self.white_king_location = (move.start_row,move.start_col) #keep track of white king's location
			elif move.piece_moved == 'bK':
				self.black_king_location = (move.start_row,move.start_col) #keep track of black king's location

			#undo en passant
			if move.en_passant_move:
				self.board[move.end_row][move.end_col] = '--' # the square the pawn lands on was blank
				captured_pawn_colour = 'w' if self.board[move.start_row][move.start_col][0] == 'b' else 'b'
				self.board[move.start_row][move.end_col] = captured_pawn_colour + 'P' # place the captured piece back 
				self.en_passant_possible = (move.end_row,move.end_col)

			#undo 2 square pawn advance
			if move.piece_moved[1] == 'P' and abs(move.start_row-move.end_row) == 2:#if pawn moved and it's 2 square advance
				self.en_passant_possible == () #move was undone so we need to reset it 

			#undoing the castling rights
			self.castle_right_log.pop() # we don't need the last castling rights since it's undone
			self.current_castling_right = copy.deepcopy(self.castle_right_log[-1])#setting the current castling rights to the actual last rights
			 

			#undo castle move
			if move.Castling:
				if move.end_col - move.start_col == 2: #king side
					self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
					self.board[move.end_row][move.end_col-1] = '--'
				else: # queen side
					self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
					self.board[move.end_row][move.end_col+1] = '--'


	#Updating castling rights
	def update_castling_rights(self,move):
		if move.piece_moved == 'wK': # if white king moves you cant castle
			self.current_castling_right.wks = False
			self.current_castling_right.wqs = False
		elif move.piece_moved == 'bK': # if black king moves you cant castle
			self.current_castling_right.bks = False
			self.current_castling_right.bqs = False	
		elif move.piece_moved == 'wR' : # if white rook moves 
			if move.start_row == 7: #if rook is on the starting row
				if move.start_col == 0: #left rook
					self.current_castling_right.wqs = False
				elif move.start_col == 7: #right rook
					self.current_castling_right.wks = False	
		elif move.piece_moved == 'bR' : # if black rook moves 
			if move.start_row == 0: #if rook is on the starting row
				if move.start_col == 0: #left rook
					self.current_castling_right.bqs = False
				elif move.start_col == 7: #right rook
					self.current_castling_right.bks = False	

		#making sure we can't castle if rook is captured
		if move.piece_captured == 'wR':
			if move.end_row == 7:
				if move.end_col == 0:
					self.current_castling_right.wqs = False
				elif move.end_col == 7 :
					self.current_castling_right.wks = False
		elif move.piece_captured == 'wR':
			if move.end_row == 0:
				if move.end_col == 0:
					self.current_castling_right.bqs = False
				elif move.end_col == 7 :
					self.current_castling_right.bks = False
	        	


	#All moves considering checks
	def get_valid_moves(self):
		moves = []
		self.in_check,self.pins,self.checks = self.pins_and_checks()
		#find out which king we are checking
		if self.white_to_move:
			king_row = self.white_king_location[0]
			king_col = self.white_king_location[1]
		else:
			king_row = self.black_king_location[0]
			king_col = self.black_king_location[1]
		if self.in_check: # if king is in check
			if len(self.checks) == 1: #if there's only 1 check, either capture the piece checking ,move or block the check
				moves = self.get_all_possible_moves()

				check = self.checks[0] # check contains (end_row,end_col,d[0],d[1]) where d is directions
				check_row = check[0]
				check_col = check[1]
				piece_checking = self.board[check_row][check_col] # enemy piece causing the check
				valid_squares = [] #squares that pieces can move to (only squares that can block the check or capture the piece causing it)
				#if piece is a knight, we must capture it or move the king 
				if piece_checking[1] == 'N':
					valid_squares = [(check_row,check_col)] # pieces can only capture the knight 
				else:
					for i in range(1,8): #start from where the king is 
						valid_square = (king_row + check[2] * i, king_col + check[3] * i)  #calculate all the squares on the check direction
						valid_squares.append(valid_square) # keep adding valid squares 
						if valid_square[0] == check_row and valid_square[1] == check_col: #once  you reach the attacking piece break
							break
				#get rid of any moves that don't block check,move king or capture the piece causing it
				for i in range(len(moves) -1, -1 , -1): # iterate through the moves backwards (because we are removing from a list)
					if moves[i].piece_moved[1] != 'K':# king can't move on the valid squares (check direction) because he's in check
						if  not (moves[i].end_row,moves[i].end_col) in valid_squares: #if move doesn't block check or captures
							moves.remove(moves[i])
			else: # if there's a double check king has to move
				self.get_king_moves(king_row,king_col,moves)
		else: # if not in check all moves are valid
			moves = self.get_all_possible_moves()
		return moves


	#All moves without considering checks 
	def get_all_possible_moves(self):
		moves = []
		for r in range(8): #number of rows
			for c in range(8): # number of columns
				turn = self.board[r][c][0] # get the colour of the piece ( white black or space)
				if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
					piece = self.board[r][c][1]
					self.move_functions[piece](r,c,moves)
		return moves
	
	def pins_and_checks(self):
		pins = [] # squares where the allied piece is pinned and direction of the enemy piece that forces the pin
		checks = [] #squares where enemy is applying a check
		in_check = False
		if self.white_to_move: # if white plays 
			enemy_colour = 'b'
			ally_colour = 'w'
			start_row = self.white_king_location[0]
			start_col = self.white_king_location[1]
		else: # if black plays
			enemy_colour = 'w'
			ally_colour = 'b'
			start_row = self.black_king_location[0]
			start_col = self.black_king_location[1]
		#check around the king for pins and checks and keep track of pins (all directions around the king)
		directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)) # directions around the king (knights not covered here)
		for j in range(len(directions)):  # go through all the directions around the king
			d = directions[j]
			possible_pin = () # reset possible pins
			for i in range(1,8): #go through all the potential squares that can check/pin on that direction (can be from 1 to 7)
				end_row = start_row + (d[0] * i)
				end_col = start_col + (d[1] * i)
				if 0 <= end_row <8 and 0 <= end_col < 8 :
					end_piece = self.board[end_row][end_col]
					if end_piece[0] == ally_colour and end_piece[1] != 'K': 
						if possible_pin == (): # only when 1  allied piece is on a specifc direction can be a pin 
							possible_pin = (end_row,end_col,d[0],d[1])
						else: # if more than 1 allied piece is on a direction it can't be a pin or a check
							break
					elif end_piece[0] == enemy_colour:
						ttype = end_piece[1] # get the kind of the piece (rook,bishop ....)
						'''
						Long if statement because each line:
							1. checks if the rook can attack
							2. checks if the bishop can attack
							3. checking if a pawn can attack (black and white attack in different directions)
							4. if it's a queen or a king and it's 1 square away
						'''
						if (0 <= j <= 3 and ttype == 'R') or  \
							(4 <= j <= 7 and ttype == 'B') or \
							(i == 1 and ttype == 'P' and ((enemy_colour == 'w' and 6 <= j <= 7) or (enemy_colour == 'b' and 4 <= j <= 5))) or \
							(ttype == 'Q') or (i == 1 and ttype == 'K'): 
							if possible_pin == (): #no piece blocking so check
								in_check = True
								checks.append((end_row,end_col,d[0],d[1]))
								break # we can't have more than 1 check on a direction
							else: #piece is blocking so there's a pin
								pins.append(possible_pin)
								break
						else: #enemy piece doesn't apply check ( rook on a diagonal for example)
							break
				else: # out of board
					break
		#checking for knight checks
		knight_moves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)) #all knight moves
		for m in knight_moves:
			end_row = start_row + m[0]
			end_col = start_col + m[1]
			if  0 <= end_row < 8 and 0 <= end_col < 8: # if on board
				end_piece = self.board[end_row][end_col]
				if end_piece[0] == enemy_colour and end_piece[1] == 'N': # enemy knight is attacking king
					in_check = True
					checks.append((end_row,end_col,m[0],m[1]))
		return in_check,pins,checks






	
	#Get all possible pawn moves for the pawn at the specif row, columun and add it to the list
	def get_pawn_moves(self,r,c,moves):
		piece_pinned = False
		pin_direction = ()
		for i in range(len(self.pins)-1, -1 , -1): # iterate through the list of pins backwards (because we remove from the list)
			if self.pins[i][0] == r and self.pins[i][1] == c: # checking if this specific piece is pinned
				piece_pinned = True
				pin_directions = (self.pins[i][2], self.pins[i][3]) # direction it's being pinned from
				self.pins.remove(self.pins[i]) # remove it from the list of pins
				break

		if self.white_to_move: 

			# white pawn moves
			if self.board[r-1][c] == '--': # Check for one square pawn advance
				if not piece_pinned or pin_directions == (-1,0): # if piece isn't pinned or pin direction is the direction the piece moves
					moves.append(Move((r,c),(r-1,c),self.board))		
					if (r == 6 and self.board[r-2][c] == '--'): #Checks for 2 square pawn advance
						moves.append(Move((r,c),(r-2,c),self.board))

				#White pawn captures
			if c-1 >= 0: # Checks to not move out of the board 
				if self.board[r-1][c-1][0] == 'b': # checks if the diagonal piece to the left is black
					if not piece_pinned or  pin_directions == (-1,-1): # if piece isn't pinned or pin direction = capture direction
						moves.append(Move((r,c),(r-1,c-1),self.board))
				elif (r-1,c-1) == self.en_passant_possible: # if you can do en passant append the move and set it to True
					moves.append(Move((r,c),(r-1,c-1),self.board,en_passant_works = True))
			if c+1 <=7 : #Checks to not move out of the board 
				if self.board[r-1][c+1][0] == 'b': # checks if the diagonal piece to the right is black
					if not piece_pinned or pin_directions == (-1,1):  
						moves.append(Move((r,c),(r-1,c+1),self.board))
				elif (r-1, c+1) == self.en_passant_possible:
					moves.append(Move((r,c),(r-1,c+1),self.board, en_passant_works = True))
			#Same with the code above , but for black pawns
		else: 

			#black pawn moves 
			if self.board[r+1][c] == '--':
				if not piece_pinned or pin_directions == (1,0):	
					moves.append(Move((r,c),(r+1,c),self.board))		
					if (r == 1 and self.board[r+2][c] == '--'):
						moves.append(Move((r,c),(r+2,c),self.board))	

			#Black pawn captures
			if c-1>= 0 : # capture to the left
				if self.board[r+1][c-1][0] == 'w':
					if not piece_pinned or pin_directions == (1,-1):
						moves.append(Move((r,c),(r+1,c-1),self.board))
				elif (r+1, c-1) == self.en_passant_possible:
					moves.append(Move((r,c),(r+1,c-1),self.board, en_passant_works = True))
			if c+1 <=7: #capture to the right
				if self.board[r+1][c+1][0] == 'w' :
					if not piece_pinned or pin_directions == (1,1):
						moves.append(Move((r,c),(r+1,c+1),self.board))
				elif (r+1, c+1) == self.en_passant_possible:
					moves.append(Move((r,c),(r+1,c+1),self.board, en_passant_works = True))

	#Get all possible rook moves for the rook at the specif row, columun and add it to the list
	def get_rook_moves(self,r,c,moves):
		piece_pinned = False
		pin_directions = ()
		for i in range(len(self.pins) -1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piece_pinned = True
				pin_directions = (self.pins[i][2], self.pins[i][3])
				if self.board[r][c][1] != 'Q' : # queens call this function so we don't want to remove them from the list 
					self.pins.remove(self.pins[i])
				break

		directions = ((-1,0), (0,-1), (1,0), (0,1) ) #Directions for up,left,down,right according to (row,col)
		enemy_colour = 'b' if self.white_to_move else 'w' # Get the enemy piece according to who is playing
		for d in directions:
			for i in range(1,8):	
				end_row = r + (d[0] * i)  #Both rows calculate all potential squares (row,col) rook could go 
				end_col = c + (d[1] * i)
				if 0 <= end_row < 8 and 0 <= end_col < 8 : # Checks to not go out of the board
					if not piece_pinned or pin_directions == d or pin_directions == (-d[0], -d[1]):	 # if not pinned or directions are towards or away from the attacking piece
						end_piece = self.board[end_row][end_col]
						if end_piece == '--':
							moves.append(Move((r,c),(end_row,end_col),self.board))
						elif end_piece[0] == enemy_colour: #if you can capture the enemy piece
							moves.append(Move((r,c),(end_row,end_col),self.board))
							break #can't move further once you encounter an enemy piece
						else: 
							break #found a friendly piece, can't move further
				else:
					break #we went off board

					
	
	#Get all possible knight moves for the knight at the specif row, columun and add it to the list
	#The code is basically the same with get_rook_moves but knights move in very specific ways
	def get_knight_moves(self,r,c,moves):
		piece_pinned = False
		for i in range(len(self.pins) - 1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piece_pinned = True
				self.pins.remove(self.pins[i])
				break

		knight_moves = ((-2,-1), (-2,1), (-1,-2), (1,-2), (-1,2), (1,2), (2,1), (2,-1))	
		ally_colour = 'w' if self.white_to_move else 'b' #Code might look cleaner with ally colour (basically the same)
		for m in knight_moves:
			end_row = r + m[0]
			end_col = c + m[1]
			if  0 <= end_row < 8 and 0 <= end_col < 8:
				if not piece_pinned:
					end_piece = self.board[end_row][end_col]
					if end_piece[0] != ally_colour: #if enemy piece or '--'
						moves.append(Move((r,c),(end_row,end_col),self.board))


	








	#Get all possible bishop moves for the bishop at the specif row, columun and add it to the list
	#The code is basically the same with get_rook_moves but bishops move diagonally 
	def get_bishop_moves(self,r,c,moves):
		piece_pinned = False
		pin_directions = ()
		for i in range(len(self.pins) -1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piece_pinned = True
				pin_directions = (self.pins[i][2], self.pins[i][3])
				self.pins.remove(self.pins[i])
				break
		directions = ((-1,-1), (-1,1), (1,-1), (1,1))
		enemy_colour = 'b' if self.white_to_move else 'w'
		for d in directions:
			for i in range(1,8):
				end_row = r + ( d[0] * i )
				end_col = c + ( d[1] * i )
				if 0 <= end_row < 8 and 0 <= end_col < 8:
					if not piece_pinned or pin_directions == d or pin_directions == (-d[0], -d[1]):
						if self.board[end_row][end_col] == '--':
							moves.append(Move((r,c),(end_row,end_col),self.board))
						elif self.board[end_row][end_col][0] == enemy_colour:
							moves.append(Move((r,c),(end_row,end_col),self.board))
							break
						else:
							break
				else:
					break


#Get all possible queen moves for both queens and add it to the list
	def get_queen_moves(self,r,c,moves):
		#Queen is basically  a combination of bishop and rook 
		self.get_bishop_moves(r,c,moves)
		self.get_rook_moves(r,c,moves)

#Get all possible king  moves for both kings and add it to the list
	def get_king_moves(self,r,c,moves):
		row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
		col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
		ally_colour = 'w' if self.white_to_move else 'b'
		for i in range(8):
			end_row = r +  row_moves[i] 
			end_col = c +  col_moves[i]
			if 0 <= end_row < 8 and 0 <= end_col < 8:
				end_piece = self.board[end_row][end_col]
				if end_piece[0] != ally_colour : #not an ally piece
					#place king on the end location ( to check for checks)
					if ally_colour == 'w' :
						self.white_king_location = (end_row,end_col) 
					else:
						self.black_king_location = (end_row,end_col)
					in_check, pins, checks = self.pins_and_checks() # find out if the king now is in check
					#if not in check make the move
					if not in_check:
						moves.append(Move((r,c),(end_row,end_col),self.board))
					#place king on the original location
					if ally_colour == 'w':
						self.white_king_location = (r,c)
					else:
						self.black_king_location = (r,c)

		self.get_castling_moves(r, c, moves, ally_colour)
		
	def get_castling_moves(self, r, c, moves, ally_colour):
		pins_checks = self.pins_and_checks()
		in_check = pins_checks[0] # getting the in_check 
		if self.in_check:
			return  # can't castle while on check
		if (self.white_to_move and self.current_castling_right.wks) or (not self.white_to_move and self.current_castling_right.bks): #if we can castle on king side
			self.king_side_castling_moves(r, c, moves, ally_colour)
		if (self.white_to_move and self.current_castling_right.wqs) or (not self.white_to_move and self.current_castling_right.bqs):
			self.queen_side_castling_moves(r, c, moves, ally_colour)		

	def king_side_castling_moves(self, r, c, moves, ally_colour):
		in_check = [False,False]
		if ally_colour == 'w':
			if self.board[r][c+1] == '--' and self.board[r][c+2] == '--' :
				#checking if the first square king side is attacked
				self.white_king_location = (r,c+1)
				pins_checks = self.pins_and_checks()
				in_check[0] = pins_checks[0]
				#checking if the second square king side is attacked
				self.white_king_location = (r,c+2)
				pins_checks = self.pins_and_checks()
				in_check[1] = pins_checks[0]
				#reset king location
				self.white_king_location = (r,c)
		else:
			if self.board[r][c+1] == '--' and self.board[r][c+2] == '--' :
				#checking if the first square king side is attacked
				self.black_king_location = (r,c+1)
				pins_checks = self.pins_and_checks()
				in_check[0] = pins_checks[0]
				#checking if the second square king side is attacked
				self.black_king_location = (r,c+2)
				in_check[1] = pins_checks[0]
				in_check.append(pins_checks[0])
				#reset king location
				self.black_king_location = (r,c)
		#if both squares are empty and not in check
		if not in_check[0] and not in_check[1]:
			moves.append(Move((r,c), (r,c+2), self.board, Castling=True))



		


		


	def queen_side_castling_moves(self, r, c, moves, ally_colour):
		in_check = [False,False]
		if ally_colour == 'w':
			if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--' :
				#checking if the first square king side is attacked
				self.white_king_location = (r,c-1)
				pins_checks = self.pins_and_checks()
				in_check[0] = pins_checks[0]
				#checking if the second square king side is attacked
				self.white_king_location = (r,c-2)
				pins_checks = self.pins_and_checks()
				in_check[1] = pins_checks[0]
				#checking if the third square king side is attacked
				#reset king location
				self.white_king_location = (r,c)

		else:
			if self.board[r][c+1] == '--' and self.board[r][c-2] == '--' :
				#checking if the first square queen side is attacked
				self.black_king_location = (r,c-1)
				pins_checks = self.pins_and_checks()
				in_check[0] = pins_checks[0]
				#checking if the second square queen side is attacked
				self.black_king_location = (r,c-2)
				in_check[1] = pins_checks[0]
				in_check.append(pins_checks[0])
				#reset king location
				self.black_king_location = (r,c)

		if not in_check[0] and not in_check[1]:
			moves.append(Move((r,c), (r,c-2), self.board, Castling=True))








class CastlingRights():
	def __init__(self,wks,bks,wqs,bqs): #white king side, black king sied. white queen side, black queen side
		self.wks = wks
		self.bks = bks
		self.wqs = wqs
		self.bqs = bqs









		





class Move():
	#Chess rows are named ranks, starting from the bottom they are numbered from 1 to 8
	# We use coordinates, which go from 0 to 7 starting from the top 
	#Therefore this matches chess ranks to our cords
	ranks_to_rows = {"1": 7,"2": 6,"3": 5,"4": 4,"5": 3,"6": 2,"7": 1,"8": 0}

	#This basically tells python to reverse the dictionary making a value: key pair 
	rows_to_ranks = {v: k for k,v in ranks_to_rows.items()}
	
	#Same thing as above , columns are named files in chess 
	#starting from left to right they are numbered as a to h
	#We match files to our cords
	files_to_cols = {"a": 0,"b": 1,"c": 2,"d": 3,"e": 4,"f": 5,"g": 6,"h": 7}

	cols_to_files = {v:k for k,v in files_to_cols.items()}


	def __init__(self, start_square, end_square, board, en_passant_works = False, Castling = False):
		#We separate the squares to rows and columns ( they are both tuples , check player_clicks in main() )
		self.start_row = start_square[0] 
		self.start_col = start_square[1]
		self.end_row = end_square[0]
		self.end_col = end_square[1]
		self.piece_moved = board[self.start_row][self.start_col] #Checks which piece was moved on the board
		self.piece_captured = board[self.end_row][self.end_col] #Checks which piece was captured 
		#Basically here we create an ID with a number between 0000 and 7777 
		#It  tells us the starting and ending squares of a move
		#For example 0002 tells us that the starting square is (0,0) and the ending square is (0,2)
		self.move_ID = self.start_row * 1000 + self.start_col *100 + self.end_row * 10 + self.end_col 

		#checking if we can promote a pawn to queen
		self.pawn_promotion = (self.piece_moved == 'wP' and self.end_row == 0) or (self.piece_moved == 'bP' and self.end_row == 7)

		#checking if we can do an en passant
		self.en_passant_move = en_passant_works

		#castling
		self.Castling = Castling
	






	#Overriding the equals method
	def __eq__(self,other):  # This compares an object (self) to another object (other)
		if isinstance(other,Move): #Check if other is an instance of the Move class
			return self.move_ID == other.move_ID
		return False 





	#We get the chess notation for the first and second click that decide the move 
	def get_chess_notation(self):
		return self.get_ranks_files(self.start_row,self.start_col) + " -> " + self.get_ranks_files(self.end_row,self.end_col)

	#We change  the row/cols with ranks and files
	def get_ranks_files(self,r,c):
		return self.cols_to_files[c] + self.rows_to_ranks[r]
