data Signal = X | O

instance Show Signal where
    show X = "X"
    show O = "O"

instance Eq Signal where
    O == O  = True
    O == X  = False
    X == O  = False
    X == X  = True
