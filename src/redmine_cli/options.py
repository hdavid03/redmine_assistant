
TITLE = "redmine-assistant"

DESCRIPTION = "Python CLI tool for Redmine REST API with useful features"
EPILOG = "GitHub repository: https://github.com/hdavid03/redmine_assistant"

GLOBAL_OPTIONS = {
	"short": "-v",
	"long": "--version",
	"action": "store_true",
	"help": "Show redmine_assistant version"
}

OPTIONS = {
	"issue": {
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
					"long": "--include",
					"type": int,
					"nargs": "*",
					"choices": [
						"journals", "attachments", "changesets"
					],
					"help": "fetch associated data [journals,attachments, changesets] (optional)"
				}
			],
			"help": "Show details of an issue"
		},
		"list": {
			"positionals": [],
			"flags": [
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
					"metavar": "N",
					"help": "number of issues per page (default=15)"
				},
				{
					"long": "--sort-asc",
					"type": str,
					"nargs": 1,
					"metavar": "COLUMN",
					"help": "sort ascending by a given parameter"
				},
				{
					"long": "--sort-desc",
					"type": str,
					"nargs": 1,
					"metavar": "COLUMN",
					"help": "sort descending by a given parameter"
				},
				{
					"short": "-p",
					"long": "--project-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "get issues by project ID"
				},
				{
					"short": "-t",
					"long": "--tracker-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "get issues by tracker ID"
				},
				{
					"short": "-s",
					"long": "--status-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "get issues by status ID"
				},
				{
					"short": "-a",
					"long": "--assigned-to-id",
					"nargs": 1,
					"metavar": "ID",
					"help": "get issues by assignee ID"
				},
				{
					"short": "-u",
					"long": "--user-id",
					"nargs": 1,
					"metavar": "ID",
					"help": "get issues by author user ID"
				}
			],
			"help": "List issues by given parameters"
		},
		"create": {
			"positionals": [],
			"flags": [
				{
					"short": "-p",
					"long": "--project-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "the ID of the project to which the issue belongs"
				},
				{
					"long": "--parent-issue-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "the ID of the parent issue"
				},
				{
					"short": "-t",
					"long": "--tracker-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "issue tracker ID"
				},
				{
					"short": "-s",
					"long": "--status-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "issue status ID"
				},
				{
					"long": "--priority-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "priority ID of the issue"
				},
				{
					"long": "--subject",
					"type": str,
					"nargs": 1,
					"metavar": "TEXT",
					"help": "a short description about the issue"
				},
				{
					"short": "-a",
					"long": "--assigned-to-id",
					"nargs": 1,
					"metavar": "ID",
					"help": "the ID of the user to assign the issue to"
				},
				{
					"short": "-e",
					"long": "--estimated-hours",
					"nargs": 1,
					"type": float,
					"metavar": "ID",
					"help": "estimated hours for the issue (float)"
				}
			],
			"help": "Create a new issue"
		},
		"update": {
			"positionals": [],
			"flags": [
				{
					"short": "-n",
					"long": "--notes",
					"type": str,
					"nargs": 1,
					"metavar": "TEXT",
					"help": "notes about the update"
				},
				{
					"long": "--private",
					"action": "store_true",
					"default": False,
					"help": "set notes to private"
				},
				{
					"short": "-p",
					"long": "--project-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "the ID of the project to which the issue belongs"
				},
				{
					"long": "--parent-issue-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "the ID of the parent issue"
				},
				{
					"short": "-t",
					"long": "--tracker-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "issue tracker ID"
				},
				{
					"short": "-s",
					"long": "--status-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "issue status ID"
				},
				{
					"long": "--priority-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "priority ID of the issue"
				},
				{
					"long": "--subject",
					"type": str,
					"nargs": 1,
					"metavar": "TEXT",
					"help": "a short description about the issue"
				},
				{
					"short": "-a",
					"long": "--assigned-to-id",
					"nargs": 1,
					"metavar": "ID",
					"help": "the ID of the user to assign the issue to"
				},
				{
					"short": "-e",
					"long": "--estimated-hours",
					"nargs": 1,
					"type": float,
					"metavar": "ID",
					"help": "estimated hours for the issue (float)"
				}
			]
		},
		#"delete": {},
		},
	"time-entry": {
		"show": {
			"positionals": [
				{
					"name": "id",
					"type": int,
	 				"help": "time entry ID (required option)"
				}
			],
			"help": "Show details of an time entry"
		},
		"list": {
			"positionals": [],
			"flags": [
				{
					"short": "-o",
					"long": "--offset",
					"type": int,
					"nargs": 1,
					"metavar": "N",
					"help": "skip this number of time entries"
				},
				{
					"short": "-l",
					"long": "--limit",
					"type": int,
					"nargs": 1,
					"metavar": "N",
					"help": "number of time entries per page (default=15)"
				},
				{
					"long": "--sort-asc",
					"type": str,
					"nargs": 1,
					"metavar": "COLUMN",
					"help": "sort time entries ascending by a given parameter"
				},
				{
					"long": "--sort-desc",
					"type": str,
					"nargs": 1,
					"metavar": "COLUMN",
					"help": "sort time entries descending by a given parameter"
				},
				{
					"short": "-p",
					"long": "--project-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "get time entries by project ID"
				},
				{
					"short": "-i",
					"long": "--issue-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "get time entries by issue ID"
				},
				{
					"short": "-a",
					"long": "--activity-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "get time entries by activity ID"
				},
				{
					"short": "-u",
					"long": "--user-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "get time entries by user ID"
				},
				{
					"long": "--from",
					"type": str,
					"nargs": 1,
					"metavar": "yyyy-mm-dd",
					"help": "get time entries from a given date"
				},
				{
					"long": "--to",
					"type": str,
					"nargs": 1,
					"metavar": "yyyy-mm-dd",
					"help": "get time entries to a given date"
				}
			],
			"help": "List time entries by given parameters"
		},
		"create": {
			"positionals": [],
			"flags": [
				{
					"short": "-p",
					"long": "--project-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "the ID of the project to which the time entry belongs"
				},
				{
					"short": "-i",
					"long": "--issue-id",
					"type": int,
					"nargs": 1,
					"metavar": "ID",
					"help": "the ID of the issue to which the time entry belongs to"
				},
				{
					"short": "-d",
					"long": "--date",
					"type": str,
					"nargs": 1,
					"metavar": "yyyy-mm-dd",
					"help": "the date of the time spent (default is the current date)"
				},
				{
					"short": "-h",
					"long": "--hours",
					"type": float,
					"nargs": 1,
					"metavar": "h.hh",
					"help": "the number of spent hours (float)"
				},
				{
					"short": "-c",
					"long": "--comment",
					"type": str,
					"nargs": 1,
					"metavar": "TEXT",
					"help": "short descreption about the spent hours (max 255 chars)"
				},
				{
					"short": "-a",
					"long": "--activity-id",
					"nargs": 1,
					"metavar": "ID",
					"help": "the ID of the activity of time spent"
				},
				{
					"short": "-e",
					"long": "--estimated-hours",
					"nargs": 1,
					"type": float,
					"metavar": "ID",
					"help": "number of hours estimated for issue (float)"
				}
			],
			"help": "Create new time entry"
		}
		# "update": {},
		# "delete": {}
	}
	# "project": {}
}
