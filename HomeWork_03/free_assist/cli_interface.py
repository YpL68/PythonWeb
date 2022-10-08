from prompt_toolkit import print_formatted_text, ANSI
from prompt_toolkit.shortcuts import set_title, confirm

from free_assist.function import easy_table
from free_assist.abstraction.interface import AInterface
from free_assist.prompt import CliPrompt
from free_assist.commands import COMMANDS, MsgType

DATA_MODULE = {}

MSG_TEXT_COLORS = {MsgType.info: "\x1b[92m", MsgType.warning: "\x1b[93m",
                   MsgType.error: "\x1b[91m", MsgType.confirm: "\x1b[93m"}


class CliCmdParser:
    def __init__(self):
        self.command = ""
        self.params = ""

    def cmd_parse(self, command_list: list, inp_str: str):
        clean_str = " ".join(list(filter(lambda x: x != "", inp_str.lower().split(" ")))) + " "
        for cmd_name in command_list:
            cmd = cmd_name + " "
            if clean_str.startswith(cmd):
                self.command, self.params = cmd_name, clean_str[len(cmd):].strip()
                break
        else:
            raise ValueError(f"Unknown command - '{inp_str}'")


class CLI(AInterface):
    def __init__(self, cli_commands: list = COMMANDS.keys(), cli_parser: CliCmdParser = CliCmdParser()):
        self.cli_commands = cli_commands
        self.cli_parser = cli_parser
        self.cli_prompt = CliPrompt(self.cli_commands)

    @staticmethod
    def highlight_str(src_str: str, text_color: str) -> str:
        return text_color + src_str + "\033[0;0m"

    def show_table_view(self, data: list, highlight_math: str = ""):
        print_formatted_text(ANSI(easy_table(data=data, highlight_math=highlight_math)))

    def show_message(self, msg_type: MsgType, msg_str):
        if msg_type == MsgType.confirm:
            return confirm(msg_str)
        else:
            print_formatted_text(ANSI(self.highlight_str(msg_str, MSG_TEXT_COLORS[msg_type])))

    def edit_data_record(self, record: dict):
        self.show_message(MsgType.info, "Editing data...Press 'Ctrl-C' to cancel")
        try:
            for field in record.values():
                field["value"] = self.cli_prompt.edit_prompt(field["class"], field["caption"], field["is_list"],
                                                             field["value"], field["is_required"])
        except KeyboardInterrupt:
            self.show_message(MsgType.warning, "Editing was canceled.")
            raise ValueError("")

    def run(self):
        set_title("Free assistant")
        while True:
            try:
                input_str = self.cli_prompt.cmd_prompt("Enter a command >> ")
            except KeyboardInterrupt:
                continue
            if not input_str:
                continue
            try:
                self.cli_parser.cmd_parse(self.cli_commands, input_str)
                # генерацию и обработку событий реализую позже.
                command = COMMANDS[self.cli_parser.command](self.cli_parser.params)
                command.interface = self
                if command.data_name:
                    command.data = DATA_MODULE.get(command.data_name, None)
                command()
            except (ValueError, KeyError, IndexError) as err:
                if str(err):
                    self.show_message(MsgType.error, str(err))
                continue
