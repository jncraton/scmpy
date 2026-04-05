from functools import partial

env = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
}

def eval(sexp, env=env):
    """
    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 1, ['+', 2, 2]])
    5

    >>> eval(['-', 2, 7])
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
    ...     ['lambda', ['self', 'count', 'a', 'b'],
    ...         ['if', 'count',
    ...             ['self', 'self', ['-', 'count', 1], 'b', ['+', 'a', 'b']],
    ...             'a']],
    ...     10
    ... ])
    55
    """

    if isinstance(sexp, int):
        return sexp
    if isinstance(sexp, str):
        return env[sexp]
    elif isinstance(sexp, list):
        if sexp[0] == 'lambda':
            names = sexp[1]
            body = sexp[2]
            return lambda *args: eval(body, env | {k:v for k,v in zip(names, args)})
        elif sexp[0] == 'if':
            condition = eval(sexp[1], env)
            return eval(sexp[2], env) if condition else eval(sexp[3], env)
        else:
            return eval(sexp[0], env)(*map(partial(eval, env=env), sexp[1:]))
