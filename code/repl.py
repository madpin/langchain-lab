from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory
from pygments.lexers import PythonLexer
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


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
    def __init__(self, completion_tree):
        super().__init__()
        self.completion_tree = completion_tree

    def get_completions(self, document, complete_event):
        # text = document.text_before_cursor  # Case Sensitive
        text = document.text_before_cursor.lower()
        arguments = parse_arguments(text)

        if len(text) == 0 or text[-1] == " ":
            arguments.append("")

        # Starting point of the autocompletion tree.
        cur_tree = self.completion_tree

        for arg in arguments[:-1]:
            # Convert keys to lowercase for case-insensitive comparison.
            matching_key = next((k for k in cur_tree if k.lower() == arg), None)
            # matching_key = arg in current_tree # Case Sensitive

            if matching_key and isinstance(cur_tree, dict):
                cur_tree = cur_tree[matching_key]
            else:
                # If a word does not match the tree, no suggestions are possible.
                return

        prefix = arguments[-1]

        # Check if at the last level, we have a list or a dict.
        if isinstance(cur_tree, dict):
            options = cur_tree.keys()
        elif isinstance(cur_tree, list):
            options = cur_tree
        else:
            return

        for option in options:
            if option.lower().startswith(prefix):
                # if option.startswith(prefix): # Case Sensitive
                yield Completion(option, start_position=-len(prefix))


def custom_eval(input_str):
    try:
        # result = eval(input_str)
        result = (
            input_str.replace("e", "3")
            .replace("o", "0")
            .replace("l", "1")
            .replace("a", "@")
            .replace("t", "7")
            .replace("s", "$")
            .replace("i", "!")
            .replace("n", "#")
            .replace("g", "9")
            .replace("z", "2")
            .replace("c", "(")
            .replace("b", "8")
        )
        return result
    except Exception as e:
        return f"Error: {e}"


def main():
    # Example usage
    options = {
        "template": {
            "House-Template": ["Living-Room", "Bedroom"],
            "Apartment-Template": ["Kitchen", "Bathroom"],
            "Wardrobe-Template": ["Casual", "Formal"],
        },
        "path": {
            "straight": ["North", "South"],
            "curves": ["Left Curve", "Right Curve"],
        },
    }

    completer = CustomCompleter(options)
    history = FileHistory("repl_history.txt")
    session = PromptSession(
        message=">>> ",
        history=history,
        lexer=PygmentsLexer(PythonLexer),
        completer=completer,
        # enable_history_search=True,
        auto_suggest=AutoSuggestFromHistory(),
    )

    while True:
        try:
            user_input = session.prompt()
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
