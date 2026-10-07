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

# error control
def error(messagesort):
    if messagesort == "wdir":
        print("error - wrong direction rep.")
        return()
    else:
        print("error FALSE N 404")
        return()

def load():
    command = input("load > ")

    if not command.strip():
        error("")
        return

    folder = Path(f"./{command}")

    if not folder.is_dir():
        error("wdir")
        return

    server_files = []

    for item in folder.iterdir():
        if item.is_file():
            server_files.append(item.name)

    if not server_files:
        error("wdir")
        return

    print(f"files found: {command}/", server_files)
    print("copying to workspace...")

    local = Path("./local")
    local.mkdir(exist_ok=True)

    for item in folder.iterdir():
        if item.is_file():
            shutil.copy2(item, local / item.name)

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
        load()

        # after loading the files repeat connection.


    # elif command == "reload":
    #     return
    
    # elif command == "connection status":
    #     return()

    elif command.startswith("push"):
        folder = Path("./local")
        server_files = []
    
        for item in folder.iterdir():
            if item.is_file():
                server_files.append(item.name)
    
        print("Versonic balm pushing...")
    
        server = Path("./server")
    
        for item in folder.iterdir():
            if item.is_file():
                shutil.copy2(item, server / item.name)
    

    else:
        print("Unknown command.")