import curses
from enum import Enum
from typing import Callable
from typing import List
from typing import Dict
from typing import Tuple


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
			  scrollable = True,
			  sep = '|',
			  alignment = "left",
			  cellsizes: List[int] = None,
			  paginate: Callable[[int], List[str]] = None,
			  select_item_action: Callable = None
		):
		self.__validate_table(header, rows, cellsizes)
		self.sep = sep
		self.scrollable = scrollable
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
		self.header = self.__get_formatted_header(header)


	def set_rows(self, rows: List[str]):
		self.rows = self.__get_formatted_rows(rows)


	@staticmethod
	def __validate_table(header: list, rows: list, cellsizes: list):
		if header is None or rows is None or cellsizes is None:
			raise ValueError("Header, rows or cell sizes are not specified!")
		header_length = len(header)
		if header_length != len(cellsizes):
			raise ValueError("Header and cellsizes must have the same size!")
		if all(map(lambda e: len(e) == header_length, rows)) is False:
			raise ValueError("Header and rows must have the same size!")


	def draw(self):
		status_bar = " Press 'q' to exit"
		if self.select_item_action is not None:
			status_bar += " | ENTER to select item | ↑ ↓ to navigate"
		if self.paginate is not None:
			status_bar += " | ← → to paginate "
		curses.wrapper(self.__draw_table_wrapper, status_bar)


	def __align_cell(self, cell: str, width: int):
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


	def __get_formatted_header(self, header: List[str]):
		return f'''|{self.sep.join([self.__align_cell(cell=c, width=w)
						for c,w in zip(header, self.cellsizes)])}|'''
	

	def __get_formatted_rows(self, rows: List[List[str]]):
		return [f'''|{self.sep.join([self.__align_cell(cell=c, width=w)
				for c,w in zip(row, self.cellsizes)])}|''' for row in rows]


	def __draw_table_wrapper(self,
			stdscr,
			status_bar: str,
		):
		self.__draw(stdscr, self.header, self.rows, status_bar)


	def __init_table(self, stdscr):
		self.offset = 0
		self.menu_pos = 0
		stdscr.clear()
		stdscr.refresh()
		curses.start_color()
		curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
 

	def __get_page_num(self):	
		return self.offset // self.num_rows + 1

 
	def __pagination(self):
		if self.paginate is not None and \
			self.offset + self.num_rows >= self.content_length and \
			self.content_length < self.max_length:
			self.rows += self.__get_formatted_rows(self.paginate(self.content_length))
			self.content_length = len(self.rows)


	def __menu_pos_overflow(self):
		return self.menu_pos == self.last_pos \
			   and self.num_rows + self.offset != self.content_length \
			   and self.paginate is not None


	def __set_actual_pos_and_offset(self, key: int):
		if key == curses.KEY_DOWN:
			if self.__menu_pos_overflow() is True:
				if self.scrollable is True:
					self.offset += 1
			else:
				self.menu_pos += 1
		elif key == curses.KEY_UP:
			if self.menu_pos == 0 and self.scrollable is True:
				self.offset -= 1
			else:
				self.menu_pos -= 1
		elif key == curses.KEY_LEFT:
			self.offset -= self.num_rows
		elif key == curses.KEY_RIGHT:
			self.offset += self.num_rows


	def __get_formatted_content(self, content: Dict[str, Tuple[str, bool]], width):
		return [k.rjust(width)[:width] + ": " + v.ljust(width)[:width]
		  if len(v) != 0 else k.center(width)[:width] for k, v in content.items()]

	
	def __draw_entry_content(self, stdscr, entry: dict, width: int):
		header = entry.pop("header")
		content = self.__get_formatted_content(entry, width)
		self.__draw_entry(stdscr, header, content, " Press 'q' to exit")

	
	def __draw(self, stdscr, header: str, content: List[str], status_bar: str):
		key = 0
		start_pos = 3
		self.__init_table(stdscr)
		while key != ord('q'):
			stdscr.clear()
			height, width = stdscr.getmaxyx()
			self.content_length = len(content)
			self.num_rows = height - 4
			self.last_pos = height - 2 - start_pos

			if self.select_item_action is not None and key == 10:
				actual_item_id = self.rows[self.menu_pos + self.offset].split('|')[1].strip()
				entry = self.select_item_action(actual_item_id)
				self.__draw_entry_content(stdscr, entry, width // 2)
			else:
				self.__set_actual_pos_and_offset(key)
				
			self.offset = min(self.content_length - 1, self.offset)
			self.offset = max(0, self.offset)
			if self.num_rows > self.content_length:
				self.offset = 0
			self.menu_pos = min(self.content_length - self.offset - 1, self.menu_pos)
			self.menu_pos = max(0, self.menu_pos)

			# Render header
			stdscr.addstr(0, 0, LINE(min(len(header), width)))
			stdscr.addstr(1, 0, self.header[:width])
			stdscr.addstr(2, 0, LINE(min(len(header), width)))

			self.__pagination()

			# Print self.rows
			for i in range(min(self.content_length - self.offset, self.num_rows)):
				if i == self.menu_pos:
					stdscr.attron(curses.color_pair(1))
					stdscr.addstr(start_pos + i, 0, content[i + self.offset][:width])
					stdscr.attroff(curses.color_pair(1))
				else:
					stdscr.addstr(start_pos + i, 0, content[i + self.offset][:width])

			# Render status bar
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(height - 1, 0, f"{status_bar} | page: {self.__get_page_num()} "[:width])
			stdscr.attroff(curses.color_pair(1))
			
			# Refresh the screen
			stdscr.refresh()

			# Wait for next input
			key = stdscr.getch()

	
	def __draw_entry(self, stdscr, header: str, content: List[str], status_bar: str):
		key = 0
		start_pos = 3
		self.__init_table(stdscr)
		while key != ord('q'):
			stdscr.clear()
			height, width = stdscr.getmaxyx()
			self.content_length = len(content)
			self.num_rows = height - 4
			self.last_pos = height - 2 - start_pos
			self.__set_actual_pos_and_offset(key)
			self.offset = min(self.content_length - 1, self.offset)
			self.offset = max(0, self.offset)

			if self.num_rows > self.content_length:
				self.offset = 0

			self.menu_pos = min(self.content_length - self.offset - 1, self.menu_pos)
			self.menu_pos = max(0, self.menu_pos)

			# Render header
			stdscr.addstr(0, 0, LINE(min(len(header), width)))
			stdscr.addstr(1, 0, self.header[:width])
			stdscr.addstr(2, 0, LINE(min(len(header), width)))

			# Print self.rows
			for i in range(min(self.content_length - self.offset, self.num_rows)):
				if i == self.menu_pos:
					stdscr.attron(curses.color_pair(1))
					stdscr.addstr(start_pos + i, 0, content[i + self.offset][:width])
					stdscr.attroff(curses.color_pair(1))
				else:
					stdscr.addstr(start_pos + i, 0, content[i + self.offset][:width])

			# Render status bar
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(height - 1, 0, f"{status_bar} | page: {self.__get_page_num()} "[:width])
			stdscr.attroff(curses.color_pair(1))
			
			# Refresh the screen
			stdscr.refresh()

			# Wait for next input
			key = stdscr.getch()

