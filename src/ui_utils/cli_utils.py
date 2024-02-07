
HLINE = f'{"-" * 120}\r\n'
LINE = lambda d: '-' * d


class Table:

 
	def __init__(self, 
			  max_rows=5,
			  sep = '|',
			  alignment = "left",
			  header: list = None,
			  rows: list = None,
			  cellsizes: list = None
		):
		self.max_rows = max_rows
		self.sep = sep
		self.alignment = alignment
		self.header = header
		self.rows = rows
		self.cellsizes = cellsizes
		if rows is not None and header is not None\
		and len(header) != len(rows[0]):
				raise ValueError("Header and row must have the same size!")


	def draw(self):

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
				print("Only left, right or center parameter is allowed")
				print("Left alignment is used by default")
				return cell.ljust(width)[:width]

		header = f'''|{self.sep.join([align(cell=c,width=w)
						for c,w in zip(self.header, self.cellsizes)])}|'''
		rows   = [f'''|{self.sep.join([align(cell=c,width=w)
						for c,w in zip(row, self.cellsizes)])}|'''
				  for row in self.rows]
		print(LINE(len(header)))
		print(header)
		print(LINE(len(header)))
		for row in rows:
			print(row)
		print(LINE(len(header)))
