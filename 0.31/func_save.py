import io
import os
import curses

def saveToFile(stdscr, name, slraw, slhm, slobj):
	# Overwriting file
	stdscr.addstr(0, 50, "Saving...")
	if os.path.exists("Saves/" + name):
		os.remove("Saves/" + name + "/save_raw.txt")
		os.remove("Saves/" + name + "/save_hm.txt")
	else:
		os.mkdir("Saves/" + name)

	with io.open("Saves/" + name + "/save_raw.txt", "w", encoding="utf-8") as fp:
		fp.write(str(slraw))
	fp.close()
	with io.open("Saves/" + name + "/save_hm.txt", "w", encoding="utf-8") as fp:
		fp.write(str(slhm))
	fp.close()
	with io.open("Saves/" + name + "/save_obj.txt", "w", encoding="utf-8") as fp:
		fp.write(str(slobj))
	fp.close()

	stdscr.addstr(0, 50, "Saved to: /Saves/" + name + "/")


def loadFromFile(name):
	loaded_slraw = []
	loaded_slhm = []
	loaded_slobj = []

	# If you can't load the file, return nothing
	if not os.path.exists("Saves/" + name):
		return loaded_slraw, loaded_slhm, loaded_slobj

	with io.open("Saves/" + name + "/save_raw.txt", "r", encoding="utf-8") as fp:
		loaded_slraw = eval(fp.readline())
	fp.close()
	with io.open("Saves/" + name + "/save_hm.txt", encoding="utf-8") as fp:
		loaded_slhm = eval(fp.readline())
	fp.close()
	with io.open("Saves/" + name + "/save_obj.txt", encoding="utf-8") as fp:
		loaded_slobj = eval(fp.readline())
	fp.close()

	return loaded_slraw, loaded_slhm, loaded_slobj