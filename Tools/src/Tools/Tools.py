from pathlib import Path
import questionary
import os, inspect # noqa: E401

def getpath():
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    return os.path.dirname(os.path.abspath(caller_file))

class filemanip:
    def __init__(self, file_name, path, perm):
        self.name = file_name
        self.path = Path(path)
        self.perm = perm
        self.full_path = self.path / self.name 
        self.content = None

        if "r" in self.perm:
            try:
                self.content = self.full_path.read_text()
            except FileNotFoundError:
                yn = input("File not found. Create it? (y/n): ")
                if yn.lower() == "y":
                    self.full_path.touch()
                    self.content = self.full_path.read_text()
                    print("File created.")
                else:
                    print("File not created.")
        #uw stands for user write 
        #i may integrate a different write feature 
        #for the people making code
        elif "uw" in self.perm:
            print("write mode, enter 'DONE' to finish writing:")
            with open(self.full_path, "w") as f:
                lines = []
                while True:
                    line = input()
                    if line.upper() == "DONE":
                        break
                    lines.append(line)

                # Join the list into a single multiline string
                final_text = "\n".join(lines)
                f.write(final_text)

        #elif "w" in self.perm:
            

        elif "a" in self.perm:
            with open(self.full_path, "a") as f:
                print("Enter text to append (type 'DONE' to finish):\n> ")
                lines = []
                while True:
                    line = input()
                    if line.upper() == "DONE":
                        break
                    lines.append(line)

                    # Join the list into a single multiline string
                    final_text = "\n".join(lines)
                    f.write(final_text)

def qa(text, *questions, answer=""):
    selected = questionary.select(text, choices=list(questions)).ask()
    if answer != "":
        if selected == answer:
            print("That is correct!")
        else:
            print(f"Sorry, the correct answer is {answer}.")

def beep():
    os.system('afplay /System/library/sounds/glass.aiff')

class PathError():
    def __inti__(self, message="the path selected does not exist"):
        super().__init__(self.message)
