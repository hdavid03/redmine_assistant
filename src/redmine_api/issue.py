from ui_utils.datetime_utils import estimate_time_delta_from_now
from ui_utils.cli_utils import HLINE
from textwrap import wrap


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
		text += f'{"ID:":>15} {self.id:<26}'
		text += f'{"Tracker:":>15} {self.tracker["name"]}\r\n'
		text += f'{"Project:":>15} {self.project["name"][:26]:<26}'
		text += f'{"Status:":>15} {self.status["name"]}\r\n'
		text += f'{"Done ratio:":>15}'
		text += f' [{str("#" * (self.done_ratio // 10)).ljust(10, ".")}{"]":<16}'
		text += f'''{"Spent hours: ".rjust(15) + str(self.spent_hours)
				if self.spent_hours is not None else ""}\r\n'''
		text += f'''{"Updated at ".rjust(15)
		+ estimate_time_delta_from_now(self.updated_on)}\r\n'''

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
		row = f'|{self.id:^7}'
		row += f'|{self.project["name"][:26]:26}'
		row += f'|{self.tracker["name"][:10]:^10}'
		row += f'|{self.status["name"][:10]:^10}'
		row += f'|{self.priority["name"][:10]:^10}'
		row += f'|{self.subject[:34]:34}'
		row += f'''|{self.assigned_to["name"][:15] 
		   if self.assigned_to is not None else "":^15}|'''
		return row

		
	@staticmethod
	def table_issues(issues: list):
		text = HLINE
		text += f'|{"ID":^7}|{"Project":^26}|{"Tracker":^10}'
		text += f'|{"Status":^10}|{"Priority":^10}'
		text +=	f'|{"Subject":^34}|{"Assignee":^15}|\r\n'
		text += HLINE
		print(text, end="")
		for issue in issues:
			print(issue.get_as_row())

	
	@staticmethod
	def get_issues_from_json(issues: list):
		return [Issue(issue) for issue in issues]