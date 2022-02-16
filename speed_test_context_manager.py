from time import process_time
from contextlib import contextmanager


@contextmanager
def timer():
    start = process_time()
    try:
        yield
    finally:
        end = process_time()
        print(f"Task finished in {end - start} seconds.")


def example():
    for i in range(1, 1000000):
        _ = i**0.5


if __name__ == "__main__":
    with timer():
        example()
