env = {
    '+': lambda a, b: a + b,
}

def eval(sexp, env=env):
    """
    >>> eval(['+', 1, 1])
    2
    """

    if isinstance(sexp[0], str):
        return env[sexp[0]](*sexp[1:])