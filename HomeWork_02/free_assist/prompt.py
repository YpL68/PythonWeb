from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import Validator

ANSI_COLORS = {"red": "\x1b[91m", "blue": "\x1b[94m", "green": "\x1b[92m", "yellow": "\x1b[93m"}

CYRILLIC_KEYS = "йцукенгшщзхъфывапролджэячсмитьбю"
TRANSLATION_KEYS = ("q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "a", "s", "d", "f",
                    "g", "h", "j", "k", "l", ";", "'", "z", "x", "c", "v", "b", "n", "m", ",", ".")

TRANS_KEYS = {ord(c): l for c, l in zip(CYRILLIC_KEYS, TRANSLATION_KEYS)}

caption_style = Style.from_dict({'field_caption': '#ffffff'})


def is_valid_field(field_class, field_values: str, is_list: bool, is_required: bool = False) -> bool:
    if is_required and not field_values:
        return False

    result = True
    values = []
    if is_list:
        values = list(filter(lambda x: x != "", field_values.lower().split(" ")))
    else:
        field_values = field_values.strip()
        if field_values:
            values.append(field_values)
    if values:
        try:
            _ = [field_class(field_value) for field_value in values]
        except ValueError:
            result = False
    return result


def create_validator(field_class, is_list: bool,
                     is_required: bool = False) -> Validator:
    def is_valid_field_value(text):
        return is_valid_field(field_class, text, is_list, is_required)

    validator = Validator.from_callable(
        is_valid_field_value,
        error_message="Input is invalid",
        move_cursor_to_end=True,
    )
    return validator


class CliCompleter(Completer):
    def __init__(self, command_list: list):
        self.commands = command_list

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor().lower().translate(TRANS_KEYS)
        if len(document.current_line_before_cursor.strip()) == len(word):
            for command in self.commands:
                if command.find(word) != -1:
                    yield Completion(
                        command,
                        start_position=-len(word),
                        style="fg:black",
                        selected_style="fg:black bg:white",
                    )


class CliPrompt:
    def __init__(self, completion_list: list):
        self.cmd_session = PromptSession(completer=CliCompleter(completion_list),
                                         complete_style=CompleteStyle.MULTI_COLUMN)

    def cmd_prompt(self, prompt_text: str):
        return self.cmd_session.prompt(prompt_text)

    @staticmethod
    def edit_prompt(field_class, field_caption: str, is_list: bool,
                    default_value: str = "", is_required: bool = False):
        field_caption = ('class:field_caption', field_caption + ": ")

        return prompt([field_caption],
                      style=caption_style,
                      validator=create_validator(field_class, is_list, is_required),
                      validate_while_typing=False,
                      default=default_value)


if __name__ == '__main__':
    cli_prompt = CliPrompt(["add", "edit"])
    input_str = cli_prompt.edit_prompt(int, "Вася", False, "Моня", False)
