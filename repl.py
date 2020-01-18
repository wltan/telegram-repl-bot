import docker
import time
import threading

POLL_INTERVAL = 0.5

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

        self.is_listening = True
        self.listener = threading.Thread(target = self.__listen)
        self.listener.start()

    def pipein(self, text):
        """
        Sends the text string into the container as standard input.
        There is no need to return anything.
        """
        self.input.send(text.encode('utf-8')) # Convert to bytes

    def kill(self):
        """
        Stops the container.
        """
        self.client.stop(self.container)
        self.client.remove_container(self.container)

    def __listen(self):
        while True:
            if not self.is_listening:
                break
            print(self.output.recv(1024))
            time.sleep(POLL_INTERVAL)
    
    def stop_listener(self):
        self.is_listening = False
        self.listener.join()


# For debugging
repl = Repl()
repl.launch("source", 1)
repl.pipein("5 === 5;")
time.sleep(5)
repl.kill()