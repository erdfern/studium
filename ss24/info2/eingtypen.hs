data Signal = X | O

instance Show Signal where
    show X = "X"
    show O = "O"

instance Eq Signal where
    O == O  = True
    O == X  = False
    X == O  = False
    X == X  = True

instance Ord Signal where
    X <= O = True
    O <= X = False

contains :: (Eq a) => a -> [a] -> Bool
contains _ [] = False
contains z (x:xs)
    | z == x    = True
    | otherwise = contains z xs
