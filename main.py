import random
import datetime
from pathlib import Path
import shutil


# init variables
date = datetime.datetime.now()
port_num = 1
port_connected = ".server"

server_files = []

# idea init
# connection is the server base. it reads and produces
# the session does the work itself, its short ram memory whhile con is hard memory


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

    elif command.startswith("load"):
        folder = Path(f"./{command[5:]}")
        server_files = []

        for item in folder.iterdir():
            if item.is_file():
                server_files.append(item.name)

        print(f"files found: {command[5:]}/", server_files)
        print("copying to workspace...")

        local = Path("./local")

        for item in folder.iterdir():
            if item.is_file():
                shutil.copy2(item, local / item.name)

        # after loading the files repeat connection.

    elif command == "reload":
        return()
    
    elif command == "connection status":
        return()

    elif command.startswith("load"):
        return()

    
    

    else:
        print("Unknown command.")