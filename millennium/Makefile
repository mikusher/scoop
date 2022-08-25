.PHONY : all clean build upload

all: install clean

clean:
	@rm -rf `find ./ -type d -name "*__pycache__"`
	@rm -rf ./build/ ./dist/ ./millennium.egg-info/

install: build
	python3 setup.py install

build:
	python3 setup.py sdist bdist_wheel