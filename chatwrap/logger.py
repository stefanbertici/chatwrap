def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"### Calling {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"### Result: {result}")
        return result
    return wrapper