from requests import get as http_get
from requests import post as http_post
from redmine_api.issue import Issue
from redmine_api.time_entry import TimeEntry
from ui_utils.cli_utils import Table


class RedmineApi:


	def __init__(self, user_info: dict):
		url = user_info["url"]
		if type(url) is not str:
			raise TypeError("URL is missing or not a string!")
		if url[-1] == "/":
			self.base_url = url
		else:
			self.base_url = url + "/"
		self.api_key = user_info["api_key"]
		self.header = {"X-Redmine-API-Key": self.api_key}
		self.issues_filter = None
		self.time_entries_filter = None


	def _get_api_endpoint(self, source: str, parameters: dict=None):
		if parameters is None or len(parameters) == 0:
			return f'{self.base_url}{source}'
		
		url = f'{self.base_url}{source}?'
		url += "&".join([f'{key}={parameters[key]}' for key in parameters])
		url = url.replace(" ", "%20")
		return url
	

	def table_issues(self, filt: dict):
		self.issues_filter = filt
		api_url = self._get_api_endpoint("issues.json", self.issues_filter)
		resp = http_get(url=api_url, headers=self.header).json()
		total_count = resp["total_count"]
		issues = Issue.get_issues_from_json(resp["issues"])
		rows = [issue.get_row() for issue in issues]
		issue_table = Table(header=["ID", "Project", "Tracker", "Status",
			   				    "Priority", "Subject", "Assignee"], scrollable=False,
					  rows=rows, cellsizes=[7, 26, 10, 10, 10, 34, 15],
					  max_length=total_count, paginate=self.issues_paginate)
		issue_table.draw()

	
	def issues_paginate(self, offset: int):
		self.issues_filter["offset"] = offset
		api_url = self._get_api_endpoint("issues.json", self.issues_filter)
		resp = http_get(url=api_url, headers=self.header).json()
		issues = Issue.get_issues_from_json(resp["issues"])
		return [issue.get_row() for issue in issues]

	
	def get_issue_by_id(self, id: int, include_journals: bool=True):
		if include_journals is True:
			api_url = self._get_api_endpoint(f'issues/{id}.json', {"include": "journals"})
		else:
			api_url = self._get_api_endpoint(f'issues/{id}.json')
		resp = http_get(url=api_url, headers=self.header)
		issue = Issue(resp.json()["issue"])
		print(issue)
		

	def table_time_entries(self, filt: dict):
		self.time_entries_filter = filt
		api_url = self._get_api_endpoint("time_entries.json", self.time_entries_filter)
		resp = http_get(url=api_url, headers=self.header).json()
		total_count = resp["total_count"]
		time_entries = TimeEntry.get_time_entries_from_json(resp["time_entries"])
		rows = [time_entry.get_row() for time_entry in time_entries]
		time_entry_table = Table(header=["ID", "Project", "Activity", "Issue",
			   				        "Comment", "Hours", "Date", "User"], scrollable=False,
					  rows=rows, cellsizes=[7, 25, 10, 7, 32, 5, 10, 15],
					  max_length=total_count, paginate=self.time_entries_paginate,
					  select_item_action=self.get_time_entry_as_content)
		time_entry_table.draw()


	def time_entries_paginate(self, offset: int):
		self.time_entries_filter["offset"] = offset
		api_url = self._get_api_endpoint("time_entries.json", self.time_entries_filter)
		resp = http_get(url=api_url, headers=self.header).json()
		time_entries = TimeEntry.get_time_entries_from_json(resp["time_entries"])
		return [time_entry.get_row() for time_entry in time_entries]


	def create_time_entry(self, parameters: dict):
		api_url = self._get_api_endpoint("time_entries.json")
		resp = http_post(url=api_url, headers=self.header, json=parameters)
		return resp


	def get_time_entry_by_id(self, id: int):
		api_url = self._get_api_endpoint(f'time_entries/{id}.json')
		resp = http_get(url=api_url, headers=self.header)
		return TimeEntry(resp.json()["time_entry"])
	

	def get_time_entry_as_content(self, id: int):
		time_entry = self.get_time_entry_by_id(id)
		time_entry_dict = time_entry.to_dict()
		time_entry_dict["log time"] = ""
		time_entry_dict["header"] = "Time entry details"
		return time_entry_dict


	def create_issue(self, parameters: dict):
		api_url = self._get_api_endpoint("issues.json")
		resp = http_post(url=api_url, headers=self.header, json=parameters)
		return resp

	

