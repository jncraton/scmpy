all: test

test:
	python3 -m doctest scm.py

clean:
	rm -rf __pycache__
