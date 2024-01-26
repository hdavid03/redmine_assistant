from requests import get as http_get
from redmine_api.issue import Issue
from redmine_api.time_entry import TimeEntry

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
		return url
	

	def get_issues(self, filt: dict):
		api_url = self._get_api_endpoint("issues.json", filt)
		resp = http_get(url=api_url, headers=self.header)
		issues = Issue.get_issues_from_json(resp.json()["issues"])
		Issue.table_issues(issues)

	
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
		time_entries = TimeEntry.get_time_entries_from_json(resp.json()["time_entries"])
		TimeEntry.table_time_entries(time_entries)


	def get_time_entry_by_id(self, id: int):
		api_url = self._get_api_endpoint(f'time_entries/{id}.json')
		resp = http_get(url=api_url, headers=self.header)
		time_entry = TimeEntry(resp.json()["time_entry"])
		print(time_entry)




	

