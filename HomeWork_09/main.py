from sqlite3 import IntegrityError

from prompt_toolkit import prompt, print_formatted_text

from database.db import session_scope
from commands import COMMANDS


def run():
    with session_scope() as session:
        try:
            while True:
                try:
                    input_str = prompt("Enter a command--> ")
                    if not input_str:
                        continue

                    input_str = " ".join(list(filter(lambda x: x != "", input_str.lower().split(" "))))

                    if input_str in COMMANDS:
                        print_formatted_text(COMMANDS[input_str](session))
                    else:
                        print_formatted_text("Unknown command.")
                        continue
                except KeyboardInterrupt:
                    break
                except (ValueError, KeyError, IndexError, IntegrityError) as err:
                    print_formatted_text(err)
                    continue
        except Exception as err:
            print(err)
            if session.in_transaction():
                session.rollback()


if __name__ == '__main__':
    run()
