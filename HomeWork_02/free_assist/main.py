from sys import exit
from time import sleep

from prompt_toolkit import PromptSession, print_formatted_text, ANSI
from prompt_toolkit.shortcuts import CompleteStyle, set_title

from free_assist.address_book import AddressBook
from free_assist.notes import Notes
from free_assist.cli_commands import CliCompleter, CliCmdParser, ExitCmd


class CLI:
    def __init__(self):
        self.data = {"address_book": AddressBook(), "note_book": Notes(), "none": None}
        self.parser = CliCmdParser()

        self.session = PromptSession(completer=CliCompleter(), complete_style=CompleteStyle.MULTI_COLUMN)

    def run(self):
        set_title("Free assistant")
        while True:
            try:
                input_str = self.session.prompt("Enter a command >> ")
            except KeyboardInterrupt:
                continue
            if not input_str:
                continue
            try:
                self.parser.cmd_parse(input_str)
                data_item = self.data[getattr(self.parser.parsed_command, "data_name")]
                result = self.parser.parsed_command(data_item)
                if isinstance(result, str):
                    print_formatted_text(ANSI(result))
            except (ValueError, KeyError, IndexError) as err:
                if str(err):
                    print_formatted_text(ANSI(str(err)))
                continue
            except ExitCmd as msg:
                print_formatted_text(ANSI(str(msg)))
                sleep(1)
                exit(0)


def main():
    try:
        cli = CLI()
        cli.run()
    finally:
        del cli


if __name__ == '__main__':
    main()
