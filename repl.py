import docker
import time

class Repl:
    def __init__(self):
        self.client = docker.APIClient()
        self.container = None

    def launch(self, lang, pipeout):
        """
        Spawns a container with the interpreter for the given language.
        Returns an instance of the container.

        pipeout is a function that takes a string and sends it back to the user.
        Use it to send standard output from the container.
        """
        if lang == "source":
            self.container = self.client.create_container(
                "source", "1",
                stdin_open = True,
                tty = True)
        
        self.client.start(self.container)
        
        self.input = self.client.attach_socket(self.container, params={'stdin': 1, 'stream': 1})
        self.output = self.client.attach_socket(self.container, params={'stdout': 1, 'stream': 1})

    def pipein(self, text):
        """
        Sends the text string into the container as standard input.
        There is no need to return anything.
        """
        self.input.send(text)

    def kill(self):
        """
        Stops the container.
        """
        self.client.stop(self.container)
        self.client.remove_container(self.container)

# For debugging
repl = Repl()
repl.launch("source", 1)
time.sleep(5)
repl.kill()