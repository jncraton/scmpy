all: test

test:
	python3 -m doctest scm.py
