SHELL := /bin/bash

main: Madd.py
	pyinstaller --onefile --add-data None.png:. --add-data Madd.tcss:. --hidden-import=crossfiledialog Madd.py
	ditto dist/ ../../dist/

clean:
	rm -rf build/ dist/ *.spec