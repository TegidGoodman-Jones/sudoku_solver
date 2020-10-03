import time
import Generator

# Author: Tegid Goodman-Jones
# 03/10/2020

def get_board(file):

	with open(file, 'r') as f:
		file_text = f.read()
		text = ""

		# get board on one line
		for line in file_text: 
			line = ' '.join(line.split())
			text += line

		board = []

		while len(text) > 0:
			l = []

			# Get row of numbers
			while len(l) < 9:
				if text[0].isdigit():
					l.append(int(text[0]))
				text = text[1:]  # removing character just added

			board.append(l)

		return board

def print_board(bo):
	"""
	Formats the Sudoku puzzle currently in a 2D list into
	a grid with lines separating the blocks for readability
	"""
	
	for row in range(9):
		for col in range(9):
			print(bo[row][col], end=' ')

			if col + 1 == 3 or col + 1 == 6:
				print(" | ", end=' ')

		if row + 1 == 3 or row + 1 == 6:
			print("\n" + "-"*25, end=' ')
		print()
	print()


def test_valid(bo, row, col):
	
	"""
	Given a Sudoku puzzle s, row, and column number, return a list which represents
	the valid numbers that can go in that cell. 0 = possible, 1 = not possible
	"""

	used = [0]*10
	used[0] = 1  # because 0 will never be a possible value
	block_row = row // 3
	block_col = col // 3

	# row and col

	for m in range(9):
		used[bo[m][col]] = 1
		used[bo[row][m]] = 1

	# block

	for m in range(3):
		for n in range(3):
			used[bo[m + block_row*3][n + block_col*3]] = 1

	return used  
	# returns list e.g [1, 1, 1, 0, 1, 0, 1, 1, 1, 1] with list[i] where i == the number that is taken/avalible

def initial_try(bo):

	"""
	Given a Sudoku puzzle, try to solve the puzzle by iterating through each
	cell and determining the possible numbers in that cell. If only one possible
	number exists, fill it in and continue on until the puzzle is stuck.
	"""

	stuck = False

	while not stuck:
		stuck = True
		# Iterate through sudoku puzzle
		for row in range(9):
			for col in range(9):
				
				used = test_valid(bo, row, col)
				
				# more than one possibility
				
				if used.count(0) != 1:
					continue

				for m in range(1, 10):
					# if current cell is empty and there is only one possibility
					# then fill in the current cell
					if bo[row][col] == m and used[m] == 0:
						s[row][col] == m
						stuck = False
						break

def ITS_solve(bo, row, col):

	"""
	Given a Sudoku puzzle, solve the puzzle by recursively performing DFS
	which tries out the possible solutions and by using backtracking (eliminating
	invalid tries and all the possible cases arising from those tries)
	"""

	# if we're on the last cell: complete the soduku by adding only possible outcome and end

	if row == 8 and col == 8:	
		used = test_valid(bo, row, col)
		if 0 in used:
			bo[row][col] = used.index(0)
		return True

	# if we're on the last column: move to start of next row

	if col == 9:
		row += 1
		col = 0

	# if current cell is 0: try other values with backtracking
	if bo[row][col] == 0:
		used = test_valid(bo, row, col)
		for i in range(1, 10):
			if used[i] == 0:
				bo[row][col] = i
				if ITS_solve(bo, row, col + 1):
					return True

		# Reached here? Then we tried 1-9 without success
		bo[row][col] = 0
		return False

	return ITS_solve(bo, row, col+1)

def main():

	generate = input("Would you like to generate new board?\n(y/n)\n:  ")
	
	if generate == "y":
		Generator.main()

	bo = get_board("SudokuPuzzles.txt")

	print_board(bo)

	user = input("Would you like to solve?\n(y/n)\n:  ")
	if user == "y":
		start_time = time.time()

		initial_try(bo)
		for line in bo:
			if 0 in line:
				ITS_solve(bo, 0, 0)
				break

		print("Solution: ")
		print("="*25)
		print_board(bo)
		print("="*25)

		print("Solved puzzle in {} seconds!".format(time.time() - start_time))


if __name__ == "__main__":
    main()




