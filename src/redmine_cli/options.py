from argparse import Action
from argparse import ArgumentTypeError

TITLE = "redmine-assistant"

DESCRIPTION = "Python CLI tool for Redmine REST API with useful features"
EPILOG = """Type 'redmine-assistant COMMAND -h' for help on a command\r\n
GitHub repository for more info: https://github.com/hdavid03/redmine_assistant"""


ARGS = {
	"flags": [
		{
			"short": "-v",
			"long": "--version",
			"action": "store_true",
			"help": "Show redmine_assistant version"
		}
	],
	"commands": {
		"issue": {
			"commands": {
				"show": {
					"positionals": [
						{
							"name": "id",
							"type": int,
		 					"help": "issue ID (required option)"
						}
					],
					"flags": [
						{
							"short": "-i",
							"long": "--include-journals",
							"required": False,
							"action": "store_true",
							"help": "fetch issue with journals (optional)"
						}
					],
					"options": [],
					"help": "Show details of an issue"
				},
				"list": {
					"positionals": [],
					"flags": [],
					"options": [
						{
							"short": "-o",
							"long": "--offset",
							"type": int,
							"nargs": 1,
							"metavar": "N",
							"help": "skip this number of issues"
						},
						{
							"short": "-l",
							"long": "--limit",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "N",
							"help": "number of issues per page (default=15)"
						},
						{
							"long": "--sort-asc",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "COLUMN",
							"help": "sort ascending by a given parameter"
						},
						{
							"long": "--sort-desc",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "COLUMN",
							"help": "sort descending by a given parameter"
						},
						{
							"short": "-p",
							"long": "--project-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "get issues by project ID"
						},
						{
							"short": "-t",
							"long": "--tracker-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "get issues by tracker ID"
						},
						{
							"short": "-s",
							"long": "--status-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "get issues by status ID"
						},
						{
							"short": "-a",
							"long": "--assigned-to-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "get issues by assignee ID"
						},
						{
							"short": "-u",
							"long": "--user-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "get issues by author user ID"
						}
					],
					"help": "List issues by given parameters"
				},
				"create": {
					"positionals": [],
					"flags": [],
					"options": [
						{
							"short": "-p",
							"long": "--project-id",
							"type": int,
							"nargs": 1,
							"required": True,
							"metavar": "ID",
							"help": "the ID of the project to which the issue belongs"
						},
						{
							"short": "-i",
							"long": "--parent-issue-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "the ID of the parent issue"
						},
						{
							"short": "-t",
							"long": "--tracker-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "issue tracker ID"
						},
						{
							"short": "-s",
							"long": "--status-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "issue status ID"
						},
						{
							"long": "--priority-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "priority ID of the issue"
						},
						{
							"long": "--subject",
							"type": str,
							"nargs": 1,
							"required": True,
							"metavar": "TEXT",
							"help": "a short description about the issue"
						},
						{
							"short": "-a",
							"long": "--assigned-to-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "the ID of the user to assign the issue to"
						},
						{
							"short": "-H",
							"long": "--estimated-hours",
							"nargs": 1,
							"required": False,
							"type": float,
							"metavar": "h.hh",
							"help": "estimated hours for the issue (float)"
						}
					],
					"help": "Create a new issue"
				},
				"update": {
					"positionals": [
						{
							"name": "id",
							"type": int,
		 					"help": "issue ID (required option)"
						}
					],
					"flags": [
						{
							"long": "--private",
							"required": False,
							"action": "store_true",
							"help": "notes about the update"
						},
					],
					"options": [
						{
							"short": "-n",
							"long": "--notes",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "TEXT",
							"help": "notes about the update"
						},
						{
							"short": "-p",
							"long": "--project-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "the ID of the project to which the issue belongs"
						},
						{
							"short": "-i",
							"long": "--parent-issue-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "the ID of the parent issue"
						},
						{
							"short": "-t",
							"long": "--tracker-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "issue tracker ID"
						},
						{
							"short": "-s",
							"long": "--status-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "issue status ID"
						},
						{
							"long": "--priority-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "priority ID of the issue"
						},
						{
							"long": "--subject",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "TEXT",
							"help": "a short description about the issue"
						},
						{
							"short": "-a",
							"long": "--assigned-to-id",
							"nargs": 1,
							"required": False,
							"type": str,
							"metavar": "ID",
							"help": "the ID of the user to assign the issue to"
						},
						{
							"short": "-H",
							"long": "--estimated-hours",
							"nargs": 1,
							"required": False,
							"type": float,
							"metavar": "h.hh",
							"help": "estimated hours for the issue (float)"
						}
					],
					"help": "Update an issue by its ID"
				},
				#"delete": {},
			},
			"help": "Manage issues"
		},
		"time-entry": {
			"commands": {
				"show": {
					"positionals": [
						{
							"name": "id",
							"type": int,
		 					"help": "time entry ID (required option)"
						}
					],
					"flags": [],
					"options": [],
					"help": "Show details of an time entry"
				},
				"list": {
					"positionals": [],
					"flags": [],
					"options": [
						{
							"short": "-o",
							"long": "--offset",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "N",
							"help": "skip this number of time entries"
						},
						{
							"short": "-l",
							"long": "--limit",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "N",
							"help": "number of time entries per page (default=15)"
						},
						{
							"long": "--sort-asc",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "COLUMN",
							"help": "sort time entries ascending by a given parameter"
						},
						{
							"long": "--sort-desc",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "COLUMN",
							"help": "sort time entries descending by a given parameter"
						},
						{
							"short": "-p",
							"long": "--project-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "get time entries by project ID"
						},
						{
							"short": "-i",
							"long": "--issue-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "get time entries by issue ID"
						},
						{
							"short": "-a",
							"long": "--activity-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "get time entries by activity ID"
						},
						{
							"short": "-u",
							"long": "--user-id",
							"type": int,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "get time entries by user ID"
						},
						{
							"long": "--from",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "yyyy-mm-dd",
							"help": "get time entries from a given date"
						},
						{
							"long": "--to",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "yyyy-mm-dd",
							"help": "get time entries to a given date"
						}
					],
					"help": "List time entries by given parameters"
				},
				"create": {
					"positionals": [
						{
							"name": "id",
							"type": int,
		 					"help": "the ID of the issue to which time entry belongs (required option)"
						}
					],
					"flags": [],
					"options": [
						{
							"short": "-d",
							"long": "--date",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "yyyy-mm-dd",
							"help": "the date of the time spent (default is the current date)"
						},
						{
							"short": "-H",
							"long": "--hours",
							"type": float,
							"nargs": 1,
							"required": True,
							"metavar": "h.hh",
							"help": "the number of spent hours (float)"
						},
						{
							"short": "-c",
							"long": "--comment",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "TEXT",
							"help": "short descreption about the spent hours (max 255 chars)"
						},
						{
							"short": "-a",
							"long": "--activity-id",
							"type": str,
							"nargs": 1,
							"required": False,
							"metavar": "ID",
							"help": "the ID of the activity of time spent"
						}
					],
					"help": "Create new time entry"
				},
				# "update": {},
				# "delete": {}
			},
			"help": "Log time spent and list time entries"
		}
	# "project": {}
	}
}