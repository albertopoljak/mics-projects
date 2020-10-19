import setuptools  # needed otherwise error "Unable to find vcvarsall.bat"
from distutils.core import setup, Extension


def main():
    setup(
        name="is_prime",
        version="1.0.0",
        description="Python3 interface for the prime C library function",
        author="Braindead",
        ext_modules=[Extension("is_prime", ["prime.c"])]
    )


if __name__ == "__main__":
    main()
