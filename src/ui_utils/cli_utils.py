import curses
from typing import Callable
from typing import List

HLINE = f'{"-" * 120}\r\n'
LINE = lambda d: '-' * d


class Table:

 
	def __init__(self, 
			  max_rows=5,
			  sep = '|',
			  alignment = "left",
			  header: List[str] = None,
			  rows: List[str] = None,
			  cellsizes: List[int] = None,
			  paginate: Callable = None,
			  select_item_action:  Callable = None
		):
		self.max_rows = max_rows
		self.sep = sep
		self.alignment = alignment
		self.header = header
		self.rows = rows
		self.cellsizes = cellsizes
		self.paginate = paginate
		self.select_item_action = select_item_action

	
	def _validate_table(self):
		if self.header is None or self.rows is None or self.cellsizes is None:
			raise ValueError("Header, rows or cell sizes are not specified!")
		header_length = len(self.header)
		if header_length != len(self.cellsizes):
			raise ValueError("Header and cellsizes must have the same size!")
		if all(map(lambda e: len(e) == header_length, self.rows)) is False:
			raise ValueError("Header and rows must have the same size!")


	def draw(self):

		self._validate_table()

		def align(cell: str, width: int):
			alignment = self.alignment.lower()
			if alignment == "left":
				return cell.ljust(width)[:width]
			elif alignment == "right":
				return cell.rjust(width)[:width]
			elif alignment == "center":
				return cell.center(width)[:width]
			else:
				print(f'Wrong alignment parameter used: {self.alignment}')
				print("Only 'left', 'right' or 'center' parameter is allowed")
				print("Left alignment is used by default")
				return cell.ljust(width)[:width]

		header = f'''|{self.sep.join([align(cell=c, width=w)
						for c,w in zip(self.header, self.cellsizes)])}|'''
		rows   = [f'''|{self.sep.join([align(cell=c, width=w)
						for c,w in zip(row, self.cellsizes)])}|'''
				  for row in self.rows]
		status_bar = " Press 'q' to exit"
		if self.select_item_action is None:
			status_bar += " | ENTER to select item | ↑ ↓ to navigate"
		if self.paginate is None:
			status_bar += " | ← → to paginate "
		curses.wrapper(Table._draw_table_wrapper,
				 status_bar, rows, header, self.paginate, self.select_item_action)

	
	@staticmethod
	def _draw_table_wrapper(
			stdscr,
			status_bar: str,
			content: List[str],
			header: str = None,
			paginate: Callable = None,
			select_item_action: Callable = None
		):

		key = 0
		menu_pos = 0
		offset = 0
		start_pos = 3

		# Clear and refresh the screen for a blank canvas
		stdscr.clear()
		stdscr.refresh()

		# Start colors in curses
		curses.start_color()
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

		while (key != ord('q')):
			stdscr.clear()
			height, width = stdscr.getmaxyx()
			content_length = len(content)
			
			if key == curses.KEY_DOWN:
				if menu_pos == height - 2 - start_pos:
					offset += 1
				else:
					menu_pos += 1
			elif key == curses.KEY_UP:
				if menu_pos == 0:
					offset -= 1
				else:
					menu_pos -= 1
			elif key == curses.KEY_LEFT:
				offset -= 1
			elif key == curses.KEY_RIGHT:
				offset += 1
				
			menu_pos = min(content_length - 1, menu_pos)
			menu_pos = max(0, menu_pos)
			offset = max(0, offset)
			if content_length > height - 4:
				offset = min(content_length - offset, offset)
			else:
				offset = 0

			# Render status bar
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(height - 1, 0, status_bar[:width])
			stdscr.attroff(curses.color_pair(1))

			# Render header
			stdscr.addstr(0, 0, LINE(min(len(header), width)))
			stdscr.addstr(1, 0, header[:width])
			stdscr.addstr(2, 0, LINE(min(len(header), width)))

			# Print content
			for i in range(min(content_length, height - 4)):
				if i == menu_pos:
					stdscr.attron(curses.color_pair(1))
					stdscr.addstr(start_pos + i, 0, content[i + offset][:width])
					stdscr.attroff(curses.color_pair(1))
				else:
					stdscr.addstr(start_pos + i, 0, content[i + offset][:width])

			# Refresh the screen
			stdscr.move(height - 1, 0)
			stdscr.refresh()

			# Wait for next input
			key = stdscr.getch()

