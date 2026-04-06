all: test

test:
	uv run python -m doctest scm.py

lint:
	uvx black@24.1.0 --check .

format:
	uvx black@24.1.0 .

index.html: slides.md
	pandoc -t revealjs -V revealjs-url=https://jncraton.github.io/reveal-themes/reveal.js -c https://jncraton.github.io/reveal-themes/purple.css -s $< -o $@

clean:
	rm -rf __pycache__
