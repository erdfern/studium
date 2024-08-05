# Terminale
terminals = ("id", "(", ")", ":=", "+", "-", "*", "/", "$$")

# Parse-Tabelle
parsing_table = (
    {"id": (1,), "$$": (1,)},  # 0
    {"id": (2, 1), "$$": ()},  # 1
    {"id": ("id", ":=", 3)},  # 2
    {"id": (5, 4), "(": (5, 4)},  # 3
    {"id": (), ")": (), "+": (8, 5, 4), "-": (8, 5, 4), "$$": ()},  # 4
    {"id": (7, 6), "(": (7, 6)},  # 5
    {
        "id": (),
        ")": (),
        "+": (),
        "-": (),
        "*": (9, 7, 6),
        "/": (9, 7, 6),
        "$$": (),
    },  # 6
    {"id": ("id",), "(": ("(", 3, ")")},  # 7
    {"+": ("+"), ("-"): ("-")},  # 8
    {"*": ("*"), ("/"): ("/")},  # 9
)


def tokenize(str):
    """
    Wandelt eine Zeichenkette in eine Liste von Terminalen um.
    Wir gehen davon aus, dass die Zeichenkette keine Leerzeichen enthält
    und nur aus Terminalen besteht.
    """
    tokens = []
    current_token = ""
    for char in str:
        # multi-char Tokens erkennen
        current_token += char
        # ist das aktuelle Token ein Terminal? Dann konsumieren und neues Token beginnen
        if current_token in terminals:
            tokens.append(current_token)
            current_token = ""
    # bleibt ein Token übrig, so ist es ein Fehler
    if current_token:
        print(f"Error: Invalid token {current_token}")
        return None
    # $$ anhängen und zurückgeben
    tokens.append("$$")
    return tokens


def parse(tokens):
    """
    Parsed eine Liste von Token.
    """
    print(tokens)

    # Initialisiere den Stack mit dem Startsymbol
    stack = [0]
    token_index = 0
    current_token = tokens[token_index]

    # Iteriere solange, bis der Stack leer ist
    while stack:
        # print(f"Stack: {stack}")
        # print(f"Current token: {current_token}")
        # print(f"Token index: {token_index}")
        # print()

        # Überprüfe, ob das oberste Element des Stacks mit dem aktuellen Token übereinstimmt
        if stack[-1] == current_token:  # Match, also handelt es sich um ein Terminal
            # Wir entfernen das Element vom Stack
            stack.pop()
            # und gehen zum nächsten Token
            token_index += 1
            current_token = tokens[token_index]
        else:  # Kein Match, also handelt es sich um ein Nichtterminal
            # Lookup der Produktion in der Parse-Tabelle
            production = parsing_table[stack[-1]].get(current_token)
            if production or production == ():
                # Entferne das Nichtterminal vom Stack
                stack.pop()
                # Prüfe, ob die Produktion auf das leere Wort abbildet
                if production == ():
                    # In diesem Fall fahren wir fort, ohne neue Elemente auf den Stack zu legen
                    continue
                else:
                    # Füge die rechte Seite der Produktion in umgekehrter Reihenfolge zum Stack hinzu
                    stack.extend(production[::-1])
            else:
                print(f"Error: unexpected token {current_token}")
                exit()
                # return


def test_scanning():
    valid_input = "id:=id*(id+id)"
    print(f"Testing valid input '{valid_input}':")
    tokens = tokenize(valid_input)
    print(tokens)
    print()

    invalid_input = "id:=id*{id+id}"
    print(f"Testing invalid input '{invalid_input}':")
    tokens = tokenize(invalid_input)
    print(tokens)
    print()


def test_parser():
    # Test with valid inputs
    valid_inputs = [
        "id:=id",
        "id:=id+id",
        "id:=id-id",
        "id:=id*id",
        "id:=id/id",
        "id:=id*(id+id)",
        "id:=(id+id)*id",
    ]
    for input_str in valid_inputs:
        tokens = tokenize(input_str)
        if tokens is not None:
            print(f"Testing valid input '{input_str}':")
            parse(tokens)
            print()

    # Test with invalid inputs
    # Crashed/Beendet das Programm
    invalid_inputs = [
        "",
        "INVALID",
        "id",
        "id:=id+",
        "id:=id-",
        "id:=id*",
        "id:=id/",
    ]
    for input_str in invalid_inputs:
        tokens = tokenize(input_str)
        if tokens is not None:
            print(f"Testing invalid input '{input_str}':")
            parse(tokens)
            print()


if __name__ == "__main__":
    # Run the tests
    test_scanning()
    # test_parser()
    input_str = "id:=id*(id+id)"
    parse(tokenize(input_str))
