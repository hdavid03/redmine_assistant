from datetime import datetime
from textwrap import wrap


HLINE = f'{"-" * 120}\r\n'


class Issue:

	def __init__(self, parameters: dict):
		self.id = parameters.get("id")
		self.project = parameters.get("project")
		self.tracker = parameters.get("tracker")
		self.status = parameters.get("status")
		self.priority = parameters.get("priority")
		self.author = parameters.get("author")
		self.assigned_to = parameters.get("assigned_to")
		self.subject = parameters.get("subject")
		self.description = parameters.get("description")
		self.start_date = parameters.get("start_date")
		self.due_date = parameters.get("due_date")
		self.done_ratio = parameters.get("done_ratio")
		self.estimated_hours = parameters.get("estimated_hours")
		self.spent_hours = parameters.get("spent_hours")
		self.created_on = parameters.get("created_on")
		self.updated_on = parameters.get("updated_on")
		self.closed_on = parameters.get("closed_on")
		self.journals = parameters.get("journals")


	@staticmethod
	def _estimate_time_delta(time_delta: int, limit: tuple, intervals: tuple):
		est = time_delta // limit[0]
		ret = f'about {est} {intervals[0] + "s" if est > 1 else intervals[0]}' 
		left = est - est * limit[0]
		if left > limit[1] - 1:
			left = left // limit[1]
			ret += f' and {left} {intervals[1] + "s" if left > 1 else intervals[1]} ago'
		else:
			ret += " ago."
		return ret


	@staticmethod
	def _get_estimated_time_delta_string(date_str: str):
		d1 = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
		d2 = datetime.now()
		diff = d2 - d1
		if diff.days > 364:
			return Issue._estimate_time_delta(diff.days, (365, 30), ("year", "month"))
		elif diff.days > 29:
			return Issue._estimate_time_delta(diff.days, (30, 7), ("month", "week"))
		elif diff.days > 6:
			return Issue._estimate_time_delta(diff.days, (7, 1), ("week", "day"))
		elif diff.days > 1:
			return f'about {diff.days} days ago.'
		elif diff.seconds > 3599:
			return Issue._estimate_time_delta(diff.seconds, (3600, 60), ("hour", "minute"))
		elif diff.seconds > 59:
			minutes = diff.seconds // 60
			return f'about {minutes} {"minutes ago." if minutes > 1 else "minute ago."}'
		else:
			return f'''{"about " + str(diff.seconds) + " seconds ago."
				   if diff.seconds > 10 else "just now."}'''


	def __str__(self):
		text =  HLINE
		text +=	f'Subject: {self.subject}\r\nadded by {self.author["name"]} '
		text +=	f'at {self.created_on}\r\n'
		text += HLINE
		text += 'Details:\r\n'
		text += f'''{"assigned to ".rjust(15, " ") + self.assigned_to["name"]
									   if self.assigned_to is not None
									   else "nobody yet"}'''
		text += f' with {self.priority["name"]} priority\r\n'
		text += f'{"ID:":>15} {self.id:<25}'
		text += f'{"Tracker:":>15} {self.tracker["name"]}\r\n'
		text += f'{"Project:":>15} {self.project["name"]:<25}'
		text += f'{"Status:":>15} {self.status["name"]}\r\n'
		text += f'{"Done ratio:":>15}'
		text += f' [{str("#" * (self.done_ratio // 10)).ljust(10, "-")}{"]":<14}'
		text += f'''{"Spent hours: ".rjust(14) + str(self.spent_hours)
				if self.spent_hours is not None else ""}\r\n'''
		text += f'''{"Updated at ".rjust(15)
		+ self._get_estimated_time_delta_string(self.updated_on)}\r\n'''

		if self.start_date is not None:
			text += f'{"Start date:":>15} {self.start_date}\r\n'
		if self.due_date is not None:
			text += f'{"Due date:":>15} {self.due_date}\r\n'
		text += HLINE
		if self.description is not None:
			text += "Description:\r\n"
			text += "\r\n".join(wrap(self.description, 75))
		return text


	def get_as_row(self):
		row = f'{self.id:<6}'
		row += f'{self.project["name"]:<25}'
		row += f'{self.tracker["name"]:<9}'
		row += f'{self.priority["name"]:<9}'
		row += f'{self.subject:<40}'
		row += f'{self.status["name"]:<9}'
		row += f'''{self.assigned_to["name"] 
		   if self.assigned_to is not None else "":<15}'''
		row += f'''{str(self.done_ratio) + "%"
		   if self.done_ratio is not None else ""}'''
		return row

		
	@staticmethod
	def table_issues(issues: list):
		text = HLINE
		text += f'{"|ID".ljust(6)}{"Project".ljust(24)}{"Tracker".ljust(10)}'
		text += f'{"Priority".ljust(10)}{"Subject".ljust(10)}'
		text +=	f'{"Status".ljust(10)}{"Author".ljust(15)}'
		text +=	f'{"Done ratio".ljust(10)}|\r\n'
		text += HLINE
		print(text)
		for issue in issues:
			print(issue.get_as_row())

	
	@staticmethod
	def get_issues_from_json(issues: list):
		return [Issue(issue) for issue in issues]