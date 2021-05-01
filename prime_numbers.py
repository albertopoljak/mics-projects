from typing import Generator


def get_mersenne_number(exponent: int) -> int:
    return 2**exponent - 1


def mersenne_generator(max_exponent: int) -> Generator[int, None, None]:
    for i in range(1, max_exponent + 1):
        yield get_mersenne_number(i)


def is_prime(number: int) -> bool:
    # Only odd numbers can be primes (except 2)
    if number & 1:

        # No prime number greater than 5 ends in a 5
        if number > 5 and number % 5 == 0:
            return False

        # You can loop up to, including, the square root of the number
        # Skip even numbers as odd%even will never be divisible without reminder
        for i in range(3, int(number**0.5)+1, 2):
            if number % i == 0:
                return False
        return True
    else:
        # The only even number which is a prime is 2
        return number == 2


def test_is_prime() -> bool:
    with open("primes.txt") as f:
        primes = tuple(int(x) for x in f.read().split(","))

    for prime in primes:
        if not is_prime(prime):
            return False

    not_primes = set(primes) ^ set(range(2, primes[-1] + 1))
    for not_prime in not_primes:
        if is_prime(not_prime):
            return False

    return True


if __name__ == "__main__":
    import cProfile
    # Around 2.12s for checking first 1m numbers (x64 CPython3.8 i5-4590S)
    cProfile.run("""for number in range(1_000_000): is_prime(number)""")
    # Around 0.015s to check first n mersenne numbers in range of max exponent of 60
    # (59 numbers generated last one is 1152921504606846975)
    cProfile.run("""for number in mersenne_generator(60): is_prime(number)""")
