import curses
import random as _r
import saveload as sl
import os
import math

h = 30
w = 119

slraw = []
slhm = []
slobj = []

game_title = "Welcome to curses-sandbox!"
author = "Samuel Anderson"

# slraw = screen list raw - has all raw data of terrain textures/characters
# slhm = screen list height map- has only heights as list
# slobj = screen list object - holds all values and positions for special objects

# Key-key
kk = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


class Player:
	x = 0
	y = 0
	behind_mat = 32
	tool_mode = 0
	tool_mat = chr(32)
	can_fall = True
	current_save = "none"


	def __init__(self, x, y):
		self.x = x
		self.y = int(h/2)
		self.current_screen = 0


	def draw(self, stdscr):
		stdscr.addstr(self.y, self.x, "☺")


	def move(self, stdscr, dir):
		if dir == 0:
			print("Go up")
		elif dir == 1:
			if self.x < w - 1:
				# Moving Right
				if stdscr.inch(self.y, self.x + 1) == 32:
					stdscr.addstr(self.y, self.x, chr(self.behind_mat))
					self.x = self.x + 1
					self.draw(stdscr)
				# Moving Up Right
				elif stdscr.inch(self.y - 1, self.x + 1) == 32:
					stdscr.addstr(self.y, self.x, chr(self.behind_mat))
					self.x = self.x + 1
					self.y = self.y - 1
					self.draw(stdscr)
			else:
				self.move_screen(stdscr, 1, 0, slhm[self.current_screen][0], 0)
		elif dir == 2:
			print("Go down")
		elif dir == 3:
			if self.x > 0:
				# Moving Left
				if stdscr.inch(self.y, self.x - 1) == 32 and self.x > 0:
					stdscr.addstr(self.y, self.x, chr(self.behind_mat))
					self.x = self.x - 1
					self.draw(stdscr)
				# Moving Up Left
				elif stdscr.inch(self.y - 1, self.x - 1) == 32 and self.x > 0:
					stdscr.addstr(self.y, self.x, chr(self.behind_mat))
					self.x = self.x - 1
					self.y = self.y - 1
					self.draw(stdscr)
			elif self.current_screen > 0:
				self.move_screen(stdscr, -1, w - 1, slhm[self.current_screen][len(slhm[self.current_screen]) - 1], w - 1)
		

	def tool_use(self, stdscr, dir):
		if dir[0] == 1:
			# Check if plr is at least 1 tile below height
			if self.y > h - 1:
				return
		elif dir[0] == -1:
			# Check if plr is at least 1 tile above 0
			if self.y < 1:
				return

		if dir[1] == 1:
			# Check if plr is at least 1 tile left of width
			if self.x > w - 2:
				return
		elif dir[1] == -1:
			# Check if plr is at least 1 tile right of 0
			if self.x < 1:
				return

		# Specifically for building down
		if self.tool_mode == 1 and dir == (1, 0):
			if stdscr.inch(self.y - 1, self.x) == 32:
				self.y = self.y - 1
				self.draw(stdscr)
			else:
				return

		stdscr.addstr(self.y + dir[0], self.x + dir[1], self.tool_mat)
		slraw[self.current_screen][self.y + dir[0]][self.x + dir[1]] = self.tool_mat

	def manual_tool_use(self, stdscr, tool, _dir):
		previous_tool = self.tool_mode
		self.tool_mode = tool
		self.tool_use(stdscr, _dir)
		self.tool_mode = previous_tool


	# Makes player fall if empty tile below
	def fall_check(self, stdscr):
		if stdscr.inch(self.y + 1, self.x) == 32:
			stdscr.addstr(self.y, self.x, chr(self.behind_mat))
			self.y = self.y + 1
			self.draw(stdscr)


	# Moves play area forward or backward by certain amount of screens
	def move_screen(self, stdscr, screen_add, x, y, player_start):
		stdscr.clear()
		self.current_screen = self.current_screen + screen_add
		self.spawn(stdscr, self.current_screen, x, y, player_start)


	def spawn(self, stdscr, screen, x, y, player_start):
		if len(slraw) < screen + 1:
			# Standard gen
			slraw.append(generate_map(self.y+1))
		if self.y <= slhm[screen][player_start]:
			self.y = slhm[screen][player_start] - 1
		self.x = x
		generate_terrain(stdscr, slraw[screen])

		# Debug info init
		stdscr.addstr(0, 112, str(self.current_screen + 1) + "/" + str(len(slraw)))
		stdscr.addstr(0, 0, str(self.tool_mode))
		self.draw(stdscr)


	def change_mode(self, stdscr, mode):
		stdscr.addstr(0, 0, str(self.tool_mode))
		if self.tool_mode != mode:
			self.tool_mode = mode
			if mode == 0:
				self.tool_mat = chr(32)
			elif mode == 1:
				self.tool_mat = "█"








