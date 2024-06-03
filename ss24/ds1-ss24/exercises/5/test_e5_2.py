from e5_2 import find_individual
import pytest


# def test_example_case():
#     list = [1, 2, 3, 4, 3, 1, 2]
#     expected = 4
#     assert find_individual(list) == expected


def test_float_list():
    # bad type (not List[int])
    # This is an invalid input.
    with pytest.raises(TypeError):
        find_individual([1.0])


def test_empty():
    # list is empty
    # This is an invalid input.
    with pytest.raises(ValueError):
        find_individual([])


def test_wrong_length():
    # length is not odd
    # This is an invalid input.
    with pytest.raises(ValueError):
        find_individual([1, 1, 2, 2])


def test_occurrs_too_often():
    # element occurs neither once nor twice
    # This is an invalid input.
    with pytest.raises(ValueError):
        find_individual([1, 1, 1])


def test_more_than_one_single_el():
    # more than one single element
    # This is an invalid input.
    with pytest.raises(ValueError):
        find_individual([1, 1, 2, 3, 4])
