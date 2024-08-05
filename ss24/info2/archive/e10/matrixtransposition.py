import sys


def matrix_to_string(matrix):
    return ''.join(''.join(row) for row in matrix)


def make_matrix(row_length, msg):
    matrix = []
    row = []

    for i in range(len(msg)):
        row.append(msg[i])
        if (i + 1) % row_length == 0:
            matrix.append(row)
            row = []

    if row:
        for _ in range(row_length - len(row)):
            row.append('X')
        matrix.append(row)

    return matrix


def encode(row_length, msg):
    transposed = zip(*make_matrix(row_length, msg))

    encoded = ""
    for column in transposed:
        for char in column:
            encoded += char
    return encoded


def decode(row_length, msg):
    # Zeilen der urspruenglichen matrix
    n_rows = len(msg) // row_length
    if len(msg) % row_length != 0:
        n_rows += 1

    # Liste der Spalten der kodierten Nachricht
    columns = [list(msg[i*n_rows:(i+1)*n_rows]) for i in range(row_length)]

    # Transposition der Spalten um die urspruengliche Matrix zu erhalten
    matrix = list(map(list, zip(*columns)))

    return matrix_to_string(matrix)


def print_matrix(matrix):
    for row in matrix:
        print(' '.join(row))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python matrixtransposition.py [d, e]<length> <msg>")
        sys.exit(1)

    if sys.argv[1] not in ["d", "e"]:
        print("Mode must be one of d or e")
        sys.exit(1)

    try:
        row_length = int(sys.argv[2])
    except ValueError:
        print("Length must be an integer")
        sys.exit(1)

    msg = sys.argv[3]

    if sys.argv[1] == "d":
        print(decode(row_length, msg))
    else:
        print(encode(row_length, msg))
