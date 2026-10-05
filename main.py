import random
import datetime
from pathlib import Path


# init variables
date = datetime.datetime.now()
port_num = 1
port_connected = ".server"


print("vsbalm 1.0.0 -", date, "port:", port_connected)

# session lib
def session(sestype):
    if sestype == "connect":
        session_id = random.randint(1000, 9999)
        connection = f"con_{port_num} - type [{session_id}]"
        print("\nSuccess session connection")
        return connection

    elif sestype == "status":
        print("control:", port_connected)
        print("port:", port_num)


# file control
def openbalm(bfile):
    with open(bfile) as f:
        print(f.read())


# port control
def checkport():
    file_path = Path(f"con_{port_num}.balm")

    if file_path.is_file():
        print("Connection file found.")
        openbalm(file_path)

    else:
        print("Connection file does not exist.")
        print("Creating new connection...")

        with open(file_path, "x"):
            pass
    return session("connect")


# main loop

while True:
    command = input("vb > ")

    if command == "port":
        port_connected = checkport()

    elif command == "session status":
        session("status")

    elif command == "exit":
        print("Closing... vsbalm.")
        break

    else:
        print("Unknown command.")