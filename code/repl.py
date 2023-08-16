from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory
from pygments.lexers import PythonLexer

class CustomCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        
        if not words:
            return

        # Only one word, and it's being typed. Suggest base commands.
        if len(words) == 1:
            base_commands = ["template", "path"]
            for cmd in base_commands:
                if cmd.startswith(words[0]):
                    yield Completion(cmd, start_position=-len(words[0]))
        else:
            # If there's a base command already and the user is starting a second word.
            prefix = words[-1]
            if words[0] == "template":
                templates = ["House Template", "Apartment Template", "Wardrobe Template"]
                for template in templates:
                    if template.startswith(prefix):
                        yield Completion(template, start_position=-len(prefix))
            elif words[0] == "path":
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
    session = PromptSession(history=history, lexer=PygmentsLexer(PythonLexer), completer=completer)

    while True:
        try:
            user_input = session.prompt(">>> ")
            if user_input.lower() in ('exit', 'quit'):
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
