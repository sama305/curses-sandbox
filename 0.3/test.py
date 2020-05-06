import curses
import math
import random as _r

h = 30
w = 119

def generate_map(start, flatness):
	# Initialize map layout
	map_gen = []
	for i in range(h):
		map_gen.append([chr(32)] * w)

	# Start location
	current_loc = start

	foo = []
	for i in range(w):
		rand_dir = _r.randint(-1, 1)

		if current_loc + rand_dir > h - 2:
			current_loc = h - 2
		elif current_loc + rand_dir < 0:
			current_loc = 0
		else:
			if i % flatness == 0:
				current_loc = current_loc + rand_dir

		foo.append(current_loc)

	#for i in range(h):
	for i in range(len(foo)):
		map_gen[foo[i]][i] = "#"

		# Filling up underneath each point
		surface_mat = "░"
		for j in range(h - foo[i] - 1):
			if j > 20:
				surface_mat = "█"
			elif j > 14:
				surface_mat = "▓"
			elif j > 7:
				surface_mat = "▒"
			map_gen[j + foo[i] + 1][i] = surface_mat

	return map_gen

def generate_terrain(stdscr, map_arr):
	for i in range(h):
		for j in range(w):
			stdscr.addstr(i, j, map_arr[i][j])


def main(stdscr):
	curses.curs_set(0)
	crash = False
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

	the_map = generate_map(15, 1)

	generate_terrain(stdscr, the_map)

	while not crash:
		k = stdscr.getch()

		if k == ord("q"):
			crash = True

curses.wrapper(main)
