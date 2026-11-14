import random
import subprocess


class Math:
    @staticmethod
    def fseq(num):
        try:
            a, b = 0, 1
            for _ in range(int(num)):
                a, b = b, a + b
            return a
        except ValueError, TypeError:
            return "Enter a number, not anything else"


class Misc:
    @staticmethod
    def piglatin(args):
        if isinstance(args, list):
            ui = " ".join(args)
        else:
            ui = args

        result = []
        for words in ui.split():
            if not words:
                continue
            if words[0].lower() in "aeiou":
                result.append(words + "-yay")
            else:
                result.append(words[1:] + "-" + words[0] + "ay")
        return " ".join(result)

    @staticmethod
    def myip():
        result = subprocess.run(
            ["ipconfig", "getifaddr", "en0"],
            check=False,
            capture_output=True,
            text=True,
        )
        print("your ip is: " + result.stdout.strip())

    @staticmethod
    def passwordgen():
        password = []
        for i in range(14):
            if i < 4:
                password.append(chr(random.randint(65, 90)))
                continue
            elif i < 8:
                password.append(chr(random.randint(97, 122)))
                continue
            elif i < 15:
                # pyrefly: ignore [bad-argument-type]
                password.append(random.randint(1, 9))
                continue
        random.shuffle(password)
        print(*password, sep="")


class Tools:
    @staticmethod
    def man(command="man"):
        manpages = {
            "fibseq": "Does the Fibonacci sequence the number of times entered.\nRequires one input.",
            "piglatin": "Takes a string and turns it into Pig Latin.\nJust enter plain text.",
            "man": "Welcome to man, which shows lots of information about a command!",
            "help": "Lists all available commands.",
            "myip": "show your ip address",
            "password": "generate a random password",
        }
        if command in manpages:
            return manpages[command]
        return f"No man page for '{command}'"

    @staticmethod
    def help():
        return ", ".join(commands.keys())


commands = {
    "fibseq": Math.fseq,
    "piglatin": Misc.piglatin,
    "help": Tools.help,
    "man": Tools.man,
    "myip": Misc.myip,
    "password": Misc.passwordgen,
}


def shell():
    while True:
        try:
            command = input("pysh >>> ").strip()
        except EOFError:
            print("\nexiting")
            break

        if command == "quit":
            print("exiting")
            break

        if not command:
            continue

        parts = command.split()
        commandname = parts[0]
        args = " ".join(parts[1:]) if len(parts) > 1 else None

        if commandname in commands:
            func = commands[commandname]
            try:
                if args:
                    # pyrefly: ignore [bad-argument-count]
                    result = func(args)
                else:
                    # pyrefly: ignore [missing-argument]
                    result = func()

                if result is not None:
                    print(result)
            except Exception as e:  # noqa: BLE001
                print(f"Error executing command: {e}")
        else:
            print(f"not a valid command: {commandname}")


if __name__ == "__main__":
    shell()
