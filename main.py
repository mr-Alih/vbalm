import random
import datetime
import json
import uuid
import shutil
import shlex
from pathlib import Path

# idea init
# connection = hard memory, lives on disk (con_<port>.balm), links a server id to a local workspace
# session    = short ram memory, state machine, dies when you exit

date = datetime.datetime.now()
print("vsbalm 1.0.0 -", date)


# ---------- error control ----------
def error(messagesort):
    if messagesort == "wdir":
        print("error - wrong direction rep.")
    else:
        print("error FALSE N 404")


# ---------- connection (on disk) ----------
def init_server(path):
    """Make sure the server folder exists and has an id. Returns the id."""
    p = Path(path)
    p.mkdir(exist_ok=True)
    id_file = p / ".server_id"
    if not id_file.exists():
        id_file.write_text("srv_" + uuid.uuid4().hex[:8])
    return id_file.read_text().strip()


def create_connection(port, server_path="./server", local_path="./local"):
    data = {
        "server_id": init_server(server_path),
        "port": port,
        "server_path": server_path,
        "local_path": local_path,
        "created": str(datetime.datetime.now()),
    }
    Path(f"con_{port}.balm").write_text(json.dumps(data, indent=2))
    return data


def read_connection(port):
    f = Path(f"con_{port}.balm")
    if not f.is_file():
        return None
    try:
        return json.loads(f.read_text())
    except json.JSONDecodeError:
        # empty/old file from the first version, treat as no connection
        return None


def verify_connection(conn):
    id_file = Path(conn["server_path"]) / ".server_id"
    return id_file.is_file() and id_file.read_text().strip() == conn["server_id"]


# ---------- session (in RAM) ----------
class Session:
    def __init__(self):
        self.id = random.randint(1000, 9999)
        self.state = "disconnected"  # disconnected -> connected -> loaded
        self.conn = None
        self.started = datetime.datetime.now()

    def connect(self, port):
        conn = read_connection(port)
        if conn is None:
            print("Connection file does not exist or is invalid.")
            print("Creating new connection...")
            conn = create_connection(port)
        else:
            print("Connection file found.")

        if not verify_connection(conn):
            print("error - server id mismatch, connection refused.")
            return

        self.conn = conn
        self.state = "connected"
        print(f"connected: port {port}, server {conn['server_id']}, session [{self.id}]")

    def require(self, *states):
        if self.state not in states:
            print(f"error - need state {states}, you are '{self.state}'.")
            return False
        return True

    def status(self):
        print("session:", self.id, "| state:", self.state)
        if self.conn:
            print("server:", self.conn["server_id"], "| port:", self.conn["port"])
            print("server path:", self.conn["server_path"], "| local path:", self.conn["local_path"])

    def disconnect(self):
        self.conn = None
        self.state = "disconnected"


# ---------- file commands ----------
def visible_files(folder):
    """Only real files, skip hidden ones like .server_id"""
    return [i for i in folder.iterdir() if i.is_file() and not i.name.startswith(".")]


def load(s, source=None):
    if not s.require("connected", "loaded"):
        return

    # no folder given -> load from the connected server
    folder = Path(source) if source else Path(s.conn["server_path"])
    local = Path(s.conn["local_path"])

    if not folder.is_dir():
        error("wdir")
        return

    if folder.resolve() == local.resolve():
        print("error - source and local workspace are the same folder.")
        return

    files = visible_files(folder)
    if not files:
        error("wdir")
        return

    print(f"files found: {folder}/", [f.name for f in files])
    print("copying to workspace...")

    local.mkdir(exist_ok=True)
    for item in files:
        shutil.copy2(item, local / item.name)

    s.state = "loaded"
    print("done.")


def push(s):
    if not s.require("loaded"):
        return

    local = Path(s.conn["local_path"])
    server = Path(s.conn["server_path"])

    if not local.is_dir():
        print("Nothing to push. Run load first.")
        return

    if not verify_connection(s.conn):
        print("error - server id mismatch, push refused.")
        return

    server.mkdir(exist_ok=True)
    print("Versonic balm pushing...")

    for item in visible_files(local):
        shutil.copy2(item, server / item.name)

    print("done.")


# ---------- main loop ----------
s = Session()

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
        try:
            port = int(args[0]) if args else 1
        except ValueError:
            print("error - port must be a number.")
            continue
        s.connect(port)

    elif cmd == "session" and args == ["status"]:
        s.status()

    elif cmd == "load":
        load(s, args[0] if args else None)

    elif cmd == "push":
        push(s)

    elif cmd == "disconnect":
        s.disconnect()
        print("disconnected.")

    elif cmd == "exit":
        print("Closing... vsbalm.")
        break

    else:
        print("Unknown command.")