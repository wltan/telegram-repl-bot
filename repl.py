import docker
import time
import threading

POLL_INTERVAL = 0.5
MESSAGE_LIMIT = 4096

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
        
        self.input = self.client.attach_socket(self.container, params={'stdin': 1, 'stream': 1})._sock
        self.output = self.client.attach_socket(self.container, params={'stdout': 1, 'stream': 1})._sock

        # Initialise listener
        self.is_listening = True
        self.listener = threading.Thread(target = self.__listen, args = [pipeout])
        self.listener.start()

    def pipein(self, text):
        """
        Sends the text string into the container as standard input.
        There is no need to return anything.
        """
        self.input.send(text.encode('utf-8')) # Convert to bytes

    def kill(self):
        self.stop_listener()
        self.client.stop(self.container) # Stop the container
        self.client.remove_container(self.container) # Remove the container

    def __listen(self, pipeout):
        while True:
            if not self.is_listening:
                break
            s = self.output.recv(MESSAGE_LIMIT)
            if s != "":
                pipeout(s)
            time.sleep(POLL_INTERVAL)
    
    def stop_listener(self):
        self.is_listening = False
        self.listener.join() # Wait for __listen to break