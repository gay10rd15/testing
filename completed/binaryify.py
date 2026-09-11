import subprocess
from pathlib import Path

Home = Path.home()
final_dir = Home / "testing/completed"


def main():
    for files in final_dir.iterdir():
        if files.suffix == ".py":
            subprocess.run(
                [
                    "pyinstaller",
                    "--onefile",
                    "--log-level",
                    "WARN",
                    "--distpath",
                    "/Users/parkerellering/testing/dist",
                    str(files),
                ],
                check=True,
            )
            subprocess.run("rm -rf build/", check=False, shell=True)
            subprocess.run(
                "rm *.spec",
                check=False,
                shell=True,
            )
            print(files)


if __name__ == "__main__":
    main()
