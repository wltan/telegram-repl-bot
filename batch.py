import docker
import os
import threading
import time

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
            self.container = self.client.create_container(
                image = "python",
                detach = False,
                tty = False,
                command = "sh -c 'python3.8 " + source_file + " > " + out_file + "'" if self.stdin is None else "sh -c 'python3.8 " + source_file + " > " + out_file + " < " + self.stdin + "'",
                volumes = [VOLUME_PATH],
                host_config = self.client.create_host_config(binds = {
                    host_path: {
                        'bind': VOLUME_PATH,
                        'mode': 'rw'
                    }
                })
            )
        elif lang == "java":
            self.container = self.client.create_container(
                image = "java",
                detach = False,
                tty = False,
                command = "sh -c 'java " + source_file + " > " + out_file + "'" if self.stdin is None else "sh -c 'java " + source_file + " > " + out_file + " < " + self.stdin + "'",
                volumes = [VOLUME_PATH],
                host_config = self.client.create_host_config(binds = {
                    host_path: {
                        'bind': VOLUME_PATH,
                        'mode': 'rw'
                    }
                })
            )
        elif lang == "c":
            self.container = self.client.create_container(
                image = "c-batch",
                detach = False,
                tty = False,
                command = "sh -c 'gcc " + source_file + " -o out && ./out > " + out_file + "'" if self.stdin is None else "sh -c 'gcc " + source_file + " -o out && ./out > " + out_file + " < " + self.stdin + "'",
                volumes = [VOLUME_PATH],
                host_config = self.client.create_host_config(binds = {
                    host_path: {
                        'bind': VOLUME_PATH,
                        'mode': 'rw'
                    }
                })
            )
        elif lang == "c++":
            pass

        # Initialise listener
        self.listener = threading.Thread(target = self.__listen)
        self.listener.start()
    
    def kill(self):
        self.client.stop(self.container) # Stop the container

    def __listen(self):
        # Start the container
        self.client.start(self.container)

        # Ensure that file is released before reading
        time.sleep(0.5)

        # Once this code is reached, the container is dead
        self.on_finish(OUTPUT_FILENAME)
        self.on_close()
        self.client.remove_container(self.container) # Remove the container