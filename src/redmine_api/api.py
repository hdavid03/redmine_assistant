from requests import get as http_get
from redmine_api.issue import Issue

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


	def _get_api_endpoint(self, source: str, parameters: dict):
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
		




	

