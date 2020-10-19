from typing import Generator


def get_mersenne_number(exponent: int) -> int:
    return 2**exponent - 1


def mersenne_generator(max_exponent: int) -> Generator[int, None, None]:
    for i in range(1, max_exponent + 1):
        yield get_mersenne_number(i)


def is_prime(number: int) -> bool:
    if number < 2:
        return False

    # You can loop up to including the square root of the number
    for i in range(2, int(number**0.5)+1):
        if number % i == 0:
            return False
    return True


if __name__ == "__main__":
    import cProfile
    # Around 7.8s for checking first 1m numbers (i5-6600)
    cProfile.run("""for number in range(1000000): is_prime(number)""")
    # Around 0.043s to check first n mersenne numbers in range of max exponent of 60
    # (59 numbers generated last one is 1152921504606846975)
    cProfile.run("""for number in mersenne_generator(60): is_prime(number)""")