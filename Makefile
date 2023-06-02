.PHONY: start
start:
	pip3 install -r requirements.txt
	python3 Fetching/fetch.py
	g++ main.cpp -o Build/server
	./Build/server

build:
	pip3 install -r requirements.txt
	python3 Fetching/fetch.py
	npm install
	npm start

run:
	pip3 install -r requirements.txt
	python3 Fetching/fetch.py
	npm install
	npm start