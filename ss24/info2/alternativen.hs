-- Betrag
absolute :: Int ->  Int 
absolute x = if x < 0 then -x else x

-- XOR
(<+>) :: Bool -> Bool -> Bool
(<+>) a b
    | a == b    = False
    | otherwise = True

-- Vergleichsfunktion
comp :: Int -> Int -> Int
comp x y
    | x > y     = 1
    | x < y     = -1
    | otherwise = 0


