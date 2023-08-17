from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory
from pygments.lexers import PythonLexer


def parse_arguments(text):
    arguments = []
    inside_quotes = False
    current_arg = ""
    for char in text:
        if char == '"':
            inside_quotes = not inside_quotes
            if not inside_quotes:
                arguments.append(current_arg.strip())
                current_arg = ""
        elif char == " " and not inside_quotes:
            arguments.append(current_arg.strip())
            current_arg = ""
        else:
            current_arg += char
    arguments.append(current_arg.strip())

    return [arg for arg in arguments if arg]  # Remove empty arguments


class CustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        arguments = parse_arguments(text)
        if text[-1] == " ":
            arguments.append("")

        if not arguments:
            return

        # Only one word, and it's being typed. Suggest base commands.
        if len(arguments) == 1:
            base_commands = ["template", "path"]
            for cmd in base_commands:
                if cmd.startswith(arguments[0]):
                    yield Completion(cmd, start_position=-len(arguments[0]))
        else:
            prefix = arguments[-1]
            if arguments[0] == "template":
                templates = [
                    "House Template",
                    "Apartment Template",
                    "Wardrobe Template",
                ]
                for template in templates:
                    if template.startswith(prefix):
                        yield Completion(template, start_position=-len(prefix))
            elif arguments[0] == "path":
                paths = ["straight", "curves"]
                for path in paths:
                    if path.startswith(prefix):
                        yield Completion(path, start_position=-len(prefix))


def custom_eval(input_str):
    try:
        result = eval(input_str)
        return result
    except Exception as e:
        return f"Error: {e}"


def main():
    completer = CustomCompleter()
    history = FileHistory("repl_history.txt")
    session = PromptSession(
        history=history, lexer=PygmentsLexer(PythonLexer), completer=completer
    )

    while True:
        try:
            user_input = session.prompt(">>> ")
            if user_input.lower() in ("exit", "quit"):
                print("Exiting REPL.")
                break

            result = custom_eval(user_input)
            print(result)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
        except EOFError:
            print("\nExiting REPL.")
            break


if __name__ == "__main__":
    print("Custom REPL with Autocomplete - Type 'exit' or 'quit' to exit.")
    main()
