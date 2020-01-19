import docker
import time
import threading
import registry_credentials

MESSAGE_LIMIT = 4096

def launch(lang, pipeout, on_close):
    return Repl(lang, pipeout, on_close)

def pipein(instance, text):
    instance.pipein(text)

def kill(instance):
    instance.kill()

class Repl:
    def __init__(self, lang, pipeout, on_close):
        """
        Spawns a container with the interpreter for the given language.
        Returns an instance of the container.

        pipeout is a function that takes a string and sends it back to the user.
        Use it to send standard output from the container.
        """
        self.client = docker.APIClient()
        self.client.login(
            username = registry_credentials.SERVICE_PRINCIPAL_ID,
            password = registry_credentials.SERVICE_PRINCIPAL_PASSWORD,
            registry = "replbotimages.azurecr.io"
        )

        self.on_close = on_close
        self.lang = lang

        # Language selection
        if lang == "python":
            self.container = self.client.create_container(
                image = "replbotimages.azurecr.io/python-repl:v1",
                stdin_open = True,
                detach = True,
                tty = True # If this is false, the Python shell doesn't bother outputting anything
            )
        elif lang == "java":
            self.container = self.client.create_container(
                image = "replbotimages.azurecr.io/java-repl:v1",
                stdin_open = True,
                detach = True,
                tty = False
            )
        elif lang == "c":
            self.container = self.client.create_container(
                image = "replbotimages.azurecr.io/c-repl:v1",
                stdin_open = True,
                detach = True,
                tty = False
            )
        elif lang == "source":
            self.container = self.client.create_container(
                image = "replbotimages.azurecr.io/source-repl:v1",
                command = "node dist/repl/repl.js 4",
                stdin_open = True,
                detach = True,
                tty = False # If this is true, you get ANSI colour escape sequences in the output
            )
        
        # Start the container
        self.client.start(self.container)
        
        # Get sockets
        self.input = self.client.attach_socket(self.container, params={'stdin': 1, 'stream': 1})._sock
        self.output = self.client.attach_socket(self.container, params={'stdout': 1, 'stream': 1})._sock

        # Initialise listener
        self.listener = threading.Thread(target = self.__listen, args = [pipeout])
        self.listener.start()

    def pipein(self, text):
        """
        Sends the text string into the container as standard input.
        There is no need to return anything.
        """
        self.input.send(text.encode('utf-8')) # Convert to bytes

    def kill(self):
        self.client.stop(self.container) # Stop the container

    def __listen(self, pipeout):
        logs = self.client.logs(
            self.container,
            stdout = True,
            stream = True
        )
        if self.lang == "python": # Python REPL flushes stdout after each char
            sb = []
            for line in logs:
                decoded_line = line.decode('utf-8')
                # Only pipeout upon newline
                if '\n' in decoded_line:
                    pipeout(''.join(sb))
                    sb = []
                else:
                    sb.append(decoded_line)
        else:
            for line in logs:
                pipeout(line.decode('utf-8'))
        
        # Once this code is reached, the container is dead
        self.on_close()
        self.client.remove_container(self.container) # Remove the container
