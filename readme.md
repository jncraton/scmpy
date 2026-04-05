# scmpy

A minimal Scheme interpreter written in Python

# Features

1. Basic arithmetic
2. Lambda expressions
3. Conditional logic
4. Environment management

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
    ['lambda', ['f', 'n'], ['f', 'f', 'n', 0, 1]],
    ['lambda', ['self', 'count', 'a', 'b'],
        ['if', 'count',
            ['self', 'self', ['-', 'count', 1], 'b', ['+', 'a', 'b']],
            'a']],
    10
]
print(eval(fib))
```
