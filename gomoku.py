"""
Gomoku in console
"""

import numpy as np


def location2coordiante(loc, colnames):
	"""Get coordinate from string and check if it is a valid input"""
	col_str = loc[0]   # string
	row_str = loc[1:]
	print(f"col_str: {col_str}")
	if col_str in colnames:
		try:
			col = colnames.index(col_str)
			row = int(loc[1:]) - 1  # integer
			if row < len(colnames):
				location_valid = True
			else:
				print("Invalid row!")
				location_valid = False
		except ValueError:
			print("Invalid row!")
			return 0.0, 0.0, False
	else:
		row, col = 0, 0
		print("Invalid column!")
		location_valid = False
	return row, col, location_valid


def get_marker(player_int):
	if player_int == 1:
		marker = "●"
	elif player_int == -1:
		marker = "○"
	else:
		marker = "-"
	return marker


class GomokuGame:
	def __init__(self, n=15, colspace=3):
		# initialize game
		self.n = n
		self.board = np.zeros((n,n))
		self.board_prev = self.board
		self.move_history = []
		# initialize column name
		self.colnames = []
		for idx in range(n):
			self.colnames.append(chr(idx+97))
		# initialize player
		self.current_player = 1
		# column-wise space
		self.colspace = colspace
		# top message
		self.topbar = "     "
		for col in self.colnames:
			self.topbar += " "*self.colspace + col
		if self.n > 26:
			raise ValueError("Max board size is 26!")

	def update(self, loc):
		"""Update move"""
		if self.current_player == 1:
			move_success = self.player_update(loc, 1)
			if move_success==True:
				self.current_player = 2
		else:
			move_success = self.player_update(loc, -1)
			if move_success==True:
				self.current_player = 1
		return


	def player_update(self, loc, player_int):
		"""Insert player move into board"""
		row, col, location_valid = location2coordiante(loc, self.colnames)
		if location_valid==True:
			if self.board[row, col] == 0:
				self.move_history.append((row, col, player_int))
				self.board[row, col] = player_int
				move_success = True
			else:
				print("Already occupied!")
				move_success = False
		else:    # location_valid == False
			print("Invalid location!")
			move_success = False
		return move_success


	def print_board(self):
		"""Print current status of the board"""
		print("\n")
		print(self.topbar)
		print("\n")
		for idx, ithcol in enumerate(self.board):
			if len(str(idx+1)) == 1:
				col_name = " " + str(idx+1)
			else:
				col_name = str(idx+1)
			col_str = col_name + "    "
			for el in ithcol:
				marker = get_marker(int(el))
				col_str += " "*self.colspace + marker
			print(col_str, "\n")
		return


	def undo(self):
		"""Undo last move"""
		if len(self.move_history)==0:
			return
		else:
			remove = self.move_history[-1]
			self.board[remove[0], remove[1]] = 0.0
			# pop last element from move-history
			self.move_history.pop()
			# switch player
			if self.current_player == 1:
				self.current_player = 2
			else:
				self.current_player = 1
		return


def play_game(n=15):
	"""Play Gomoku game

	Args:
		n (int): board size, will be n * n, max 26
	"""
	# initialize
	Gomoku = GomokuGame(n=n)
	end_game = False
	# print intial board
	Gomoku.print_board()
	while end_game == False:
		option = input(f"Player {Gomoku.current_player} move [e.g. h8] OR b - back, q - quit: ")
		if option == "b":
			# go back one move
			Gomoku.undo()
			Gomoku.print_board()

		elif option == "q":
			# quit game
			end_game = True

		else:
			# update
			Gomoku.update(option)
			Gomoku.print_board()
	return


if __name__=="__main__":
	play_game(n=15)