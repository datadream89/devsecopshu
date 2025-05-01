def safe_exec(code: str, allowed_globals=None):
    # Define a restricted set of built-in functions
    safe_builtins = {
        'print': print,
        'range': range,
        'len': len,
        'int': int,
        'str': str,
        'float': float,
        'bool': bool,
        'dict': dict,
        'list': list,
        'set': set,
        'tuple': tuple,
        'enumerate': enumerate,
        'zip': zip,
        'abs': abs,
        'min': min,
        'max': max,
        'sum': sum,
        'sorted': sorted,
    }

    # Set up the restricted globals
    restricted_globals = {
        '__builtins__': safe_builtins
    }

    if allowed_globals:
        restricted_globals.update(allowed_globals)

    # Empty locals for isolation
    restricted_locals = {}

    try:
        exec(code, restricted_globals, restricted_locals)
    except Exception as e:
        print(f"Execution error: {e}")

    return restricted_locals
