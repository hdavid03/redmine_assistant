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
	arg_namespace = cmd.run_parser()
	version = arg_namespace.__dict__.pop("version")
	if version:
		print("experimental")
	command = arg_namespace.__dict__.pop(TITLE)
	if command == "time-entry":
		command = arg_namespace.__dict__.pop(command)
		if command == "list":
			filt = time_entry_build_filter(arg_namespace.__dict__)
			redmine_api.get_time_entries(filt)
		elif command == "show":
			#TODO: implement time-entry show
			print('show not implements')
		elif command == "create":
			issue_id = arg_namespace.__dict__.pop("id")
			payload = time_entry_build_filter(arg_namespace.__dict__)
			payload["issue_id"] = issue_id
			resp = redmine_api.create_time_entry({"time_entry": payload})
			print(f'{resp.status_code}')
		else:
			print("error")

	if command == 'issue':
		if arg_namespace.__dict__["issue"] == 'create':
			print(f'{arg_namespace.project_id if arg_namespace.project_id is not None else ""}')
			print(f'{arg_namespace.tracker_id if arg_namespace.tracker_id is not None else ""}')
			print(f'{arg_namespace.subject if arg_namespace.subject is not None else ""}')
		if arg_namespace.__dict__["issue"] == 'list':
			filt = {}
			# filt[]
			print(f'{arg_namespace.user_id if arg_namespace.user_id is not None else ""}')
			print(f'{arg_namespace.assigned_to_id if arg_namespace.assigned_to_id is not None else ""}')
			redmine_api.get_issues()
	# redmine_api.get_issue_by_id(id=10469)
	# redmine_api.get_time_entry_by_id(42413)
	# redmine_api.get_time_entries({"user_id": "me", "limit": 5})
	# redmine_api.get_issues({"user_id": "me", "limit": 5})

def time_entry_build_filter(args: dict):
	options = dict(map(lambda pair: (pair[0], pair[1][0]),
	 list(filter(lambda pair: pair[1] is not None, args.items()))))
	return options
