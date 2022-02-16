from time import process_time


def speed_test(func):
    def wrapper(*args, **kwargs):
        start = process_time()
        func(*args, **kwargs)
        end = process_time()
        print(f"{func.__name__} took {end - start} seconds.")
    return wrapper


@speed_test
def example():
    for i in range(1, 1000000):
        _ = i**0.5


if __name__ == "__main__":
    example()
