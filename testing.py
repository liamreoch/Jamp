#!/usr/bin/python

import sys, os, curses, traceback, string, time, subprocess
screen_height, screen_width = 0, 0
pad_height, pad_width = 0, 0
y, x = 2, 1
pad = object
down = 0
children, contents, directory = [], [], []
pad_position = 0
content_height = -1
content_position = 0

def main(screen):
	global screen_height, screen_width
	global pad_height, pad_width
	global y, x, pad, down
	global directory, pad_position
	global content_height, start_contents
	global position, page

	screen_height, screen_width = screen.getmaxyx()

	# create pad with space allowance for statuses underneath
	pad = curses.newpad(screen_height - 4, screen_width)
	pad.scrollok(1)
	pad.idlok(1)

	# temporary colouring for pad
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
	pad.bkgd(1, curses.color_pair(1))

	# get dimensions of pad
	pad_height, pad_width = pad.getmaxyx()


	audio_types = ['.mp3', '.mp4', '.wav']

	# print heading, border, status placeholders
	screen.addstr(0, 1, 'testing ground', curses.A_BOLD)
	screen.addstr(1, 1, ('-' * (screen_width - 2)))
	screen.addstr(screen_height - 2, 1, 'placeholder', curses.A_BOLD)
	screen.addstr(screen_height - 1, 1, 'placeholder', curses.A_BOLD)

	populate()
	screen.refresh()
	refresh_pad()
	screen.move(y, x)

	screen.nodelay(1)
	while True:
		key = screen.getch()
		if key == 113: # q
			break
		else:
			move_cursor(key)
			curses.doupdate()
		time.sleep(0.1)

def populate(content_position = 0):
		global contents, pad, pad_height, content_height, directory, down
		# dummy data for directory
		children = (['..', 'apple', 'banana', 'cats', 'dogs', 'every', 'flan', 'goes', 'happy', 'indigo', 'jack', 'kalamari', 'llama', 'magic', 'nonsense', 'opening', 'parachute', 'quickly', 'rusted', 'stolen', 'trampoline', 'universe', 'valour', 'water', 'xylophonic', 'younger', 'zebra'])
		directory = children + contents

		try:
			# fill pad with items from directory
			for item in directory[content_position:pad_height]:
				pad.addstr(down, 1, item)
				down += 1
				content_height += 1
			pad.setscrreg(0, pad_height - 1)
		except:
			traceback.print_exc()

def refresh_pad():
	global pad_position, screen_height, screen_width
	pad.refresh(0, 0, 2, 0, screen_height - 3, screen_width - 1)

def move_cursor(key):
	global y, x, content_height, content_position
	global pad, screen_height, screen_width
	global down, screen, directory, start_contents
	global pad_position, pad_height, pad_width, content_position
	y, x = screen.getyx()
	y_prev, x_prev = y, x
	pad_height, pad_width = pad.getmaxyx()
	# pad_height -= 1
	if key == curses.KEY_DOWN:
		if pad_position < content_height:
			pad_position += 1
			y += 1
			content_position += 1
		elif pad_height < len(directory) and content_position < len(directory) - 1:
			pad.scroll(1)
			pad.addstr(pad_height - 2, 1, directory[content_position + 1])
			content_position += 1
		refresh_pad()

	elif key == curses.KEY_UP:
		if y > 2 and pad_position > 0:
			pad_position -= 1
			y -= 1
			content_position -= 1
		elif pad_height < len(directory) and pad_position == 0 and content_position > 0:
			pad.scroll(-1)
			pad.addstr(0, 1, directory[content_position - 1])
			content_position -= 1
			refresh_pad()

	elif key == curses.KEY_RESIZE:
		screen_height, screen_width = screen.getmaxyx()
		screen.clear()
		curses.resizeterm(screen_height, screen_width)
		content_position = 0
		content_height = -1
		pad_position = 0
		down = 0
		y, x = pad_height, 1
		pad.resize(screen_height - 3, screen_width)
		main(screen)

	stats()
	#screen.chgat(y, x, screen_width - 1, curses.A_STANDOUT)
	screen.move(y, x)
	screen.refresh()

def clear_line(y_line):
	screen.move(y_line, 0)
	screen.clrtoeol()
	screen.move(y, x)

def stats():
	# screen.move(0, 15)
	# screen.clrtoeol()
	# screen.move(y, x)
	# screen.addstr(0, max_x - 14, ("contents: " + str(content_height)))
	# screen.addstr(0, 20, ("[screen height: " + str(screen_height) + "]"))
	# screen.addstr(0, 39, ("[pad height: " + str(pad_height) + "]"))
	screen.addstr(0, 55, ("[y: " + str(y) + "]"))
	# screen.addstr(0, 62, ("[pad_pos: " + str(pad_position) + "]"))
	screen.addstr(0, 50, ("[content: " + str(content_position) + "]"))
	# screen.addstr(0, 88, ("[dir length: " + str(len(directory)) + "]"))


if __name__=='__main__':
	try:
		screen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(1)
		screen.keypad(1)
		main(screen)
		screen.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
	except:
		# In event of error, restore terminal to sane state.
		screen.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
		traceback.print_exc()
