#!/usr/bin/env python3

from redmine_api.api import RedmineApi
from redmine_cli.config import RedmineConfig


def main():
	config = RedmineConfig()
	url, api_key = config.get_user_info()
	redmine_api = RedmineApi({"url": url, "api_key": api_key})
	# redmine_api.get_issue_by_id(id=10469)
	# redmine_api.get_time_entry_by_id(42413)
	redmine_api.get_time_entries({"user_id": "me", "limit": 5})
	redmine_api.get_issues({"user_id": "me", "limit": 5})

