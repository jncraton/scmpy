## Building a Lisp Interpreter

This document outlines the construction of a minimalist s-expression interpreter using test-driven development.

---

### Step 1: Initial Test for Basic Arithmetic

We begin by defining the interface and adding the first requirement. The interpreter must handle prefix notation for addition using a default environment.

```python
def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    Evaluates `sexp` in `env`

    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 2, -7])
    -5
    """
    pass
```

---

### Step 2: Implementing Basic Function Evaluation

To pass the first tests, the interpreter must distinguish between atoms and lists. It evaluates all elements of a list and applies the first element to the rest if it is callable.

**Diff from Step 1**
```diff
--- Step 1
+++ Step 2
@@ -9,4 +9,10 @@
     >>> eval(['+', 2, -7])
     -5
     """
-    pass
+    if not isinstance(sexp, list):
+        return sexp
+
+    results = [eval(expr, env) for expr in sexp]
+    if callable(results[0]):
+        return results[0](*results[1:])
+    return results[-1]
```

**Complete Code**
```python
def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    Evaluates `sexp` in `env`

    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 2, -7])
    -5
    """
    if not isinstance(sexp, list):
        return sexp

    results = [eval(expr, env) for expr in sexp]
    if callable(results[0]):
        return results[0](*results[1:])
    return results[-1]
```

---

### Step 3: Tests for Sequences and Nesting

We add requirements for handling sequences of expressions and nested subexpressions.

```python
def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    Evaluates `sexp` in `env`

    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 2, -7])
    -5

    >>> eval([['+', 1, 1], ['+', 2, 2]])
    4

    >>> eval(['+', 1, ['+', 2, 2]])
    5
    """
    if not isinstance(sexp, list):
        return sexp

    results = [eval(expr, env) for expr in sexp]
    if callable(results[0]):
        return results[0](*results[1:])
    return results[-1]
```

**Note:** No implementation changes are required for Step 3. The recursive nature of the existing `eval` already handles sequences and nesting.

---

### Step 4: Tests for Variable Scoping

The interpreter must support symbol lookup across multiple nested dictionaries representing scopes.

```python
def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    Evaluates `sexp` in `env`

    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 2, -7])
    -5

    >>> eval([['+', 1, 1], ['+', 2, 2]])
    4

    >>> eval(['+', 1, ['+', 2, 2]])
    5

    >>> eval('x', env=[{'x': 1}])
    1

    >>> eval('x', env=[{'x': 2}, {'x': 4}])
    2
    """
    if not isinstance(sexp, list):
        return sexp

    results = [eval(expr, env) for expr in sexp]
    if callable(results[0]):
        return results[0](*results[1:])
    return results[-1]
```

---

### Step 5: Implementing Scope Lookup

We add logic to resolve strings by searching through the environment stack.

**Diff from Step 4**
```diff
--- Step 4
+++ Step 5
@@ -19,6 +19,8 @@
     >>> eval('x', env=[{'x': 2}, {'x': 4}])
     2
     """
+    if isinstance(sexp, str):
+        return next(scope[sexp] for scope in env if sexp in scope)
     if not isinstance(sexp, list):
         return sexp
```

**Complete Code**
```python
def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    Evaluates `sexp` in `env`

    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 2, -7])
    -5

    >>> eval([['+', 1, 1], ['+', 2, 2]])
    4

    >>> eval(['+', 1, ['+', 2, 2]])
    5

    >>> eval('x', env=[{'x': 1}])
    1

    >>> eval('x', env=[{'x': 2}, {'x': 4}])
    2
    """
    if isinstance(sexp, str):
        return next(scope[sexp] for scope in env if sexp in scope)
    if not isinstance(sexp, list):
        return sexp

    results = [eval(expr, env) for expr in sexp]
    if callable(results[0]):
        return results[0](*results[1:])
    return results[-1]
```

---

### Step 6: Tests for Lambda and If

We introduce anonymous function creation and conditional logic.

```python
def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    ... (previous tests) ...

    >>> eval([['lambda', ['n'], ['+', 'n', 'n']], 2])
    4

    >>> eval(['if', 1, 2, 3])
    2

    >>> eval(['if', 0, 2, 3])
    3
    """
    # implementation same as Step 5
```

---

### Step 7: Implementing Lambda and If

The interpreter now identifies special forms. `lambda` captures the current environment and creates a new scope upon execution. `if` provides short-circuiting.

