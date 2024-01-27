from argparse import ArgumentParser
from options import TITLE
from options import DESCRIPTION
from options import EPILOG
from options import GLOBAL_OPTIONS


class CommandInterpreter:


    def __init__(self):
        self.parser = ArgumentParser(prog=TITLE, description=DESCRIPTION,
                                     epilog=EPILOG)
        self.parser.add_argument(GLOBAL_OPTIONS["short"], GLOBAL_OPTIONS["long"],
                                 action=GLOBAL_OPTIONS["action"], help=GLOBAL_OPTIONS["help"])
        command_parsers = self.parser.add_subparsers(dest="command", required=True)


def main(command_line=None):
    parser = ArgumentParser('Redmine cli tool')
    subparsers = parser.add_subparsers(dest='command')
    issue = subparsers.add_parser('issue', help='Issue related commands')
    issue_subparser = issue.add_subparsers(dest='issue_cmd', required=True)
    issue_create = issue_subparser.add_parser('create', help='create new issue')
    issue_create.add_argument(
        '--dry-run',
        help='do nothing, just pretend',
        action='store_true'
    )
    issue_create.add_argument('-p', '--project-id', nargs=1, help='project id')
    issue_create.add_argument('-s', '--subject', nargs=1, help='subject')
    issue_create.add_argument('-t', '--tracker-id', nargs=1, help='tracker id')
    issue_show = issue_subparser.add_parser("show", help="Show a specific issue")
    issue_show.add_argument("id", type=int, help="ex. redmine-assistant issue show 10234")
    issue_show.add_argument("-i", "--include", type=str, nargs="*", choices=["journals", "attachments", "changesets"])
    issue_list = issue_subparser.add_parser('list', help='list issues')
    issue_list.add_argument('-u', '--author-user-id', nargs=1, help='List by author id')
    issue_list.add_argument('-a', '--assignee-user-id', nargs=1, help='List by assignee id')
    time_entry = subparsers.add_parser('time-entry', help='Time entry related commands')
    time_entry_subparsers = time_entry.add_subparsers(dest='time_entry_cmd', required=True)
    time_entry_list = time_entry_subparsers.add_parser('list', help='List time entries')
    time_entry_list.add_argument('-u', '--author-user-id', nargs=1, help='List by author id')
    time_entry_list.add_argument('-p', '--project-id', nargs=1, help='project id')
    args = parser.parse_args(command_line)
    print(args.command)
    if args.command == 'time-entry':
        print(args)
        print(args.time_entry_cmd)
        if args.time_entry_cmd == 'list':
            print('list')
            print(f'{args.project_id if args.project_id is not None else ""}')
            print(f'{args.author_user_id if args.author_user_id is not None else ""}')
    elif args.command == 'issue':
        print(args)
        print(args.issue_cmd)
        if args.issue_cmd == 'create':
            print(f'{args.project_id if args.project_id is not None else ""}')
            print(f'{args.tracker_id if args.tracker_id is not None else ""}')
            print(f'{args.subject if args.subject is not None else ""}')
        if args.issue_cmd == 'list':
            print(f'{args.author_user_id if args.author_user_id is not None else ""}')
            print(f'{args.assignee_user_id if args.assignee_user_id is not None else ""}')


if __name__ == '__main__':
    main()

