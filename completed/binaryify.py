from pathlib import Path
import subprocess

Home = Path.home()
final_dir = Home / "testing/completed"
def main():
    for files in final_dir.iterdir():
        if files.suffix == ".py":   
            subprocess.run(["pyinstaller", "--onefile", "--log-level", "WARN", "--distpath", "/Users/Gaylord/testing/dist", str(files)], check=True)   
            subprocess.run("rm -rf ~/testing/build", shell=True)
            subprocess.run("rm ~/testing/*.spec", shell=True)   
            print(files)

if __name__ == "__main__":
    main()