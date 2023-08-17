from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory
from pygments.lexers import PythonLexer
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import shlex
from functools import lru_cache


class CustomCompleter(Completer):
    def __init__(self, completion_tree):
        super().__init__()
        self.completion_tree = completion_tree

    @lru_cache(maxsize=128)
    def _parse_arguments(self, text):
        return shlex.split(text)

    def get_completions(self, document, complete_event):
        # Convert the input text to lowercase for case-insensitive comparison.
        text = document.text_before_cursor.lower()
        
        # Parse the input text to extract arguments.
        arguments = self._parse_arguments(text)

        if text[-1] == " ":
            arguments.append("")

        # If there are no arguments or a space was just typed, suggest an empty option.
        if not arguments:
            yield Completion("", start_position=0)
            return

        # Traverse the completion tree based on parsed arguments.
        cur_tree = self.completion_tree
        for arg in arguments[:-1]:
            matching_key = next((k for k in cur_tree if k.lower() == arg), None)
            if isinstance(cur_tree, dict) and matching_key:
                cur_tree = cur_tree[matching_key]
            else:
                return

        # Get the prefix for suggestions at the current level.
        prefix = arguments[-1]

        # Check if the current level contains options (dict or list).
        if isinstance(cur_tree, dict):
            # Special handling for dictionary values that are lists
            matching_key = next((k for k in cur_tree if k.lower() == prefix), None)
            if matching_key and isinstance(cur_tree[matching_key], list):
                for option in cur_tree[matching_key]:
                    yield Completion(str(option), start_position=0)
                return

            # Regular handling for other dictionary values
            options = [o for o in cur_tree if str(o).lower().startswith(prefix)]
            for option in options:
                yield Completion(str(option), start_position=-len(prefix))

        elif isinstance(cur_tree, list):
            options = [o for o in cur_tree if str(o).lower().startswith(prefix)]
            for option in options:
                yield Completion(str(option), start_position=-len(prefix))




def custom_eval(input_str):
    try:
        # result = eval(input_str)
        return (
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
        "ai": None
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
                print("Exiting REPL. See Ya!")
                break

            result = custom_eval(user_input)
            print(result)
        except KeyboardInterrupt:
            print("\n🎹🎹Interrupt, opsie, let's move on!")
        except EOFError:
            print("\nExiting REPL. Bye 👋🏻")
            break


if __name__ == "__main__":
    print("MadIA REPL with Autocomplete - Type 'exit' or 'quit' to exit.")
    main()
