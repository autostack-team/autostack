import subprocess
from threading import Thread
   
if __name__ == '__main__':
    # Command to run the .d stdout script.
    cmd = ["sudo", "dtrace", "-q", "-s", "stdout.d"]

    # Listen for stdout.
    stdout_listener = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    # Listen for new stdout.
    while True:
        try:
            line = stdout_listener.stdout.readline().decode("utf-8")
            print(line)
        except UnicodeDecodeError:
            pass