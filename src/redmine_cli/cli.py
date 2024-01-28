#!/usr/bin/env python3

from redmine_api.api import RedmineApi
from redmine_cli.config import RedmineConfig
from ui_utils.command_interpreter import CommandInterpreter
from redmine_cli.options import ARGS
from redmine_cli.options import TITLE
from redmine_cli.options import DESCRIPTION
from redmine_cli.options import EPILOG

def main():
	config = RedmineConfig()
	url, api_key = config.get_user_info()
	redmine_api = RedmineApi({"url": url, "api_key": api_key})
	cmd = CommandInterpreter(TITLE, DESCRIPTION, EPILOG, ARGS)
	cmd.run_parser()
	# redmine_api.get_issue_by_id(id=10469)
	# redmine_api.get_time_entry_by_id(42413)
	# redmine_api.get_time_entries({"user_id": "me", "limit": 5})
	# redmine_api.get_issues({"user_id": "me", "limit": 5})

