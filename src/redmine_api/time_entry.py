from ui_utils.datetime_utils import estimate_time_delta_from_now
from ui_utils.cli_utils import HLINE


class TimeEntry:
    

    def __init__(self, parameters: dict):
        self.id = parameters.get("id")
        self.project = parameters.get("project")
        self.issue = parameters.get("issue")
        self.user = parameters.get("user")
        self.activity = parameters.get("activity")
        self.hours = parameters.get("hours")
        self.comments = parameters.get("comments")
        self.spent_on = parameters.get("spent_on")
        self.created_on = parameters.get("created_on")
        self.updated_on = parameters.get("updated_on")


    def __str__(self):
        text  = HLINE
        text +=	f'Comments: {self.comments}\r\nadded by {self.user["name"]} '
        text +=	f'{estimate_time_delta_from_now(self.created_on)}\r\n'
        text += HLINE
        text += 'Details:\r\n'
        text += f'{"ID:":>15} {self.id:<26}'
        text += f'{"Issue ID:":>15} {self.issue["id"]}\r\n'
        text += f'{"Project:":>15} {self.project["name"][:26]:<26}'
        text += f'{"Activity:":>15} {self.activity["name"]}\r\n'
        text += f'{"Date:":>15} {self.spent_on:<26}'
        text += f'{"Spent hours:":>15} {self.hours}\r\n'
        text += HLINE
        return text


    def get_as_row(self):
        row  = f'|{self.id:^7}'
        row += f'|{self.project["name"][:25]:25}'
        row += f'|{self.activity["name"][:10]:^10}'
        row += f'|{self.issue["id"]:^7}'
        row += f'|{self.comments[:32]:32}'
        row += f'|{self.hours:^5}'
        row += f'|{self.spent_on:^10}'
        row += f'|{self.user["name"][:15]:^15}|'
        return row

    def get_row(self):
        return [
			str(self.id), self.project.get("name"),
			self.activity.get("name"), str(self.issue.get("id")),
			self.comments, str(self.hours),
			self.spent_on, self.user.get("name")
		]

		
    @staticmethod
    def table_time_entries(time_entries: list):
        text  = HLINE
        text += f'|{"ID":^7}|{"Project":^25}|{"Activity":^10}'
        text += f'|{"Issue":^7}|{"Comment":^32}'
        text +=	f'|{"Hours":^5}'
        text += f'|{"Date":^10}|{"User":^15}|\r\n'
        text += HLINE
        print(text, end="")
        for time_entry in time_entries:
            print(time_entry.get_as_row())

             
    @staticmethod
    def get_time_entries_from_json(time_entries: list):
        return [TimeEntry(time_entry) for time_entry in time_entries]

