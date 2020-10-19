""""
You will need to build&install is_prime c extension:
cd c_extensions/prime_numbers
python setup.py install

For last step it is advisable to be in virtual environment or similar.
Only after you install will you be able to use it (obviously), you need Python 3x to build.
"""


if __name__ == "__main__":
    import cProfile
    from is_prime import is_prime
    # Around 7.8s for checking first 10m numbers (i5-4590S 3GHz)
    cProfile.run("for number in range(10_000_000): is_prime(number)")