**Diff from Step 6**
```diff
--- Step 6
+++ Step 7
@@ -34,6 +34,11 @@
     if not isinstance(sexp, list):
         return sexp
 
+    if sexp[0] == "lambda":
+        return lambda *args: eval(sexp[2], [dict(zip(sexp[1], args))] + env)
+    if sexp[0] == "if":
+        return eval(sexp[2], env) if eval(sexp[1], env) else eval(sexp[3], env)
+
     results = [eval(expr, env) for expr in sexp]
     if callable(results[0]):
```

**Complete Code**
```python
def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    Evaluates `sexp` in `env`

    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 2, -7])
    -5

    >>> eval([['+', 1, 1], ['+', 2, 2]])
    4

    >>> eval(['+', 1, ['+', 2, 2]])
    5

    >>> eval('x', env=[{'x': 1}])
    1

    >>> eval('x', env=[{'x': 2}, {'x': 4}])
    2

    >>> eval([['lambda', ['n'], ['+', 'n', 'n']], 2])
    4

    >>> eval(['if', 1, 2, 3])
    2

    >>> eval(['if', 0, 2, 3])
    3
    """
    if isinstance(sexp, str):
        return next(scope[sexp] for scope in env if sexp in scope)
    if not isinstance(sexp, list):
        return sexp

    if sexp[0] == "lambda":
        return lambda *args: eval(sexp[2], [dict(zip(sexp[1], args))] + env)
    if sexp[0] == "if":
        return eval(sexp[2], env) if eval(sexp[1], env) else eval(sexp[3], env)

    results = [eval(expr, env) for expr in sexp]
    if callable(results[0]):
        return results[0](*results[1:])
    return results[-1]
```

---

### Step 8: Tests for Define and Complex Recursion

The final requirements include binding names in the environment and computing Fibonacci numbers using different approaches.

```python
def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    ... (previous tests) ...

    >>> eval([['define', 'x', 2], 'x'])
    2

    >>> eval([
    ...   ['lambda', ['f', 'n'], ['f', 'f', 'n', 0, 1]],
    ...   ['lambda', ['self', 'count', 'cur', 'next'],
    ...     ['if', 'count',
    ...       ['self', 'self', ['+', 'count', -1], 'next', ['+', 'cur', 'next']],
    ...        'cur'],
    ...   ], 10
    ... ])
    55

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
    # implementation same as Step 7
```

---

### Step 9: Final Implementation with Define

We add the `define` special form to mutate the local environment scope.

**Diff from Step 8**
```diff
--- Step 8
+++ Step 9
@@ -40,6 +40,8 @@
         return lambda *args: eval(sexp[2], [dict(zip(sexp[1], args))] + env)
     if sexp[0] == "if":
         return eval(sexp[2], env) if eval(sexp[1], env) else eval(sexp[3], env)
+    if sexp[0] == "define":
+        env[0][sexp[1]] = eval(sexp[2], env)
 
     results = [eval(expr, env) for expr in sexp]
     if callable(results[0]):
```

**Complete Code**
```python
def eval(sexp, env=[{"+": lambda a, b: a + b}]):
    """
    Evaluates `sexp` in `env`

    >>> eval(['+', 1, 1])
    2

    >>> eval(['+', 2, -7])
    -5

    >>> eval([['+', 1, 1], ['+', 2, 2]])
    4

    >>> eval(['+', 1, ['+', 2, 2]])
    5

    >>> eval('x', env=[{'x': 1}])
    1

    >>> eval('x', env=[{'x': 2}, {'x': 4}])
    2

    >>> eval([['lambda', ['n'], ['+', 'n', 'n']], 2])
    4

    >>> eval(['if', 1, 2, 3])
    2

    >>> eval(['if', 0, 2, 3])
    3

    >>> eval([['define', 'x', 2], 'x'])
    2

    >>> eval([
    ...   ['lambda', ['f', 'n'], ['f', 'f', 'n', 0, 1]],
    ...   ['lambda', ['self', 'count', 'cur', 'next'],
    ...     ['if', 'count',
    ...       ['self', 'self', ['+', 'count', -1], 'next', ['+', 'cur', 'next']],
    ...        'cur'],
    ...   ], 10
    ... ])
    55

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
        if callable(results[0]):
            return results[0](*results[1:])
        return results[-1]
```