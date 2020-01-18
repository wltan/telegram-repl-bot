import docker
import time

class Repl:
    def __init__(self):
        self.client = docker.from_env()
        self.container = None

    def launch(self, lang, pipeout):
        """
        Spawns a container with the interpreter for the given language.
        Returns an instance of the container.

        pipeout is a function that takes a string and sends it back to the user.
        Use it to send standard output from the container.
        """
        if lang == "source":
            self.container = self.client.containers.run("source", "1", stdin_open = True, tty = True, detach = True)

    def pipein(self, text):
        """
        Sends the text string into the container as standard input.
        There is no need to return anything.
        """
        pass

    def kill(self):
        """
        Stops the container.
        """
        self.container.stop()

# For debugging
repl = Repl()
repl.launch("source", 1)
time.sleep(5)
repl.kill()