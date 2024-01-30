from argparse import ArgumentParser


class CommandInterpreter:


    def __init__(self,
                 prog=None,
                 description=None,
                 epilog=None,
                 arguments: dict=None):

        self.parser = ArgumentParser(prog=prog,
                      description=description, epilog=epilog)
        _add_arguments_to_parser(parser=self.parser,
                                 arguments=arguments, dest=prog)

        self.command_executors = {}

    
    def get_parser(self):
        return self.parser


    def run_parser(self, args=None):
        return self.parser.parse_args(args)
        

def _add_arguments_to_parser(
        parser: ArgumentParser, 
        arguments: dict,
        dest: str):

    positionals = arguments.get("positionals")
    if positionals is not None and len(positionals) > 0:
        for pos in positionals:
            parser.add_argument(
                pos.get("name"),
                type=pos.get("type"),
                help=pos.get("help")
            )
    flags = arguments.get("flags")
    if flags is not None and len(flags) > 0:
        for flag in flags:
            try:
                parser.add_argument(
                    flag["short"],
                    flag["long"],
                    action=flag["action"],
                    help=flag.get("help")
                )
            except KeyError as error:
                key = error.__str__()
                if key == "'short'":
                    parser.add_argument(
                        flag["long"],
                        action=flag["action"],
                        help=flag.get("help")
                    )
                else:
                    raise RuntimeError("long argument is required at least")
    options = arguments.get("options")
    if options is not None and len(options) > 0:
        for option in options:
            try:
                parser.add_argument(
                    option["short"],
                    option["long"],
                    type=option.get("type"),
                    nargs=option.get("nargs"),
                    required=option.get("required"),
                    metavar=option.get("metavar"),
                    choices=option.get("choices"),
                    help=option.get("help")
                )
            except KeyError as error:
                key = error.__str__()
                if key == "'short'":
                    parser.add_argument(
                        option["long"],
                        type=option.get("type"),
                        nargs=option.get("nargs"),
                        required=option.get("required"),
                        metavar=option.get("metavar"),
                        choices=option.get("choices"),
                        help=option.get("help")
                    )
                else:
                    raise RuntimeError("long argument is required at least")
    commands = arguments.get("commands")
    if arguments.get("commands") is not None:
        command_parsers = parser.add_subparsers(dest=dest,
                      title=f'{dest} commands', required=True)
        for command in commands:
            # commands = issue, time-entry 
            cmd_parser = command_parsers.add_parser(command, help=commands[command]["help"])
            _add_arguments_to_parser(cmd_parser, commands[command], command)

