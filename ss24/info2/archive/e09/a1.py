import sys


def main():
    """
    We read 1 or 3 arguments.
    The first is an integer x.
    The second and third are integers a and b.

    If we have 1 argument, we print x in binary and decimal.

    If we have three arguments, we interpret a and b as decimal numbers.
    The bits of index a to b-1 of the binary representation of x are the integer y.
    We print y in binary and decimal.
    """
    try:
        if len(sys.argv) == 2:
            x = int(sys.argv[1])
            print(f"{x} in binary: {bin(x)}")
            print(f"{x} in decimal: {x}")
        elif len(sys.argv) == 4:
            x = int(sys.argv[1])
            a = int(sys.argv[2])
            b = int(sys.argv[3])
            if a >= b:
                raise ValueError("a must be less than b")
            y = int(bin(x)[2:].zfill(b)[a:b], 2)
            print(f"{y} in binary: {bin(y)}")
            print(f"{y} in decimal: {y}")
        else:
            raise ValueError("Invalid number of arguments")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
# import sys


# def main():
#     """
#     We read 1 or 3 arguments.
#     The first is an integer x.
#     The second and third are integers a and b.

#     If we have 1 argument, we print x in binary and decimal.

#     If we have three arguments, we interpret a and b as decimal numbers.
#     The bits of index a to b-1 of the binary representation of x are the integer y.
#     We print y in binary and decimal.
#     """
#     if len(sys.argv) == 2:
#         x = int(sys.argv[1])
#         print(f"{x} in binary: {bin(x)}")
#         print(f"{x} in decimal: {x}")
#     elif len(sys.argv) == 4:
#         x = int(sys.argv[1])
#         a = int(sys.argv[2])
#         b = int(sys.argv[3])
#         y = int(bin(x)[2:].zfill(b)[a:b], 2)
#         print(f"{y} in binary: {bin(y)}")
#         print(f"{y} in decimal: {y}")


# if __name__ == "__main__":
#     main()
