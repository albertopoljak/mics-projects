import math
from typing import Generator


def get_mersenne_number(exponent: int) -> int:
    return 2**exponent - 1


def mersenne_generator(max_exponent: int) -> Generator[int, None, None]:
    for i in range(1, max_exponent + 1):
        yield(get_mersenne_number(i))


def is_prime(number: int) -> bool:
    if number < 2:
        return False

    # You can loop up to including the square root of the number
    for i in range(2, int(math.sqrt(number))+1):
        if number % i == 0:
            return False
    return True


if __name__ == "__main__":
    import cProfile
    cProfile.run("""for number in range(1000000): is_prime(number)""")
    cProfile.run("""for number in mersenne_generator(60): is_prime(number)""")