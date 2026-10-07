import random
import datetime
from pathlib import Path
import shutil
import shlex

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

def load(command):
    if not command:
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
    try:
        parts = shlex.split(input("vb > "))
    except ValueError:
        print("Bad quotes in command.")
        continue

    if not parts:
        continue

    cmd, args = parts[0], parts[1:]

    if cmd == "port":
        port_connected = checkport()

    elif cmd == "session" and args == ["status"]:
        session("status")

    elif cmd == "load":
        load(args[0] if args else None)

    elif cmd == "push":
        local = Path("./local")
        server = Path("./server")

        if not local.is_dir():
            print("Nothing to push. Run load first.")
            continue

        server.mkdir(exist_ok=True)
        print("Versonic balm pushing...")

        for item in local.iterdir():
            if item.is_file():
                shutil.copy2(item, server / item.name)

    elif cmd == "exit":
        print("Closing... vsbalm.")
        break

    else:
        print("Unknown command.")