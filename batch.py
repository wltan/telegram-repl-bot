def launch(path, src, stdin, lang, on_finish, on_close):
    """
    Parameters
    path (str) - path to code files
    src (str) - source code file name
    stdin (str) - input file name (value is None if no file supplied)
    lang (str) - language
    on_finish (unary function) - call when program has successfully terminated; 
                                argument is the path to output file
    on_close (nullary function) - call when container is dead
    """
    pass

def kill(instance):
    pass

class Batch:
    def __init__(self, path, src, stdin, lang, on_finish, on_close):
        # Store all the variables
        self.path = path
        self.src = src
        self.stdin = stdin
        self.lang = lang
        self.on_finish = on_finish
        self.on_close = on_close

        # Language selection
        if lang == "python":
            pass
        elif lang == "java":
            pass
        elif lang == "c":
            pass
        elif lang == "c++":
            pass