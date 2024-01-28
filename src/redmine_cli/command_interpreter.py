from argparse import ArgumentParser
from options import TITLE
from options import DESCRIPTION
from options import EPILOG
from options import GLOBAL_OPTIONS
from options import OPTIONS


class CommandInterpreter:


    def __init__(self):
        self.parser = ArgumentParser(prog=TITLE,
                      description=DESCRIPTION, epilog=EPILOG)
        self.parser.add_argument(GLOBAL_OPTIONS["short"], GLOBAL_OPTIONS["long"],
                                 action=GLOBAL_OPTIONS["action"],
                                 help=GLOBAL_OPTIONS["help"])
        command_parsers = self.parser.add_subparsers(dest="command",
                          title="commands", required=True)
        for command in OPTIONS:
            # command = issue 
            cmd = command_parsers.add_parser(command, help=OPTIONS[command]["help"])
            cmd_subparsers = cmd.add_subparsers(dest=f'{command}_command',
                             title=f'{command} commands', required=True)
            # sub_cmd = show, create, list etc.
            for sub_cmd in OPTIONS[command]:
                if sub_cmd == "help":
                    continue
                cmd_subparser = cmd_subparsers.add_parser(sub_cmd,
                                help=OPTIONS[command][sub_cmd]["help"])
                for sub_cmd_pos in OPTIONS[command][sub_cmd]["positionals"]:
                    cmd_subparser.add_argument(
                        sub_cmd_pos.get("name"),
                        type=sub_cmd_pos.get("type"),
                        help=sub_cmd_pos.get("help")
                    )
                for sub_cmd_flag in OPTIONS[command][sub_cmd]["flags"]:
                    try:
                        cmd_subparser.add_argument(
                            sub_cmd_flag["short"],
                            sub_cmd_flag["long"],
                            action=sub_cmd_flag["action"],
                            help=sub_cmd_flag.get("help")
                        )
                    except KeyError as error:
                        key = error.__str__()
                        if key == "'short'":
                            cmd_subparser.add_argument(
                                sub_cmd_flag["long"],
                                action=sub_cmd_flag["action"],
                                help=sub_cmd_flag.get("help")
                            )
                        else:
                            raise RuntimeError

                for sub_cmd_opt in OPTIONS[command][sub_cmd]["options"]:
                    try:
                        cmd_subparser.add_argument(
                            sub_cmd_opt["short"],
                            sub_cmd_opt["long"],
                            type=sub_cmd_opt.get("type"),
                            nargs=sub_cmd_opt.get("nargs"),
                            metavar=sub_cmd_opt.get("metavar"),
                            choices=sub_cmd_opt.get("choices"),
                            help=sub_cmd_opt.get("help")
                        )
                    except KeyError as error:
                        key = error.__str__()
                        if key == "'short'":
                            cmd_subparser.add_argument(
                                sub_cmd_opt["long"],
                                type=sub_cmd_opt.get("type"),
                                nargs=sub_cmd_opt.get("nargs"),
                                metavar=sub_cmd_opt.get("metavar"),
                                choices=sub_cmd_opt.get("choices"),
                                help=sub_cmd_opt.get("help")
                            )
                        else:
                            raise RuntimeError

    def get_parser(self):
        return self.parser


def main(command_line=None):
    cmd = CommandInterpreter()
    parser = cmd.get_parser()
    # args = ['issue', 'create']
    args = command_line
    args = parser.parse_args(args)
    print(args.command)
    if args.command == 'time-entry':
        print(args)
        print(args.time_entry_cmd)
        if args.time_entry_cmd == 'list':
            print('list')
            print(f'{args.project_id if args.project_id is not None else ""}')
            print(f'{args.author_user_id if args.author_user_id is not None else ""}')
    elif args.command == 'issue':
        if args.issue_command == 'create':
            print(f'{args.project_id if args.project_id is not None else ""}')
            print(f'{args.tracker_id if args.tracker_id is not None else ""}')
            print(f'{args.subject if args.subject is not None else ""}')
        if args.issue_command == 'list':
            print(f'{args.author_user_id if args.author_user_id is not None else ""}')
            print(f'{args.assignee_user_id if args.assignee_user_id is not None else ""}')


if __name__ == '__main__':
    main()

