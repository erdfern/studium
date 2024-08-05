--negation
neg :: Bool -> Bool
neg False   = True
neg True    = False

-- Konjunktion
(<&>) :: Bool -> Bool -> Bool
(<&>) False False   = False
(<&>) False True    = False
(<&>) True False    = False
(<&>) True True     = True

-- Konjunktion 2
(<&&>) :: Bool -> Bool -> Bool
False <&&> False   = False
False <&&> True    = False
True <&&> False    = False
True <&&> True     = True

-- Konjunktion 3
(<&&&>) :: Bool -> Bool -> Bool
(<&&&>) True True   = True
(<&&&>) a b         = False

-- Konjunktion 4
(<&&&&>) :: Bool -> Bool -> Bool
True <&&&&> True   = True
_ <&&&&> _         = False
