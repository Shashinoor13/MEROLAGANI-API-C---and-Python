.PHONY: start
start:
	pip3 install -r requirements.txt
	python3 Fetching/fetch.py
	g++ main.cpp -o Build/server
	./Build/server
