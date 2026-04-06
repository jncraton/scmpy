def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    Evaluates `sexp` in `env`

    Function evaluation uses prefix notation.

    `+` is provided as a function in the default global `env`

    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 2, -7])
    -5

    Sequences of expressions return the value of the last expression

    >>> eval([['+', 1, 1], ['+', 2, 2]])
    4

    Nested subexpressions are properly evaluated

    >>> eval(['+', 1, ['+', 2, 2]])
    5

    Nested scopes shadow values

    >>> eval('x', env=[{'x': 1}])
    1

    >>> eval('x', env=[{'x': 2}, {'x': 4}])
    2

    `lambda` creates anonymous functions

    >>> eval([['lambda', ['n'], ['+', 'n', 'n']], 2])
    4

    `if` provides a ternary operator with short-circuit evaluation

    >>> eval(['if', 1, 2, 3])
    2

    >>> eval(['if', 0, 2, 3])
    3

    `define` binds a value to a name in the current scope

    >>> eval([['define', 'x', 2], 'x'])
    2

    n-th Fibonacci computation using Y-combinator

    >>> eval([
    ...   ['lambda', ['f', 'n'], ['f', 'f', 'n', 0, 1]],
    ...   ['lambda', ['self', 'count', 'cur', 'next'],
    ...     ['if', 'count',
    ...       ['self', 'self', ['+', 'count', -1], 'next', ['+', 'cur', 'next']],
    ...        'cur'],
    ...   ], 10
    ... ])
    55

    n-th Fibonacci computation using `define`

    >>> eval([
    ...   ['define', 'fib',
    ...     ['lambda', ['n'],
    ...       ['if', ['+', 'n', -1],
    ...         ['if', ['+', 'n', -2],
    ...           ['+', ['fib', ['+', 'n', -1]], ['fib', ['+', 'n', -2]]],
    ...           1],
    ...         1]]],
    ...   ['fib', 10]
    ... ])
    55
    """
    if isinstance(sexp, str):
        return next(scope[sexp] for scope in env if sexp in scope)
    if not isinstance(sexp, list):
        return sexp

    if sexp[0] == "lambda":
        return lambda *args: eval(sexp[2], [dict(zip(sexp[1], args))] + env)
    elif sexp[0] == "define":
        env[0][sexp[1]] = eval(sexp[2], env)
    elif sexp[0] == "if":
        return eval(sexp[2], env) if eval(sexp[1], env) else eval(sexp[3], env)
    else:
        results = [eval(expr, env) for expr in sexp]

        return results[0](*results[1:]) if callable(results[0]) else results[-1]
