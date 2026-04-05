def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 1, ['+', 2, 2]])
    5

    >>> eval(['+', 2, -7])
    -5

    Anonymous `double` function
    >>> eval([['lambda', ['n'], ['+', 'n', 'n']], 2])
    4

    >>> eval(['if', 1, 2, 3])
    2

    >>> eval(['if', 0, 2, 3])
    3

    Fibonacci
    >>> eval([
    ...     ['lambda', ['f', 'n'], ['f', 'f', 'n', 0, 1]],
    ...     ['lambda', ['self', 'count', 'current', 'next'],
    ...         ['if', 'count',
    ...             ['self', 'self', ['+', 'count', -1], 'next', ['+', 'current', 'next']],
    ...             'current']],
    ...     10
    ... ])
    55
    """

    if isinstance(sexp, str):
        return next(scope[sexp] for scope in env if sexp in scope)
    if not isinstance(sexp, list):
        return sexp

    if sexp[0] == "lambda":
        return lambda *args: eval(sexp[2], [dict(zip(sexp[1], args))] + env)
    elif sexp[0] == "if":
        return eval(sexp[2], env) if eval(sexp[1], env) else eval(sexp[3], env)
    else:
        return eval(sexp[0], env)(*[eval(arg, env) for arg in sexp[1:]])
