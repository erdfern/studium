from typing import List


def assert_list_of_integers(input_list):
    if not isinstance(input_list, list) or not all(
        isinstance(item, int) for item in input_list
    ):
        raise TypeError("List must be of type List[int]")


def find_individual(lst: List[int]) -> int:
    """
    Given an array of integers in which all elements except one appear exactly twice,
    finds the individual element.

    Example:
    ```
    > find_individual([1,2,3,4,3,1,2])
    > 4
    ```
    """
    if len(lst) == 0 or len(lst) % 2 == 0:
        raise ValueError("Length is ")
    assert_list_of_integers(lst)

    element_counts = dict.fromkeys(lst, 0)
    # XOR based method
    # Since `a xor a = 0` and `a xor 0 = a` for any integer `a`, and XOR is commutative and associative,
    # we can find the unique element in the list by XOR-ing all the elements.
    # All elements that appear twice will cancel out, only leaving the unique element.
    result = 0
    for el in lst:
        element_counts[el] += 1
        result ^= el

    # These checks are somewhat expensive, but necessary. At least we can use generator expressions.
    unique_elements = [
        el for el, count in element_counts.items() if count == 1
    ]
    if len(unique_elements) != 1:
        raise ValueError(
            "There should be exactly one unique element that appears once"
        )

    multiple_occurrence_elements = [
        el for el, count in element_counts.items() if count > 2
    ]
    if multiple_occurrence_elements:
        raise ValueError("All elements except one should appear exactly twice")

    return result


def _main():
    find_individual([1, 1, 2, 3, 3])


if __name__ == "__main__":
    _main()
