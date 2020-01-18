import docker
import os
import threading

VOLUME_PATH = '/user/'
OUTPUT_FILENAME = 'out.txt'

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
    return Batch(path, src, stdin, lang, on_finish, on_close)

def kill(instance):
    instance.kill()

class Batch:
    def __init__(self, path, src, stdin, lang, on_finish, on_close):
        # Store all the variables
        self.path = path
        self.src = src
        self.stdin = stdin
        self.lang = lang
        self.on_finish = on_finish
        self.on_close = on_close

        self.client = docker.APIClient()

        source_file = VOLUME_PATH + self.src
        out_file = VOLUME_PATH + OUTPUT_FILENAME
        host_path = os.getcwd() + "/" + self.path

        # Language selection
        if lang == "python":
            pass
        elif lang == "java":
            self.container = self.client.create_container(
                image = "java",
                stdin_open = True,
                detach = True,
                tty = False,
                command = "java " + source_file + " > " + out_file if self.stdin is None else "java " + source_file + " > " + out_file + " < " + self.stdin,
                volumes = [VOLUME_PATH],
                host_config = self.client.create_host_config(binds = {
                    host_path: {
                        'bind': VOLUME_PATH,
                        'mode': 'rw'
                    }
                })
            )
        elif lang == "c":
            pass
        elif lang == "c++":
            pass

        # Start the container
        self.client.start(self.container)

        # Initialise listener
        self.listener = threading.Thread(target = self.__listen)
        self.listener.start()
    
    def kill(self):
        self.client.stop(self.container) # Stop the container

    def __listen(self):
        logs = self.client.logs(
            self.container,
            stdout = True,
            stream = True
        )
        for line in logs:
            pass
        
        # Once this code is reached, the container is dead
        self.on_finish(OUTPUT_FILENAME)
        self.on_close()
        self.client.remove_container(self.container) # Remove the container