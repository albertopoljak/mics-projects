"""High precision timing speed execution decorator."""
from timeit import default_timer as timer


def speed_test(func):
    def wrapper(*args, **kwargs):
        start = timer()
        func(*args, **kwargs)
        print(f"{func.__name__} took {timer() - start} seconds.")
    return wrapper


@speed_test
def example():
    for i in range(1, 1000000):
        _ = i**0.5


if __name__ == "__main__":
    example()
