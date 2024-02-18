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
			  max_length = None,
			  sep = '|',
			  alignment = "left",
			  cellsizes: List[int] = None,
			  paginate: Callable[[int], List[str]] = None,
			  select_item_action: Callable = None
		):
		self._validate_table(header, rows, cellsizes)
		self.sep = sep
		self.alignment = alignment
		self.cellsizes = cellsizes
		self.paginate = paginate
		self.max_length = max_length
		self.select_item_action = select_item_action
		self.offset = 0
		self.set_header(header)
		self.set_rows(rows)
		self.content_length = len(self.rows)

	
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
		curses.wrapper(self._draw_table_wrapper, status_bar)


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
		):

		key = 0
		self.offset = 0
		self.menu_pos = 0
		start_pos = 3

		stdscr.clear()
		stdscr.refresh()

		curses.start_color()
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

		while key != ord('q'):
			stdscr.clear()
			height, width = stdscr.getmaxyx()
			self.content_length = len(self.rows)
			self.num_rows = height - 4
			self.last_pos = height - 2 - start_pos

			self._set_actual_pos_and_offset(key)
				
			self.offset = min(self.content_length - 1, self.offset)
			self.offset = max(0, self.offset)
			if self.num_rows > self.content_length:
				self.offset = 0
			self.menu_pos = min(self.content_length - self.offset - 1, self.menu_pos)
			self.menu_pos = max(0, self.menu_pos)

			# Render header
			stdscr.addstr(0, 0, LINE(min(len(self.header), width)))
			stdscr.addstr(1, 0, self.header[:width])
			stdscr.addstr(2, 0, LINE(min(len(self.header), width)))

			self._pagination()

			# Print self.rows
			for i in range(min(self.content_length - self.offset, self.num_rows)):
				if i == self.menu_pos:
					stdscr.attron(curses.color_pair(1))
					stdscr.addstr(start_pos + i, 0, self.rows[i + self.offset][:width])
					stdscr.attroff(curses.color_pair(1))
				else:
					stdscr.addstr(start_pos + i, 0, self.rows[i + self.offset][:width])

			# Render status bar
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(height - 1, 0, f"{status_bar} | self.offset: {self.offset}"[:width])
			stdscr.attroff(curses.color_pair(1))
			
			# Refresh the screen
			stdscr.refresh()

			# Wait for next input
			key = stdscr.getch()
	

	def _pagination(self):
		if self.paginate is not None and \
			self.offset + self.num_rows >= self.content_length and \
			self.content_length < self.max_length:
			self.rows += self._get_formatted_rows(self.paginate(self.content_length))
			self.content_length = len(self.rows)


	def _menu_pos_overflow(self):
		return self.menu_pos == self.last_pos and self.num_rows + self.offset != self.content_length


	def _set_actual_pos_and_offset(self, key: int):
		if key == curses.KEY_DOWN:
			if self._menu_pos_overflow() is True:
				self.offset += 1
			else:
				self.menu_pos += 1
		elif key == curses.KEY_UP:
			if self.menu_pos == 0:
				self.offset -= 1
			else:
				self.menu_pos -= 1
		elif key == curses.KEY_LEFT:
			self.offset -= self.num_rows
		elif key == curses.KEY_RIGHT:
			self.offset += self.num_rows
