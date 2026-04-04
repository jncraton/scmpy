env = {
    '+': lambda a, b: a + b,
}

def eval(sexp, env=env):
    """
    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 1, ['+', 2, 2]])
    5
    """

    if isinstance(sexp, int):
        return sexp
    elif isinstance(sexp[0], str):
        return env[sexp[0]](*map(eval, sexp[1:]))