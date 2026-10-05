import random
import datetime
from pathlib import Path


# variable control
date = datetime.datetime.now()
port_connected = ".server"
port_num = 1

# load layer
print("vsbalm 1.0.0 -", date, "port: "+ port_connected)

while True:
    # functions
    # baseline open?
    def openbalm(file):
        with open(file) as f:
            print(f.read())

    # start vbalm connection
    def checkport():
        file_path = Path(f"con_{port_num}.balm")
        # Exists?
        if file_path.is_file():
            openbalm()

        # it does not .create new connection
        else:
           f =  open(f"con_{port_num}.balm", "x")


    # main layer
    command = input("vb > ")

    # check system
    if command == "port":
        checkport()

