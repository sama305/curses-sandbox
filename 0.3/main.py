import curses
import random as _r

h = 30
w = 119

screen_list = []
screen_list_hm = []

# Key-key
kk = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]




class Player:
	x = 0
	y = 0
	behind_mat = 32
	tool_mode = 0
	tool_mat = chr(32)
	can_fall = True


	def __init__(self, x, y):
		self.x = x
		self.y = y
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
				self.move_screen(stdscr, 1, 0, screen_list_hm[self.current_screen][0], 0)
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
				self.move_screen(stdscr, -1, w - 1, screen_list_hm[self.current_screen][len(screen_list_hm[self.current_screen]) - 1], w - 1)
		

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
		screen_list[self.current_screen][self.y + dir[0]][self.x + dir[1]] = self.tool_mat


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
		if len(screen_list) < screen + 1:
			screen_list.append(generate_map(y, 4))
		self.y = screen_list_hm[screen][player_start] - 1
		self.x = x
		generate_terrain(stdscr, screen_list[screen])

		# Debug info init
		stdscr.addstr(0, 112, str(self.current_screen + 1) + "/" + str(len(screen_list)))
		stdscr.addstr(0, 0, str(self.tool_mode))
		self.draw(stdscr)

	def change_mode(self, stdscr, mode):
		stdscr.addstr(0, 0, str(self.tool_mode))
		if self.tool_mode != mode:
			self.tool_mode = mode
			if mode == 0:
				self.tool_mat = chr(32)
			elif mode == 1:
				self.tool_mat = "■"









# Creates a list, where all values of the height map are placed
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

	screen_list_hm.append(foo)
	return map_gen


# Displays and addstr() all the values from generate_map()
def generate_terrain(stdscr, map_arr):
	for i in range(h):
		for j in range(w):
			stdscr.addstr(i, j, map_arr[i][j])


def main(stdscr):
	# Setup
	player = Player(0, 0)


	# h, w = stdscr.getmaxyx()

	curses.curs_set(0)
	crash = False
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)


	# Start
	player.spawn(stdscr, 0, 0, int(h / 2), 0)
	player.change_mode(stdscr, 0)

	# Update
	while not crash:
		k = stdscr.getch()

		player.draw(stdscr)

		# 0 = North   1 = East   2 = South   3 = West

		if k == ord("q"):
			crash = True
			stdscr.refresh()
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

		if player.can_fall:
			player.fall_check(stdscr)

curses.wrapper(main)