# Creates a list, where all values of the height map are placed
def generate_map(start):
	flatness = _r.randint(1,7)
	# Initialize map/obj layout
	map_gen = []
	obj_gen = []
	for i in range(h):
		map_gen.append([chr(32)] * w)
	# Creating obj screen list
	for i in range(h):
		obj_gen.append([None] * w)
	slobj.append(obj_gen)

	# Start location
	current_loc = start

	foo = []
	foo.append(current_loc)
	for i in range(w-1):
		rand_dir = _r.randint(-1, 1)

		if current_loc + rand_dir > h - 2:
			current_loc = h - 2
		elif current_loc + rand_dir < 0:
			current_loc = 0
		else:
			if i % flatness == 0:
				current_loc = current_loc + rand_dir
		
		foo.append(current_loc)

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

	slhm.append(foo)
	return map_gen


# Displays and addstr() all the values from generate_map()
def generate_terrain(stdscr, map_arr):
	for i in range(h):
		for j in range(w):
			stdscr.addstr(i, j, map_arr[i][j])



def start_game(stdscr):
	stdscr.clear()
	game_started = True
	player.spawn(stdscr, 0, 0, int(h / 2), 0)
	player.change_mode(stdscr, 0)

menu_options = ["Start new game"]
def initialize_menu():
	file_list = os.listdir("Saves/")
	for f in file_list:
		menu_options.append(f)


player = Player(0,0)

def main(stdscr):
	game_started = False
	# h, w = stdscr.getmaxyx()

	curses.curs_set(0)
	crash = False
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)


	# MENU CODE

	selected = 0
	initialize_menu()
	while not crash and not game_started:

		stdscr.addstr(1, math.floor(w / 2) - math.floor(len(game_title) / 2), game_title)
		stdscr.addstr(h - 2, math.floor(w / 2) - math.floor(len("By " + author) / 2), "By " + author)

		for i in range(len(menu_options)):
			current_option = menu_options[i]
			if i != 0:
				current_option = "Load: " + current_option

			if i == selected:
				stdscr.addstr(15 + i, math.floor(w / 2) - math.floor(len(current_option) / 2), current_option, curses.color_pair(1))
			else:
				stdscr.addstr(15 + i, math.floor(w / 2) - math.floor(len(current_option) / 2), current_option)


		k = stdscr.getch()
		if k == ord("q"):
			crash = True
		elif k == curses.KEY_UP:
			selected = selected - 1
			if selected < 0:
				selected = len(menu_options) - 1
		elif k == curses.KEY_DOWN:
			selected = selected + 1
			if selected > len(menu_options) - 1:
				selected = 0
		# Select option
		elif k == 10:
			if selected != 0:
				global slraw
				global slhm
				global slobj

				slraw, slhm, slobj = sl.loadFromFile(menu_options[selected])
				player.current_save = menu_options[selected]
			else:
				player.current_save = "save_" + str(len(os.listdir("Saves/")) + 1)
			game_started = True
			start_game(stdscr)





	# Update
	while not crash and game_started:
		k = stdscr.getch()

		player.draw(stdscr)

		if k == ord("q"):
			crash = True
			stdscr.refresh()
		# !!!Change to tuple input system
		elif k == ord("w"):
			player.move(stdscr, 0)
		elif k == ord("d"):
			player.move(stdscr, 1)
		elif k == ord("s"):
			player.move(stdscr, 2)
		elif k == ord("a"):
			player.move(stdscr, 3)

		# DIRECTIONAL TOOL USAGE
		# N
		elif k == 450:
			player.tool_use(stdscr, kk[0])
		# NE
		elif k == 451:
			player.tool_use(stdscr, kk[1])
		# E
		elif k == 454:
			player.tool_use(stdscr, kk[2])
		# SE
		elif k == 457:
			player.tool_use(stdscr, kk[3])
		# S
		elif k == 456:
			player.tool_use(stdscr, kk[4])
		# SW
		elif k == 455:
			player.tool_use(stdscr, kk[5])
		# W
		elif k == 452:
			player.tool_use(stdscr, kk[6])
		# NW
		elif k == 449:
			player.tool_use(stdscr, kk[7])

		# Tool switching
		elif k == ord("1"):
			player.change_mode(stdscr, 0)
		elif k == ord("2"):
			player.change_mode(stdscr, 1)
		elif k == ord("S"):
			sl.saveToFile(stdscr, player.current_save, slraw, slhm, slobj, player)

		if player.can_fall:
			player.fall_check(stdscr)


curses.wrapper(main)