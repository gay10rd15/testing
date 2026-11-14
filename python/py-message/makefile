SHELL := /bin/bash

main:
	. ../../.venv/bin/activate
	pyinstaller --onefile --add-data Main.tcss:. message.py
	ditto dist/ ../../dist
clean:
	rm -rf build/ dist/ *.spec