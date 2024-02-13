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
		self.header = {
			"X-Redmine-API-Key": self.api_key
		}


	def _get_api_endpoint(self, source: str, parameters: dict=None):
		if parameters is None or len(parameters) == 0:
			return f'{self.base_url}{source}'
		
		url = f'{self.base_url}{source}?'
		url += "&".join([f'{key}={parameters[key]}' for key in parameters])
		url = url.replace(" ", "%20")
		return url
	

	def table_issues(self, filt: dict):
		api_url = self._get_api_endpoint("issues.json", filt)
		resp = http_get(url=api_url, headers=self.header)
		issues = Issue.get_issues_from_json(resp.json()["issues"])
		rows = [issue.get_row() for issue in issues]
		issue_table = Table(max_rows=20,
					  header=["ID", "Project", "Tracker", "Status",
			   				  "Priority", "Subject", "Assignee"],
					  rows=rows, cellsizes=[7, 26, 10, 10, 10, 34, 15])
		issue_table.draw()

	
	def get_issue_by_id(self, id: int, include_journals: bool=True):
		if include_journals is True:
			api_url = self._get_api_endpoint(f'issues/{id}.json', {"include": "journals"})
		else:
			api_url = self._get_api_endpoint(f'issues/{id}.json')
		resp = http_get(url=api_url, headers=self.header)
		issue = Issue(resp.json()["issue"])
		print(issue)
		

	def get_time_entries(self, filt: dict):
		api_url = self._get_api_endpoint("time_entries.json", filt)
		resp = http_get(url=api_url, headers=self.header)
		resp_json = resp.json()
		count = resp_json.get("total_count")
		limit = resp_json.get("limit")
		time_entries = TimeEntry.get_time_entries_from_json(resp.json()["time_entries"])
		n = len(time_entries)
		TimeEntry.table_time_entries(time_entries)
		if filt.get("offset") is None:
			filt["offset"] = 0
		offset = limit
		ans = ""
		while ans.upper() != "Q":
			ans = input("b/n/q")
			if ans.upper() == "B":
				if filt["offset"] > (offset - 1):
					filt["offset"] -= offset
				elif filt["offset"] != 0:
					filt["offset"] = 0
			elif ans.upper() == "N":
				if (filt["offset"] + offset) < count + 1:
					filt["offset"] += offset
			else:
				continue
			print("\033[F" * (n + 5))
			api_url = self._get_api_endpoint("time_entries.json", filt)
			resp = http_get(url=api_url, headers=self.header)
			time_entries = TimeEntry.get_time_entries_from_json(resp.json()["time_entries"])
			TimeEntry.table_time_entries(time_entries)


	def create_time_entry(self, parameters: dict):
		api_url = self._get_api_endpoint("time_entries.json")
		resp = http_post(url=api_url, headers=self.header, json=parameters)
		return resp


	def get_time_entry_by_id(self, id: int):
		api_url = self._get_api_endpoint(f'time_entries/{id}.json')
		resp = http_get(url=api_url, headers=self.header)
		time_entry = TimeEntry(resp.json()["time_entry"])
		print(time_entry)




	

