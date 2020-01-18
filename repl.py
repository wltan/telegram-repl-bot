def launch(lang, pipeout):
    """
    Spawns a container with the interpreter for the given language.
    Returns an instance of the container.

    pipeout is a function that takes a string and sends it back to the user.
    Use it to send standard output from the container.
    """
    pass

def pipein(container, text):
    """
    Sends the text string into the container as standard input.
    There is no need to return anything.
    """
    pass

def kill(container):
    """
    Stops the container.
    """
    pass