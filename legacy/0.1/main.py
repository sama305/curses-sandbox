import curses
import random as _r

h = 28
w = 119

screen_list = []

class Player:
	x = 0
	y = 0
	behind_mat = 32
	tool_mode = 0
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
				self.move_screen(stdscr, 1, 0, screen_list[self.current_screen][0], 0)
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
				self.move_screen(stdscr, -1, w - 1, screen_list[self.current_screen][0], w - 1)

	def mine(self, stdscr, dir):
		if dir == 0:
			if self.y < h - 1:
				if stdscr.inch(self.y - 1, self.x) != 32:
					stdscr.addstr(self.y - 1, self.x, chr(32))
		elif dir == 1:
			if self.x < w - 1:
				if stdscr.inch(self.y, self.x + 1) != 32:
					stdscr.addstr(self.y, self.x + 1, chr(32))
		elif dir == 2:
			if self.y > 1:
				if stdscr.inch(self.y + 1, self.x) != 32:
					stdscr.addstr(self.y + 1, self.x, chr(32))
		elif dir == 3:
			if self.x > 0:
				if stdscr.inch(self.y, self.x - 1) != 32:
					stdscr.addstr(self.y, self.x - 1, chr(32))


	def build(self, stdscr, dir):
		if dir == 0:
			if self.y < h - 1:
				if stdscr.inch(self.y - 1, self.x) == 32:
					stdscr.addstr(self.y - 1, self.x, "■")
		elif dir == 1:
			if self.x < w - 1:
				if stdscr.inch(self.y, self.x + 1) == 32:
					stdscr.addstr(self.y, self.x + 1, "■")
		elif dir == 2:
			if self.y > 1 and stdscr.inch(self.y - 1, self.x) == 32:
				stdscr.addstr(self.y, self.x, "■")
				self.y = self.y - 1
				self.draw(stdscr)
		elif dir == 3:
			if self.x > 0:
				if stdscr.inch(self.y, self.x - 1) == 32:
					stdscr.addstr(self.y, self.x - 1, "■")


	def fall_check(self, stdscr):
		if stdscr.inch(self.y + 1, self.x) == 32:
			stdscr.addstr(self.y, self.x, chr(self.behind_mat))
			self.y = self.y + 1
			self.draw(stdscr)


	def move_screen(self, stdscr, screen_add, x, y, player_start):
		stdscr.clear()
		self.current_screen = self.current_screen + screen_add
		self.spawn(stdscr, self.current_screen, x, y, player_start)


	def spawn(self, stdscr, screen, x, y, player_start):
		if len(screen_list) < screen + 1:
			screen_list.append(generate_map(y, 5))
		self.y = screen_list[screen][player_start] - 1
		self.x = x
		generate_terrain(stdscr, screen_list[screen], True)

	def change_mode(self, stdscr, mode):
		if self.tool_mode != mode:
			self.tool_mode = mode
			stdscr.addstr(0, 0, str(self.tool_mode))

def generate_map(start, flatness):
	map_gen = []

	# Start location
	current_loc = start

	for i in range(w):
		rand_dir = _r.randint(-1, 1)

		if current_loc + rand_dir > h - 2:
			current_loc = h - 2
		elif current_loc + rand_dir < 0:
			current_loc = 0
		else:
			if i % flatness == 0:
				current_loc = current_loc + rand_dir

		map_gen.append(current_loc)

	return map_gen


def generate_terrain(stdscr, map_arr, fill):
	for i in range(len(map_arr)):
		stdscr.addstr(map_arr[i], i, "#")

		if (fill == True):
			len_under = h - map_arr[i]

			surface_mat = "░"
			for j in range(len_under):
				if j > 20:
					surface_mat = "█"
				elif j > 14:
					surface_mat = "▓"
				elif j > 7:
					surface_mat = "▒"

				stdscr.addstr(map_arr[i] + j + 1, i, surface_mat)


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
		elif k == curses.KEY_UP:
			player.move(stdscr, 0)
		elif k == curses.KEY_RIGHT:
			player.move(stdscr, 1)
		elif k == curses.KEY_DOWN:
			player.move(stdscr, 2)
		elif k == curses.KEY_LEFT:
			player.move(stdscr, 3)
		elif k == ord("w"):
			if player.tool_mode == 0:
				player.mine(stdscr, 0)
			elif player.tool_mode == 1:
				player.build(stdscr, 0)
		elif k == ord("d"):
			if player.tool_mode == 0:
				player.mine(stdscr, 1)
			elif player.tool_mode == 1:
				player.build(stdscr, 1)
		elif k == ord("s"):
			if player.tool_mode == 0:
				player.mine(stdscr, 2)
			elif player.tool_mode == 1:
				player.build(stdscr, 2)
		elif k == ord("a"):
			if player.tool_mode == 0:
				player.mine(stdscr, 3)
			elif player.tool_mode == 1:
				player.build(stdscr, 3)
		elif k == ord("1"):
			player.change_mode(stdscr, 0)
		elif k == ord("2"):
			player.change_mode(stdscr, 1)

		if player.can_fall:
			player.fall_check(stdscr)

curses.wrapper(main)