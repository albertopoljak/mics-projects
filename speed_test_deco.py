from timeit import default_timer as timer


def speed_test(func):
    def wrapper():
        start = timer()
        func()
        print(f"{func.__name__} took {timer() - start} seconds.")
    return wrapper


@speed_test
def some_function():
    for i in range(1, 1000000):
        _ = i**0.5


some_function()
