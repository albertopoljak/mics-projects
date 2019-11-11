"""
Some functions made to be as simple as possible and yet still readable and functional.
Without Regex, just pure Python.
"""

from typing import Callable


def camel_to_snake(word: str) -> str:
    """
    Will not work for repeating uppercase letters example:
    input: exampleImproperCAMELCaseToSnakeCase
    output: example_improper_c_a_m_e_l_case_to_snake_case

    :param word: word in camelCase to be converted to snake_case
    :return: snake_case equivalent of the word - if word is not camelCase then just return the word
    """

    if word and word[0].islower():
        word = list(word)

        upper_indexes = [index for index, char in enumerate(word) if char.isupper()]
        insertion = 0
        for index in upper_indexes:
            moved_index = index + insertion
            word[moved_index] = word[moved_index].lower()
            word.insert(moved_index, "_")
            insertion += 1

        return "".join(word)
    else:
        return word


def snake_to_camel(word: str) -> str:
    """
    :param word:  word in snake_case to be converted to camelCase
    :return: camelCase equivalent of the word - if word is not snake_case then just return the word
    """

    if word and word[0].islower():
        word = list(word)

        underscore_indexes = [index for index, char in enumerate(word) if char == "_"]
        deletion = 0
        for index in underscore_indexes:
            moved_index = index - deletion
            del word[moved_index]
            word[moved_index] = word[moved_index].upper()
            deletion += 1

        return "".join(word)
    else:
        return word


if __name__ == "__main__":
    camel_to_snake_tests = ("camelCaseToSnakeCaseTest",
                            "exampleImproperCAMELCaseToSnakeCase",
                            "ExampleImproperPascalCase",
                            "")

    snake_to_camel_tests = ("snake_case_to_camel_case_test",
                            "snake_case__to___camel____case_____test_____example",
                            "example_IMPROPER___snake___case_to_camel_case_test",
                            "Example_improper_snake_case",
                            "")

    def print_tests(tests: tuple, converter_function: Callable):
        for test in tests:
            six_space = " " * 6
            three_space = " " * 3
            print(f"{six_space}{test if test else '(empty string)'}\n{three_space}-->{converter_function(test)}")

    print("Camel to snake:")
    print_tests(camel_to_snake_tests, camel_to_snake)

    print("Snake to camel:")
    print_tests(snake_to_camel_tests, snake_to_camel)
