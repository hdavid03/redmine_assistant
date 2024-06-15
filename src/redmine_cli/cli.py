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
			filt = build_filter(arg_namespace.__dict__)
			redmine_api.table_time_entries(filt)
		elif command == "show":
			time_entry_id = arg_namespace.__dict__.pop("id")
			print(redmine_api.get_time_entry_by_id(time_entry_id))
		elif command == "create":
			issue_id = arg_namespace.__dict__.pop("id")
			payload = build_filter(arg_namespace.__dict__)
			payload["issue_id"] = issue_id
			resp = redmine_api.create_time_entry({"time_entry": payload})
			print(f'{resp.status_code}')
		else:
			print("error")

	if command == 'issue':
		command = arg_namespace.__dict__.pop(command)
		if command == 'create':
			print(f'{arg_namespace.project_id if arg_namespace.project_id is not None else ""}')
			print(f'{arg_namespace.tracker_id if arg_namespace.tracker_id is not None else ""}')
			print(f'{arg_namespace.subject if arg_namespace.subject is not None else ""}')
		if command == 'list':
			filt = build_filter(arg_namespace.__dict__)
			redmine_api.table_issues(filt)


def build_filter(args: dict):
	options = dict(map(lambda pair: (pair[0], pair[1][0]),
	 list(filter(lambda pair: pair[1] is not None, args.items()))))
	return options
