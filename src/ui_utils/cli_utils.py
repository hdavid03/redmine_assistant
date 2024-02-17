import curses
from enum import Enum
from typing import Callable
from typing import List

HLINE = f'{"-" * 120}\r\n'
LINE = lambda d: '-' * d


class PaginateDirection(Enum):
	PREV_PAGE = 0
	NEXT_PAGE = 1


class Table:

 
	def __init__(self, 
			  header: List[str],
			  rows: List[List[str]],
			  max_rows=5,
			  sep = '|',
			  alignment = "left",
			  cellsizes: List[int] = None,
			  paginate: Callable[[PaginateDirection], List[str]] = None,
			  select_item_action: Callable = None
		):
		self._validate_table(header, rows, cellsizes)
		self.max_rows = max_rows
		self.sep = sep
		self.alignment = alignment
		self.cellsizes = cellsizes
		self.paginate = paginate
		self.select_item_action = select_item_action
		self.header = None
		self.rows = None
		self.set_header(header)
		self.set_rows(rows)

	
	def set_header(self, header: List[str]):
		self.header = self._get_formatted_header(header)


	def set_rows(self, rows: List[str]):
		self.rows = self._get_formatted_rows(rows)

	
	@staticmethod
	def _validate_table(header: list, rows: list, cellsizes: list):
		if header is None or rows is None or cellsizes is None:
			raise ValueError("Header, rows or cell sizes are not specified!")
		header_length = len(header)
		if header_length != len(cellsizes):
			raise ValueError("Header and cellsizes must have the same size!")
		if all(map(lambda e: len(e) == header_length, rows)) is False:
			raise ValueError("Header and rows must have the same size!")


	def draw(self):

		status_bar = " Press 'q' to exit"
		if self.select_item_action is None:
			status_bar += " | ENTER to select item | ↑ ↓ to navigate"
		if self.paginate is None:
			status_bar += " | ← → to paginate "
		curses.wrapper(self._draw_table_wrapper,
				 status_bar, self.rows, self.header)


	def _align_cell(self, cell: str, width: int):
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


	def _get_formatted_header(self, header: List[str]):
		return f'''|{self.sep.join([self._align_cell(cell=c, width=w)
						for c,w in zip(header, self.cellsizes)])}|'''
	

	def _get_formatted_rows(self, rows: List[List[str]]):
		return [f'''|{self.sep.join([self._align_cell(cell=c, width=w)
				for c,w in zip(row, self.cellsizes)])}|''' for row in rows]


	def _draw_table_wrapper(self,
			stdscr,
			status_bar: str,
			content: List[str],
			header: str = None,
		):

		key = 0
		menu_pos = 0
		offset = 0
		start_pos = 3

		stdscr.clear()
		stdscr.refresh()

		curses.start_color()
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

		while (key != ord('q')):
			stdscr.clear()
			height, width = stdscr.getmaxyx()
			content_length = len(content)
			num_rows = height - 4
			
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
				offset -= num_rows
			elif key == curses.KEY_RIGHT:
				offset += num_rows
				
			menu_pos = min(content_length - 1, menu_pos)
			menu_pos = max(0, menu_pos)
			offset = max(0, offset)
			offset = min(content_length - num_rows, offset)
			if num_rows > content_length:
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
			for i in range(min(content_length - offset, num_rows)):
				if i == menu_pos:
					stdscr.attron(curses.color_pair(1))
					stdscr.addstr(start_pos + i, 0, content[i + offset][:width])
					stdscr.attroff(curses.color_pair(1))
				else:
					stdscr.addstr(start_pos + i, 0, content[i + offset][:width])

			# Refresh the screen
			# stdscr.move(height - 1, 0)
			stdscr.refresh()

			# Wait for next input
			key = stdscr.getch()

