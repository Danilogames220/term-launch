all: build

build:
	pyinstaller --onefile -n terml main.py

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf __pycache__/
	rm -f *.spec

run:
	python3 main.py
