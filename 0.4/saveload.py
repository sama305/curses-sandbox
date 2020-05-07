import io
import os
import curses
import pickle

def saveToFile(stdscr, name, slraw, slhm, slobj, plr):
	# Overwriting file
	stdscr.addstr(0, 50, "Saving...")

	file = "Saves/" + name

	if os.path.exists(file):
		os.remove(file + "/save_raw.txt")
		os.remove(file + "/save_hm.txt")
		os.remove(file + "/save_obj.txt")
		os.remove(file + "/save_plr.p")
	else:
		os.mkdir(file)

	with io.open(file + "/save_raw.txt", "w", encoding="utf-8") as fp:
		fp.write(str(slraw))
	fp.close()
	with io.open(file + "/save_hm.txt", "w", encoding="utf-8") as fp:
		fp.write(str(slhm))
	fp.close()
	with io.open(file + "/save_obj.txt", "w", encoding="utf-8") as fp:
		fp.write(str(slobj))
	fp.close()
	pickle.dump(plr, open(file + "/save_plr.p", "wb"))

	stdscr.addstr(0, 50, "Saved to: /Saves/" + name + "/")


def loadFromFile(name):
	loaded_slraw = []
	loaded_slhm = []
	loaded_slobj = []
	loaded_player = None

	file = "Saves/" + name

	# If you can't load the file, return nothing
	if not os.path.exists(file):
		return loaded_slraw, loaded_slhm, loaded_slobj

	with io.open(file + "/save_raw.txt", "r", encoding="utf-8") as fp:
		loaded_slraw = eval(fp.readline())
	fp.close()
	with io.open(file + "/save_hm.txt", encoding="utf-8") as fp:
		loaded_slhm = eval(fp.readline())
	fp.close()
	with io.open(file + "/save_obj.txt", encoding="utf-8") as fp:
		loaded_slobj = eval(fp.readline())
	fp.close()
	loaded_player = pickle.load(open(file + "/save_plr.p", "rb"))
	print(loaded_player.x)

	return loaded_slraw, loaded_slhm, loaded_slobj