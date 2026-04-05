# scmpy

[![Release](https://github.com/jncraton/scmpy/actions/workflows/release.yml/badge.svg)](https://github.com/jncraton/scmpy/actions/workflows/release.yml)
[![Deploy](https://github.com/jncraton/scmpy/actions/workflows/deploy.yml/badge.svg)](https://github.com/jncraton/scmpy/actions/workflows/deploy.yml)
[![Test](https://github.com/jncraton/scmpy/actions/workflows/test.yml/badge.svg)](https://github.com/jncraton/scmpy/actions/workflows/test.yml)
[![Lint](https://github.com/jncraton/scmpy/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/scmpy/actions/workflows/lint.yml)

A minimal Scheme interpreter written in Python

# Features

1. Basic arithmetic
2. Lambda expressions
3. Conditional logic
4. Variable definition

# Usage

Call the eval function with [S-expressions](https://en.wikipedia.org/wiki/S-expression) as lists.

```python
from scm import eval
print(eval(['+', 1, 1]))
```

# Development
Use the makefile to test and format the code.

```bash
make test
make format
```

# Recursion

The project demonstrates computing [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_sequence) using a [Y-combinator](https://en.wikipedia.org/wiki/Fixed-point_combinator) pattern.

```python
from scm import eval
fib = [
    ['lambda', ['fib', 'n'], ['fib', 'fib', 'n', 0, 1]],
    ['lambda', ['f', 'count', 'cur', 'next'],
        ['if', 'count',
            ['f', 'f', ['+', 'count', -1], 'next', ['+', 'cur', 'next']],
            'cur']],
    10
]
print(eval(fib))
```

# Reference

Reference implementations of the Fibonacci Y-combinator are provided in fib-ycombinator.scm and fib-ycombinator.js.
